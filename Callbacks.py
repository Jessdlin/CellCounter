from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import numpy as np
import os
from ColorChannel import DetectionChannel
import json
from skimage.measure import block_reduce
from skimage.external.tifffile import TiffFile

class Mixin:
    def browse_button_dapi_callback(self):
        dapi_filename, _ = QFileDialog.getOpenFileName(self, "Select Dapi File", "./images",
                                                       "Tiff Files(*.tif);;All Files (*)")
        if not os.path.isfile(dapi_filename):
            self.status_box.append("User pressed cancel or selected invalid file")
            return
        self.fname_entry_dapi.setText(dapi_filename)
        # Open Dapi Image
        dapiIm = cv2.imread(dapi_filename)
        x, y, z = dapiIm.shape
        if x >= 2500 and y >= 2500:
            dapiIm = block_reduce(dapiIm, block_size=(2, 2, 1), func=np.mean)
        x, y, z = dapiIm.shape
        # print(x)
        self.dapi, gdapi, rdapi = cv2.split(dapiIm)
        if self.dapi.sum() == 0:
            self.status_box.append("Invalid image")
            return
        else:
            # print("hi")
            self.layersChannel.setBackgroundImage(self.dapi, self.dapi, self.dapi)
        if self.contains_meta_data:
            self.layersChannel.setLayers(self.meta_layers)
            self.redChannel.setLayers(self.meta_layers)
            self.greenChannel.setLayers(self.meta_layers)
            self.blueChannel.setLayers(self.meta_layers)
            self.resultChannel.setLayers(self.meta_layers)

    def browse_button_callback(self):
        # print(self.Tabs)
        # self.getParameters()
        filename, _ = QFileDialog.getOpenFileName(self, "Select Image File", "./images",
                                                  "Tiff Files(*.tif);;All Files (*)")
        if not os.path.isfile(filename):
            self.status_box.append("User pressed cancel or selected invalid file")
            return
        self.fname_entry.setText(filename)

        # Open Image
        im = cv2.imread(filename)

        if im is None:
            self.status_box.append("Invalid image")
            return
        for c in self.channels:
            c.reset()
        x, y, z = im.shape
        if x >= 2500 and y >= 2500: #reduce if image is too large
            im = block_reduce(im, block_size=(2, 2, 1), func=np.mean)

        self.blueImg, self.greenImg, self.redImg = cv2.split(im)
        print(self.layerChannelName)
        if self.show_Dapi:
            if self.layerChannelName == "Separate":
                imR = im.copy()
                imR[:, :, 2] = self.dapi
                imR[:, :, 1] = 0
                imR[:, :, 0] = self.redImg

                imG = im.copy()
                imG[:, :, 2] = self.dapi
                imG[:, :, 0] = 0
                imG[:, :, 1] = self.greenImg

                imB = im.copy()
                imB[:, :, 0] = self.dapi
                imB[:, :, 1] = 0
                imB[:, :, 2] = self.blueImg
                self.blueChannel.setBackgroundImage(imB, self.blueImg, self.dapi)
                self.redChannel.setBackgroundImage(imR, self.redImg, self.dapi)
                self.greenChannel.setBackgroundImage(imG, self.greenImg, self.dapi)
                self.layersChannel.setBackgroundImage(self.dapi, self.dapi, self.dapi)
            elif self.layerChannelName == "Blue":
                imR = im.copy()
                imR[:, :, 2] = self.blueImg
                imR[:, :, 1] = 0
                imR[:, :, 0] = self.redImg

                imG = im.copy()
                imG[:, :, 2] = self.blueImg
                imG[:, :, 0] = 0
                imG[:, :, 1] = self.greenImg

                self.blueChannel.setBackgroundImage(self.blueImg, self.blueImg, self.blueImg)
                self.redChannel.setBackgroundImage(imR, self.redImg, self.blueImg)
                self.greenChannel.setBackgroundImage(imG, self.greenImg, self.blueImg)
                self.layersChannel.setBackgroundImage(self.dapi, self.dapi, self.dapi)

        else:
            #if blueImg.sum() == 0:
            #    self.status_box.append("Selected image has no blue channel")
            #else:
            #    self.blueChannel.setBackgroundImage(blueImg, blueImg, blueImg)
            if self.layerChannelName == "Blue":
                self.redChannel.setBackgroundImage(self.redImg, self.redImg, self.blueImg)
                self.greenChannel.setBackgroundImage(self.greenImg, self.greenImg, self.blueImg)
                self.layersChannel.setBackgroundImage(self.blueImg, self.blueImg, self.blueImg)
            elif self.layerChannelName == "Separate":
                self.redChannel.setBackgroundImage(self.redImg, self.redImg, self.blueImg)
                self.greenChannel.setBackgroundImage(self.greenImg, self.greenImg, self.blueImg)
                self.blueChannel.setBackgroundImage(self.blueImg, self.blueImg, self.blueImg)
                self.layersChannel.setBackgroundImage(self.dapi, self.dapi, self.dapi)
            #elif self.layerChannelName != 'Blue':
            #     if self.layerChannelName == "Red":
            #        self.layersChannel.setBackgroundImage(redImg, redImg, redImg)
            #    elif self.layerChannelName == "Green":
            #        self.layersChannel.setBackgroundImage(greenImg, greenImg, greenImg)
        if self.contains_meta_data:
            self.redChannel.label_img_item.setImage(self.red_labels)
            self.greenChannel.label_img_item.setImage(self.green_labels)
            self.blueChannel.label_img_item.setImage(self.blue_labels)
            self.layersChannel.setLayers(self.meta_layers)
            self.redChannel.setLayers(self.meta_layers)
            self.greenChannel.setLayers(self.meta_layers)
            self.blueChannel.setLayers(self.meta_layers)
            self.resultChannel.setLayers(self.meta_layers)
        if 'b' in self.detectionChannels:
            if self.current_tab in [self.Tabs['red'], self.Tabs['green'], self.Tabs['blue']]:
                self.run_button.setEnabled(True)
        else:
            if self.current_tab in [self.Tabs['red'], self.Tabs['green']]:
                self.run_button.setEnabled(True)
        #self.layersChannel.setBackgroundImage(self.dapi, self.dapi, self.dapi)


    def rbrowse_button_callback(self):
        rfilename, _ = QFileDialog.getOpenFileName(self, "Select Image File", "./images",
                                                   "Tiff Files(*.tif);;All Files (*)")
        if not os.path.isfile(rfilename):
            self.rfname_entry.setText("User pressed cancel or selected invalid file")
            return
        red_img = cv2.imread(rfilename)
        if red_img is None:
            self.rfname_entry.setText("Invalid Image")
            return
        self.rfname_entry.setText(rfilename)
        with TiffFile(rfilename) as tif:
            red_labels = tif.asarray()
            red_labels = red_labels.astype(np.uint8)
            red_labels[:20, :] = 0
            red_labels[:, :20] = 0
            red_labels[-20:, :] = 0
            red_labels[:, -20:] = 0
            im = np.zeros((red_labels.shape[1], red_labels.shape[0], 3))
            im[:, :, 0] = red_labels.T
            self.red_labels = im
            red_metadata = tif[0].image_description
            red_metadata = json.loads(red_metadata.decode('utf-8'))
            self.meta_layers = red_metadata['layers']

    def gbrowse_button_callback(self):
        gfilename, _ = QFileDialog.getOpenFileName(self, "Select Image File", "./images",
                                                   "Tiff Files(*.tif);;All Files (*)")
        if not os.path.isfile(gfilename):
            self.gfname_entry.setText("User pressed cancel or selected invalid file")
            return
        green_img = cv2.imread(gfilename)
        if green_img is None:
            self.gfname_entry.setText("Invalid Image")
            return
        self.gfname_entry.setText(gfilename)
        with TiffFile(gfilename) as tif:
            green_labels = tif.asarray()
            green_labels = green_labels.astype(np.uint8)
            green_labels[:20, :] = 0
            green_labels[:, :20] = 0
            green_labels[-20:, :] = 0
            green_labels[:, -20:] = 0
            im = np.zeros((green_labels.shape[1], green_labels.shape[0], 3))
            im[:, :, 1] = green_labels.T
            self.green_labels = im
            green_metadata = tif[0].image_description
            green_metadata = json.loads(green_metadata.decode('utf-8'))

    def bbrowse_button_callback(self):
        bfilename, _ = QFileDialog.getOpenFileName(self, "Select Image File", "./images",
                                                   "Tiff Files(*.tif);;All Files (*)")
        if not os.path.isfile(bfilename):
            self.gfname_entry.setText("User pressed cancel or selected invalid file")
            return
        blue_img = cv2.imread(bfilename)
        if blue_img is None:
            self.bfname_entry.setText("Invalid Image")
            return
        self.bfname_entry.setText(bfilename)
        with TiffFile(bfilename) as tif:
            blue_labels = tif.asarray()
            blue_labels = blue_labels.astype(np.uint8)
            blue_labels[:20, :] = 0
            blue_labels[:, :20] = 0
            blue_labels[-20:, :] = 0
            blue_labels[:, -20:] = 0
            im = np.zeros((blue_labels.shape[1], blue_labels.shape[0], 3))
            im[:, :, 2] = blue_labels.T
            self.blue_labels = im
            blue_metadata = tif[0].image_description
            blue_metadata = json.loads(blue_metadata.decode('utf-8'))

    def browse_export_button_callback(self):
        dirname = QFileDialog.getExistingDirectory(self, "Select export location", "./", QFileDialog.ShowDirsOnly)
        self.export_entry.setText(dirname)

    def export_button_callback(self):
        if not self.resultChannel.hasCellCounts():
            self.status_box.append("Count cells before exporting")
            return
        full_fn = self.resultChannel.exportData(self.export_entry.text(), self.fname_entry.text(), self.expressionLevelArray, self.reporterChannel)
        self.status_box.append("saving " + full_fn)

    def run_button_callback(self):
        if not self.channels[self.current_tab].hasBackground():
            self.status_box.append("Choose image before running")
            return
        self.channels[self.current_tab].runDetection(self.tempsize, self.variance, self.minSize, self.maxSize,
                                                     self.threshold)
        if self.channels[self.Tabs[self.reporterChannel]].hasLabels():
            self.expressionTest_button.setEnabled(True)

    def layer_button_callback(self):
        if self.layerChannelName == "Blue":
            if self.current_tab == self.Tabs[
                'blue'] and self.layersChannel.hasBackground() and not self.layersChannel.hasLayers():
                layers = self.layersChannel.addLayers(self.numLayers)
                self.redChannel.setLayers(layers)
                self.greenChannel.setLayers(layers)
                self.resultChannel.setLayers(layers)
        elif 'b' in self.detectionChannels:
            if self.current_tab == self.Tabs[
                'layers'] and self.layersChannel.hasBackground() and not self.layersChannel.hasLayers():
                layers = self.layersChannel.addLayers(self.numLayers)
                self.redChannel.setLayers(layers)
                self.greenChannel.setLayers(layers)
                self.blueChannel.setLayers(layers)
                self.resultChannel.setLayers(layers)
        elif 'b' not in self.detectionChannels and self.layerChannelName != "Blue":
            if self.current_tab == self.Tabs[
                'layers'] and self.layersChannel.hasBackground() and not self.layersChannel.hasLayers():
                layers = self.layersChannel.addLayers(self.numLayers)
                self.redChannel.setLayers(layers)
                self.greenChannel.setLayers(layers)
                self.resultChannel.setLayers(layers)
        if self.layerChannelName == "Blue":
            for i, layerline in enumerate(self.layersChannel.layerlines):
                layerline.sigPositionChangeFinished.connect(self.change_lines(i))
        else:
            for i, layerline in enumerate(self.layersChannel.layerlines):
                layerline.sigPositionChangeFinished.connect(self.change_lines(i))

    def change_lines(self, lineNum):
        # self.getParameters()
        if self.layerChannelName == "Blue":
            bluelayerline = self.layersChannel.layerlines[lineNum]
        else:
            bluelayerline = self.layersChannel.layerlines[lineNum]

        def layer_function():
            if self.layerChannelName == "Blue" or 'b' not in self.detectionChannels:
                self.redChannel.updateLayers(lineNum, bluelayerline.value())
                self.greenChannel.updateLayers(lineNum, bluelayerline.value())
                self.resultChannel.updateLayers(lineNum, bluelayerline.value())
            elif 'b' in self.detectionChannels:
                self.redChannel.updateLayers(lineNum, bluelayerline.value())
                self.greenChannel.updateLayers(lineNum, bluelayerline.value())
                self.blueChannel.updateLayers(lineNum, bluelayerline.value())
                self.resultChannel.updateLayers(lineNum, bluelayerline.value())

        return layer_function

    def tab_changed_callback(self, index):
        # self.getParameters()
        self.current_tab = index
        channel = self.channels[self.current_tab]
        print(channel)
        print(self.layersChannel.hasBackground())
        if isinstance(channel, DetectionChannel):
            channel.set_brushsize(self.brushsize)
            if self.showhidebg_button.isChecked():
                channel.showbg()
            else:
                channel.hidebg()
            if self.showhidelabels_button.isChecked():
                channel.label_img_item.setVisible(True)
            else:
                channel.label_img_item.setVisible(False)

        # Run Button
        if self.current_tab == self.Tabs['red'] and self.redChannel.hasBackground():
            self.run_button.setEnabled(True)
        elif self.current_tab == self.Tabs['green'] and self.greenChannel.hasBackground():
            self.run_button.setEnabled(True)
        elif 'b' in self.detectionChannels and self.current_tab == self.Tabs['blue']:
            if self.layerChannelName == 'Blue':
                self.run_button.setEnabled(False)
            elif self.layerChannelName != 'Blue' and self.blueChannel.hasBackground():
                self.run_button.setEnabled(True)
        else:
            self.run_button.setEnabled(False)
        # Layer Button
        if self.layerChannelName == "Blue" and self.current_tab == self.Tabs[
            'blue'] and self.layersChannel.hasBackground():
            self.layer_button.setEnabled(True)
        elif self.layerChannelName != "Blue" and self.current_tab == self.Tabs[
            'layers'] and self.layersChannel.hasBackground():
            self.layer_button.setEnabled(True)
        else:
            self.layer_button.setEnabled(False)
        # Update result channel
        if 'b' not in self.detectionChannels:
            if (self.current_tab == self.Tabs['results'] and
                    self.greenChannel.hasLabels() and
                    self.redChannel.hasLabels()):
                self.resultChannel.updateColocal()
        elif 'b' in self.detectionChannels:
            if (self.current_tab == self.Tabs['results'] and
                    self.greenChannel.hasLabels() and
                    self.redChannel.hasLabels() and self.blueChannel.hasLabels()):
                self.resultChannel.updateColocal()

    def count_button_callback(self):
        # self.getParameters()
        if self.layerChannelName == "Blue":
            if not self.redChannel.hasLabels() or not self.greenChannel.hasLabels():
                self.status_box.append("Label cells before counting cells")
                return
            if not self.layersChannel.hasLayers():
                self.status_box.append('All cells assumed to be in layer 1 (press "Add Layers")')
        elif 'b' in self.detectionChannels:
            if not self.redChannel.hasLabels() or not self.greenChannel.hasLabels() or not self.blueChannel.hasLabels():
                self.status_box.append("Label cells before counting cells")
                return
            if not self.layersChannel.hasLayers():
                self.status_box.append('All cells assumed to be in layer 1 (press "Add Layers")')
        elif self.layerChannelName != "Blue":  # can change
            if not self.redChannel.hasLabels() or not self.greenChannel.hasLabels():
                self.status_box.append("Label cells before counting cells")
                return
            if not self.layersChannel.hasLayers():
                self.status_box.append('All cells assumed to be in layer 1 (press "Add Layers")')

        result_text = self.resultChannel.countCells(self.countAllCombos)
        self.status_box.append(result_text)

    def expressionTest_callback(self):
        if self.reporterChannel == 'red':
            self.expressionLevelAvg, self.expressionLevelArray = self.redChannel.findCellsPixelValue(self.redImg)
        elif self.reporterChannel  == 'green':
            self.expressionLevelAvg, self.expressionLevelArray = self.greenChannel.findCellsPixelValue(self.greenImg)
        elif self.reporterChannel == 'blue':
            self.expressionLevelAvg, self.expressionLevelArray = self.blueChannel.findCellsPixelValue(self.blueImg)

        self.status_box.append('Expression Level Average: ')
        self.status_box.append(str(self.expressionLevelAvg))

    def threshold_slider_callback(self, value):
        self.threshold = value / 100
        self.threshold_label.setText("Detection Threshold: {}".format(self.threshold))

    def min_slider_callback(self, value):
        self.minSize = value
        self.min_label.setText("Minimum Cell Size: {}".format(self.minSize))

    def max_slider_callback(self, value):
        self.maxSize = value
        self.max_label.setText("Maximum Cell Size: {}".format(self.maxSize))

    def tempsize_slider_callback(self, value):
        self.tempsize = value
        self.tempsize_label.setText("Template Size: {}".format(self.tempsize))

    def variance_entry_callback(self):
        self.variance = float(self.variance_entry.text())
        self.variance_label.setText("Template Variance: {}".format(self.variance))

    def showhidelabels_button_callback(self, state):
        channel = self.channels[self.current_tab]
        if isinstance(channel, DetectionChannel):
            if state:
                channel.label_img_item.setVisible(True)
            else:
                channel.label_img_item.setVisible(False)

    def showhidebg_button_callback(self, state):
        if state:
            self.channels[self.current_tab].showbg()
        else:
            self.channels[self.current_tab].hidebg()

    def showhidedapi_button_callback(self, state):
        if state:
            self.channels[self.current_tab].showDapi()
        else:
            self.channels[self.current_tab].hideDapi()

    def showhidecells_button_callback(self, state):
        if state:
            self.channels[self.current_tab].showCells()
        else:
            self.channels[self.current_tab].hideCells()

    def brushsize_slider_callback(self, value):
        self.brushsize = value
        self.brushsize_label.setText("Brush Size: {}".format(self.brushsize))
        self.channels[self.current_tab].set_brushsize(value)
