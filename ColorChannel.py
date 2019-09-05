import pyqtgraph as pg
from ImageItems import DrawingImage, HoverImage
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import ImageProc as ip
import os
import datetime
import skimage.measure as skm


class Channel:
    colors = {'r': 0, 'g': 1, 'b': 2, 'w': 3}
    nchannels = 0

    def __init__(self, tab, c, img_dim, name=None):
        self.c = c
        print(img_dim)
        print(name)
        if name is None:
            self.name = "Channel{}".format(Channel.nchannels)
        else:
            self.name = name
        self.background_img_item = pg.ImageItem(opacity=1, border=pg.mkPen(c, width=5))
        self.background_img = None
        self.background_img_and_dapi = None
        self.background_dapi = None
        self.current_img = None  # current
        self.img_dim = img_dim
        self.layerlines = []

        layout = QHBoxLayout(tab)
        tab.setLayout(layout)
        self.view = pg.GraphicsView(parent=tab)
        self.viewbox = pg.ViewBox(lockAspect=True)
        self.viewbox.invertY()
        self.view.setCentralItem(self.viewbox)
        layout.addWidget(self.view)

        self.viewbox.addItem(self.background_img_item)

        Channel.nchannels += 1

    def setBackgroundImage(self, img, singleImg, dapiImg, align=True, setbg=True):
        #print("setbackground")
        #print(img.shape)
        #print(img.ndim)
        #print(self.img_dim)
        #print(self.name)
        if align:
            if self.img_dim == 3:
                self.background_img_item.setImage(img.transpose(1, 0, 2))
                self.current_img = img
            else:
                self.background_img_item.setImage(img.T)
                self.current_img = img
        else:
            self.background_img_item.setImage(singleImg)
        if setbg:
            self.background_img = singleImg  # just cells
            self.background_img_and_dapi = img  # cells and dapi
            self.background_dapi = dapiImg  # just dapi

    def hasBackground(self):
        return self.background_img is not None

    def updateLayers(self, layer, value):
        self.layerlines[layer].setValue(value)

    def getLayerValues(self):
        numLayers = len(self.layerlines)
        layerValues = []
        for x in range(numLayers):
            layerValues.append(self.layerlines[x].value())
        return layerValues

    def hidebg(self):
        pass

    def showbg(self):
        pass

    def showDapi(self):
        pass

    def hideDapi(self):
        pass

    def showCells(self):
        pass

    def hideCells(self):
        pass

    def reset(self):
        self.viewbox.removeItem(self.background_img_item)
        for l in self.layerlines:
            self.viewbox.removeItem(l)
        self.background_img_item = pg.ImageItem(opacity=1, border=pg.mkPen(self.c, width=5))
        self.background_img = None
        self.layerlines = []
        self.viewbox.addItem(self.background_img_item)

    def setLayers(self, layers):
        for layer in layers:
            line = pg.InfiniteLine(movable=False, angle=0)
            line.setValue(layer)
            self.viewbox.addItem(line)
            self.layerlines.append(line)

    def hasLayers(self):
        return len(self.layerlines) != 0


class LayerChannel(Channel):

    def setLayers(self, layers):
        for layer in layers:
            line = pg.InfiniteLine(movable=True, angle=0)
            line.setValue(layer)
            self.viewbox.addItem(line)
            self.layerlines.append(line)

    def addLayers(self, numLayers):
        layers = ip.addLayers(self.background_img, numLayers)
        self.setLayers(layers)
        return layers


class DetectionChannel(Channel):

    def __init__(self, tab, c, img_dim, name=None):
        super().__init__(tab, c, img_dim, name)

        self.label_img_item = DrawingImage(c, compositionMode=pg.QtGui.QPainter.CompositionMode_Plus, opacity=1)
        self.hover_img_item = HoverImage(self.img_dim, opacity=1,
                                         compositionMode=pg.QtGui.QPainter.CompositionMode_Plus)
        self.histogram_item = pg.HistogramLUTItem()
        self.histogram_item.setImageItem(self.background_img_item)
        self.histogram_item.setMinimumHeight(500)
        self.histogram_item.setHistogramRange(0, 300)
        self.histogram_state = None
        self.threshold_value = 0
        self.minSize_value = 0
        self.maxSize_value = 0
        self.Template_variance_value = 0
        self.Template_size_value = 0

        self.viewbox.addItem(self.label_img_item)
        self.viewbox.addItem(self.hover_img_item)

        self.view.addItem(self.histogram_item)

        self.thresholds = []
        self.areaThreshold = 0

    def reset(self):
        super().reset()
        self.viewbox.removeItem(self.hover_img_item)
        self.viewbox.removeItem(self.label_img_item)
        self.view.removeItem(self.histogram_item)
        self.label_img_item = DrawingImage(self.c, compositionMode=pg.QtGui.QPainter.CompositionMode_Plus, opacity=1)
        self.hover_img_item = HoverImage(self.img_dim, opacity=1,
                                         compositionMode=pg.QtGui.QPainter.CompositionMode_Plus)
        self.histogram_item = pg.HistogramLUTItem()
        self.histogram_item.setImageItem(self.background_img_item)
        self.histogram_item.setMinimumHeight(500)
        self.histogram_item.setHistogramRange(0, 300)
        self.histogram_state = None
        self.viewbox.addItem(self.label_img_item)
        self.viewbox.addItem(self.hover_img_item)
        self.view.addItem(self.histogram_item)

    def showbg(self):
        if self.img_dim == 2:
            self.setBackgroundImage(self.background_img, self.background_img, self.background_img, setbg=False)
        elif self.img_dim == 3:
            self.setBackgroundImage(self.background_img_and_dapi, self.background_img, self.background_dapi,
                                    setbg=False)
        if self.histogram_state is not None:
            self.histogram_item.restoreState(self.histogram_state)

    def hidebg(self):
        self.histogram_state = self.histogram_item.saveState()
        self.setBackgroundImage(np.zeros_like(self.background_img), np.zeros_like(self.background_img),
                                np.zeros_like(self.background_img), setbg=False)

    def showDapi(self):
        tempImg = self.current_img.copy()
        if self.c == 'r':
            tempImg[:, :, 2] = self.background_dapi
        elif self.c == 'g':
            tempImg[:, :, 2] = self.background_dapi
        elif self.c == 'b':
            tempImg[:, :, 0] = self.background_dapi
        self.setBackgroundImage(tempImg, self.current_img, self.current_img, setbg=False)

    def hideDapi(self):
        tempImg = self.current_img.copy()
        if self.c == 'r':
            tempImg[:, :, 2] = 0
        elif self.c == 'g':
            tempImg[:, :, 2] = 0
        elif self.c == 'b':
            tempImg[:, :, 0] = 0
        self.setBackgroundImage(tempImg, self.current_img, self.current_img, setbg=False)

    def showCells(self):
        tempImg = self.current_img.copy()
        if self.c == 'r':
            tempImg[:, :, 0] = self.background_img
        elif self.c == 'g':
            tempImg[:, :, 1] = self.background_img
        elif self.c == 'b':
            tempImg[:, :, 2] = self.background_img
        self.setBackgroundImage(tempImg, self.current_img, self.current_img, setbg=False)

    def hideCells(self):
        tempImg = self.current_img.copy()
        if self.c == 'r':
            tempImg[:, :, 0] = 0
        elif self.c == 'g':
            tempImg[:, :, 1] = 0
        elif self.c == 'b':
            tempImg[:, :, 2] = 0
        self.setBackgroundImage(tempImg, self.current_img, self.current_img, setbg=False)

    @property
    def label_img(self):
        if self.label_img_item.image is None:
            return None
        return self.label_img_item.image[:, :, super().colors[self.c]]

    def setBackgroundImage(self, img, singleImg, dapiImg, setbg=True):
        print(self.name)
        super().setBackgroundImage(img, singleImg, dapiImg, setbg=setbg)
        if self.img_dim == 3:
            self.hover_img_item.setImage(np.zeros_like(img.transpose(1, 0, 2), dtype=np.uint8))
        else:
            self.hover_img_item.setImage(np.zeros_like(img.T, dtype=np.uint8))
        self.histogram_item.setLevels(0, 255)

    def getLabels(self):
        im = np.any(self.label_img_item.image, axis=2) * 255
        return im.T

    def runDetection(self, ts, var, mins, maxs, th):
        labels = ip.findCells(self.background_img, ts, var, mins, maxs, th)
        self.threshold_value = th
        self.minSize_value = mins
        self.maxSize_value = maxs
        self.Template_variance_value = var
        self.Template_size_value = ts
        im = np.zeros((labels.shape[1], labels.shape[0], 3))
        im[:, :, super().colors[self.c]] = labels.T
        self.label_img_item.setImage(im)

    def hasLabels(self):
        return self.label_img is not None

    def countCells(self, thresholds, layerVals):
        print("hi")
        self.thresholds = thresholds
        print(self.thresholds)
        counts = ip.countCells(self.label_img > 0, 'single', self.thresholds, layerVals)
        return counts

    def findAreaThreshold(self):
        areaSum = 0
        averageArea = 0
        labels = skm.label(self.label_img > 0)
        stats = skm.regionprops(labels)
        if len(stats) > 0:
            for p in stats:
                areaSum += p.area
            averageArea = areaSum / len(stats)
        self.areaThreshold = averageArea * 0.4  # ignore bottom 5%
        return self.areaThreshold

    def set_brushsize(self, value):
        self.label_img_item.setKernel(value)
        self.hover_img_item.setKernel(value, self.img_dim)

    def findCellsPixelValue(self, img):
        self.areaThreshold = self.findAreaThreshold()
        expressionLevelAvg, expressionLevelArray = ip.findCellsPixelValue(self.label_img_item.image[:, :, super().colors[self.c]], self.areaThreshold, img)
        return expressionLevelAvg, expressionLevelArray


class ResultsChannel(Channel):

    def __init__(self, tab, c, channels, name=None):
        super().__init__(tab, c, channels, name)
        self.channels = channels
        self.cell_counts = None
        self.thresholds = []

    def hasCellCounts(self):
        return self.cell_counts is not None

    def getLabels(self):
        im = (self.background_img_item.image > 0) * 255
        return im.T

    def updateColocal(self):
        size = len(self.channels)
       # self.thresholds = []
       # for chan in self.channels:
        #    self.thresholds.append(chan.areaThreshold())
       # image = 1
       # for c in self.channels:
       #     image = image * c.label_img
        #image = image.astype(np.uint16)
       # image = np.where(image > 0, 255, 0)
        #image = image.T
       # colocal = ip.processColoc(image, self.thresholds)
        if size == 2:
            colocal = np.stack([c.label_img for c in self.channels] + [np.zeros_like(self.channels[0].label_img)],
                               axis=2) * 255
            self.background_img_item.setImage(colocal)
        else:
            colocal = np.stack([c.label_img for c in self.channels], axis=2) * 255
            self.background_img_item.setImage(colocal)

    def countCells(self, countAllCombos):
        countAll = countAllCombos
        #  with open('config.json') as json_data_file:
        #      data = json.load(json_data_file)
        #  if data['countAllCombos']=="Yes":
        #      countAll = True
        self.columnNames = []
        for c in self.channels:
            self.columnNames.append(c.name)
        if countAll:
            startIndex = 1
            for x in range(0, len(self.channels) - 1):
                for y in range(startIndex, len(self.channels)):
                    hName = self.channels[x].name + "_" + self.channels[y].name
                    self.columnNames.append(hName)
                startIndex += 1
        self.updateColocal()
        if len(self.layerlines) == 0:
            layerVals = None
        else:
            layerVals = [layer.value() for layer in self.layerlines]
        image = 1
        for c in self.channels:
            image = image * c.label_img
        if countAll:
            red_green_coloc = self.channels[0].label_img * self.channels[1].label_img
            red_blue_coloc = self.channels[0].label_img * self.channels[2].label_img
            green_blue_coloc = self.channels[1].label_img * self.channels[2].label_img
            coloc = []
            coloc.append(red_green_coloc)
            coloc.append(red_blue_coloc)
            coloc.append(green_blue_coloc)

        self.thresholds = []
        for chan in self.channels:
            self.thresholds.append(chan.findAreaThreshold())

        counts = [ip.countCells(image > 0, 'coloc', self.thresholds, layerVals)]
        for chan in self.channels:
            counts.append(chan.countCells(self.thresholds, layerVals))
            print(counts)
        if countAll:
            for col in coloc:
                counts.append(ip.countCells(col > 0, 'coloc', self.thresholds, layerVals))
        if not layerVals == None:
            self.cell_counts = np.stack(counts, axis=1)
        else:
            self.cell_counts = np.hstack(counts)
            self.cell_counts = self.cell_counts.reshape(1, self.cell_counts.shape[0])
        string = "Layer / {}".format(self.name)
        string += "".join(['/ ' + c for c in self.columnNames])
        string += '\n'
        if layerVals is None:
            string += "{:<d}   ".format(1)
            for num in self.cell_counts:
                string += "{:3d}   ".format(num)

        else:
            subString = "{:<d}   "
            for i in range(self.cell_counts.shape[0]):  # layers
                string += subString.format(i + 1)
                for j in range(self.cell_counts.shape[1]):  # channels
                    string += "{:0>3d}   ".format(self.cell_counts[i, j])
                string += '\n'
        return string

    def exportData(self, export_text, fname_text, expressionLevelArray, reporterChannel):
        now = datetime.datetime.now()
        dir_name = export_text
        path, base_filename = os.path.split(fname_text)
        base_filename, _ = os.path.splitext(base_filename)
        base_filename = base_filename + str(now.year) + "-" + str(now.month) +  "-" + str(now.day) + "-" + str(now.hour) + "," + str(now.minute)
        full_fn = os.path.join(dir_name, base_filename)
        np.savetxt(full_fn + ".csv", self.cell_counts, fmt='%d', delimiter=',',
                   header=self.name + "".join([', ' + c for c in self.columnNames]), comments="")
        if reporterChannel != None:
            np.savetxt(full_fn + "_Expression_Test_results.csv", expressionLevelArray, fmt='%1.3f', delimiter = ',')

        channelLabels = []
        channelNames = []
        thresholdValues = []
        minValues = []
        maxValues = []
        tsValues = []
        varValues = []
        image = 1

        for c in self.channels:
            channelLabels.append(c.getLabels())
            image = image * c.label_img
            channelNames.append(c.name)
            thresholdValues.append(c.threshold_value)
            minValues.append(c.minSize_value)
            maxValues.append(c.maxSize_value)
            tsValues.append(c.Template_size_value)
            varValues.append(c.Template_variance_value)

        image = image.astype(np.uint16)
        image = np.where(image > 0, 255, 0)
        channelLabels.append(image.T)
        channelNames.append("coloc")
        layerValues = self.getLayerValues()
        ip.saveImages(full_fn, channelLabels, channelNames, layerValues, thresholdValues, minValues, maxValues,
                      tsValues, varValues)

        return full_fn