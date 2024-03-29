import Layout
import Callbacks
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg

# Base PyQtGraph configuration
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


class CellCounterApp(QMainWindow, Layout.Mixin, Callbacks.Mixin):

    def __init__(self, *args, **kwargs):
        super(CellCounterApp, self).__init__(*args, **kwargs)

        self.current_tab = 0
        self.threshold = .12
        self.opacity = .75
        self.brushsize = 10
        self.tempsize = 10
        self.variance = 4
        self.minSize = 10
        self.maxSize = 200
        self.showCells = True
        self.blueImg = None
        self.greenImg = None
        self.redImg = None
        self.layerlinesB = None
        self.cell_counts = None
        self.addLayersBlue = False
        self.countBlue = False
        self.addBlueChannel = True
        self.addLayersTab = False
        self.artificalLayerChannel = None
        self.layerChannelName = None
        self.channels = []
        self.seperateDapiFile = False
        self.artificalLayerChannel = None
        self.blueChannelStatus = None
        self.numLayers = 0
        self.detectionChannels = []
        self.detectionChannels_labels = []
        self.reporterChannel = None
        self.expressionLevelArray = 0
        self.dChannels = []
        self.contains_meta_data = False
        self.n_dim = 2
        self.show_Dapi = False
        self.countAllCombos = False
        self.Tabs = {}
        self.setup()
