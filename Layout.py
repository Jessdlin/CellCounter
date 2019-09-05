from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ColorChannel import Channel, DetectionChannel, ResultsChannel, LayerChannel

class Mixin:
    def setup(self):
        self.first_page = QWidget()
        self.detection_page = QWidget()
        self.meta_page = QWidget()

        self.one_page()

        self.stacked_pages = QStackedWidget(self)

        self.stacked_pages.addWidget(self.first_page)
        self.stacked_pages.addWidget(self.meta_page)
        self.stacked_pages.addWidget(self.detection_page)

        hbox = QSplitter()
        hbox.addWidget(self.stacked_pages)

        self.setCentralWidget(hbox)

        self.setWindowTitle("Cell Counter 2000")
        self.setGeometry(0, 0, 1500, self.minimumHeight())

        self.show()


    def one_page(self):
        one_layout = QHBoxLayout()
        right_box = QGroupBox("Settings")
        one_layout.addWidget(right_box)
        right_layout = QVBoxLayout()
        right_box.setLayout(right_layout)

        sub_top_box = QGroupBox("Image Description")
        right_layout.addWidget(sub_top_box)
        sub_top_layout = QVBoxLayout()
        sub_top_box.setLayout(sub_top_layout)

        sub_layout_1 = QHBoxLayout()
        sub_layout_2 = QHBoxLayout()
        sub_layout_3 = QHBoxLayout()

        detection_channels_label = QLabel('Choose cell detection color channels and add color channel label: ')
        self.red_dc = QCheckBox("Red")
        self.red_dc_label = QLineEdit()
        self.green_dc = QCheckBox("Green")
        self.green_dc_label = QLineEdit()
        self.blue_dc = QCheckBox("Blue")
        self.blue_dc_label = QLineEdit()

        detection_channels_label_r = QLabel('Choose reporter color channel')
        self.red_dc_r = QCheckBox("Red")
        self.green_dc_r = QCheckBox("Green")
        self.blue_dc_r = QCheckBox("Blue")

        layers_channel_label = QLabel("Choose layers color channel: ")
        self.red_lc = QCheckBox("Red")
        self.green_lc = QCheckBox("Green")
        self.blue_lc = QCheckBox("Blue")
        self.separate_lc = QCheckBox("Separate Dapi Image")

        sub_layout_1.addWidget(self.red_dc)
        sub_layout_1.addWidget(self.red_dc_label)
        sub_layout_1.addWidget(self.green_dc)
        sub_layout_1.addWidget(self.green_dc_label)
        sub_layout_1.addWidget(self.blue_dc)
        sub_layout_1.addWidget(self.blue_dc_label)

        sub_layout_2.addWidget(self.red_lc)
        sub_layout_2.addWidget(self.green_lc)
        sub_layout_2.addWidget(self.blue_lc)
        sub_layout_2.addWidget(self.separate_lc)

        sub_layout_3.addWidget(self.red_dc_r)
        sub_layout_3.addWidget(self.green_dc_r)
        sub_layout_3.addWidget(self.blue_dc_r)

        sub_top_layout.addWidget(detection_channels_label)
        sub_top_layout.addLayout(sub_layout_1)
        sub_top_layout.addWidget(detection_channels_label_r)
        sub_top_layout.addLayout(sub_layout_3)
        sub_top_layout.addWidget(layers_channel_label)
        sub_top_layout.addLayout(sub_layout_2)

        meta_data_label = QLabel("Do imported images contain metadata?")
        self.meta_data_cb = QCheckBox("Check if yes")
        sub_top_layout.addWidget(meta_data_label)
        sub_top_layout.addWidget(self.meta_data_cb)

        dapi_show_label = QLabel("Do you want to see Dapi while counting?")
        self.dapi_show_cb = QCheckBox("Check if yes")
        sub_top_layout.addWidget(dapi_show_label)
        sub_top_layout.addWidget(self.dapi_show_cb)

        sub_mid_box = QGroupBox("Number of Layers")
        right_layout.addWidget(sub_mid_box)
        sub_mid_layout = QHBoxLayout()
        sub_mid_box.setLayout(sub_mid_layout)

        numLayers_label = QLabel("Enter Number of Layers")
        self.numLayers_tb = QLineEdit()

        sub_mid_layout.addWidget(numLayers_label)
        sub_mid_layout.addWidget(self.numLayers_tb)

        sub_bottom_box = QGroupBox("Colocalization")
        right_layout.addWidget(sub_bottom_box)
        sub_bottom_layout = QHBoxLayout()
        sub_bottom_box.setLayout(sub_bottom_layout)

        combo_label = QLabel("Check to Count All Combinations: ")
        self.combo_checkBox = QCheckBox('Note: Do not click unless have red, green, and blue detection channels')

        sub_bottom_layout.addWidget(combo_label)
        sub_bottom_layout.addWidget(self.combo_checkBox)

        self.submit_button = QPushButton('submit')
        right_layout.addWidget(self.submit_button)

        bottom_space_box = QGroupBox(" ")
        right_layout.addWidget(bottom_space_box)
        bottom_space_layout = QHBoxLayout()
        bottom_space_box.setLayout(bottom_space_layout)
        empty_space = QLabel("                                                         ")
        bottom_space_layout.addWidget(empty_space)

        one_layout.addWidget(empty_space)
        one_layout.addWidget(empty_space)
        one_layout.addWidget(empty_space)

        self.first_page.setLayout(one_layout)

        # connect
        self.red_dc.stateChanged.connect(self.red_dc_callback)
        self.green_dc.stateChanged.connect(self.green_dc_callback)
        self.blue_dc.stateChanged.connect(self.blue_dc_callback)

        self.red_dc_r.stateChanged.connect(self.red_dc_r_callback)
        self.green_dc_r.stateChanged.connect(self.green_dc_r_callback)
        self.blue_dc_r.stateChanged.connect(self.blue_dc_r_callback)

        self.red_lc.stateChanged.connect(self.red_lc_callback)
        self.green_lc.stateChanged.connect(self.green_lc_callback)
        self.blue_lc.stateChanged.connect(self.blue_lc_callback)
        self.separate_lc.stateChanged.connect(self.separate_lc_callback)

        self.meta_data_cb.stateChanged.connect(self.meta_data_callback)
        self.dapi_show_cb.stateChanged.connect(self.dapi_show_callback)

        self.combo_checkBox.stateChanged.connect(self.combo_callback)

        self.submit_button.pressed.connect(self.submit_button_callback)

    def red_dc_callback(self, state):
        if state:
            self.detectionChannels.append('r')
        else:
            self.detectionChannels.remove('r')

    def green_dc_callback(self, state):
        if state:
            self.detectionChannels.append('g')
        else:
            self.detectionChannels.remove('g')

    def blue_dc_callback(self, state):
        if state:
            self.detectionChannels.append('b')
        else:
            self.detectionChannels.remove('b')

    def red_dc_r_callback(self, state):
        if state:
            self.green_dc_r.setCheckable(False)
            self.blue_dc_r.setCheckable(False)
            self.reporterChannel = 'red'
        else:
            self.green_dc_r.setCheckable(True)
            self.blue_dc_r.setCheckable(True)

    def green_dc_r_callback(self, state):
        if state:
            self.red_dc_r.setCheckable(False)
            self.blue_dc_r.setCheckable(False)
            self.reporterChannel = 'green'

        else:
            self.red_dc_r.setCheckable(True)
            self.blue_dc_r.setCheckable(True)

    def blue_dc_r_callback(self, state):
        if state:
            self.red_dc_r.setCheckable(False)
            self.green_dc_r.setCheckable(False)
            self.reporterChannel = 'blue'

        else:
            self.red_dc_r.setCheckable(True)
            self.green_dc_r.setCheckable(True)

    def red_lc_callback(self, state):
        if state:
            self.green_lc.setCheckable(False)
            self.blue_lc.setCheckable(False)
            self.separate_lc.setCheckable(False)
            self.layerChannelName = "Red"
        else:
            self.green_lc.setCheckable(True)
            self.blue_lc.setCheckable(True)
            self.separate_lc.setCheckable(True)

    def green_lc_callback(self, state):
        if state:
            self.red_lc.setCheckable(False)
            self.blue_lc.setCheckable(False)
            self.separate_lc.setCheckable(False)
            self.layerChannelName = "Green"
        else:
            self.red_lc.setCheckable(True)
            self.blue_lc.setCheckable(True)
            self.separate_lc.setCheckable(True)

    def blue_lc_callback(self, state):
        if state:
            self.green_lc.setCheckable(False)
            self.red_lc.setCheckable(False)
            self.separate_lc.setCheckable(False)
            self.layerChannelName = "Blue"
        else:
            self.green_lc.setCheckable(True)
            self.red_lc.setCheckable(True)
            self.separate_lc.setCheckable(True)

    def separate_lc_callback(self, state):
        if state:
            self.green_lc.setCheckable(False)
            self.blue_lc.setCheckable(False)
            self.red_lc.setCheckable(False)
            self.layerChannelName = "Separate"
        else:
            self.green_lc.setCheckable(True)
            self.blue_lc.setCheckable(True)
            self.red_lc.setCheckable(True)

    def meta_data_callback(self, state):
        if state:
            self.contains_meta_data = True
        else:
            self.contains_meta_data = False

    def dapi_show_callback(self, state):
        if state:
            self.show_Dapi = True
            self.n_dim = 3
        else:
            self.show_Dapi = False
            self.n_dim = 2

    def combo_callback(self, state):
        if state:
            self.countAllCombos = True
        else:
            self.countAllCombos = False

    def submit_button_callback(self):
        redChannel_label = self.red_dc_label.text()
        greenChannel_label = self.green_dc_label.text()
        blueChannel_label = self.blue_dc_label.text()
        self.numLayers = int(self.numLayers_tb.text()) - 1
        if 'r' in self.detectionChannels:
            if len(redChannel_label) > 0:
                self.detectionChannels_labels.append(redChannel_label)
            else:
                self.detectionChannels_labels.append('red')
        if 'g' in self.detectionChannels:
            if len(greenChannel_label) > 0:
                self.detectionChannels_labels.append(greenChannel_label)
            else:
                self.detectionChannels_labels.append('green')
        if 'b' in self.detectionChannels:
            if len(blueChannel_label) > 0:
                self.detectionChannels_labels.append(blueChannel_label)
            else:
                self.detectionChannels_labels.append('blue')
        if self.contains_meta_data:
            self.m_page()
            self.stacked_pages.setCurrentWidget(self.meta_page)
        else:
            self.d_page()
            self.stacked_pages.setCurrentWidget(self.detection_page)

    def m_page(self):
        m_layout = QVBoxLayout()
        if 'r' in self.detectionChannels:
            rLayout = QHBoxLayout()
            m_layout.addLayout(rLayout)
            rname_label = QLabel('Red Labels Image Path:')
            self.rfname_entry = QLineEdit()
            rbrowse_button = QPushButton('Browse')
            rLayout.addWidget(rname_label)
            rLayout.addWidget(self.rfname_entry)
            rLayout.addWidget(rbrowse_button)
            rbrowse_button.pressed.connect(self.rbrowse_button_callback)
        if 'g' in self.detectionChannels:
            gLayout = QHBoxLayout()
            m_layout.addLayout(gLayout)
            gname_label = QLabel('Green Labels Image Path:')
            self.gfname_entry = QLineEdit()
            gbrowse_button = QPushButton('Browse')
            gLayout.addWidget(gname_label)
            gLayout.addWidget(self.gfname_entry)
            gLayout.addWidget(gbrowse_button)
            gbrowse_button.pressed.connect(self.gbrowse_button_callback)
        if 'b' in self.detectionChannels:
            bLayout = QHBoxLayout()
            m_layout.addLayout(bLayout)
            bname_label = QLabel('Blue Labels Image Path:')
            self.bfname_entry = QLineEdit()
            bbrowse_button = QPushButton('Browse')
            bLayout.addWidget(bname_label)
            bLayout.addWidget(self.bfname_entry)
            bLayout.addWidget(bbrowse_button)
            bbrowse_button.pressed.connect(self.bbrowse_button_callback)

        self.m_submit_button = QPushButton('submit')
        m_layout.addWidget(self.m_submit_button)
        self.meta_page.setLayout(m_layout)
        self.m_submit_button.pressed.connect(self.m_submit_button_callback)

    def m_submit_button_callback(self):
        self.d_page()
        self.stacked_pages.setCurrentWidget(self.detection_page)

    def d_page(self):

        # %% Layouts
        toplevel_layout = QVBoxLayout()
        hlayout_top1 = QHBoxLayout()
        hlayout_top2 = QHBoxLayout()
        hlayout_top3 = QHBoxLayout()
        hlayout_bottom = QSplitter()
        bottom_right_layout = QVBoxLayout()
        bottom_right = QWidget()
        bottom_right.setLayout(bottom_right_layout)
        tabs = QTabWidget(tabPosition=QTabWidget.East, tabShape=QTabWidget.Rounded)

        toplevel_layout.addLayout(hlayout_top1)
        toplevel_layout.addLayout(hlayout_top2)
        toplevel_layout.addLayout(hlayout_top3)
        # hlayout_bottom.addWidget(bottom_right)
        hlayout_bottom.addWidget(tabs)
        # print(hlayout_bottom.indexOf(tabs))
        hlayout_bottom.addWidget(bottom_right)
        # print(hlayout_bottom.indexOf(bottom_right))
        hlayout_bottom.setCollapsible(0, False)
        hlayout_bottom.setCollapsible(1, False)
        hlayout_bottom.setSizes([1499, 1])

        toplevel_layout.addWidget(hlayout_bottom)
        self.detection_page.setLayout(toplevel_layout)

        # %% File Selection
        fname_label = QLabel('Image Path:')
        self.fname_entry = QLineEdit()
        browse_button = QPushButton('Browse')
        hlayout_top2.addWidget(fname_label)
        hlayout_top2.addWidget(self.fname_entry)
        hlayout_top2.addWidget(browse_button)

        if self.layerChannelName == "Separate":
            fname_label_dapi = QLabel('Dapi Path:')
            self.fname_entry_dapi = QLineEdit()
            browse_button_dapi = QPushButton('Browse')
            hlayout_top1.addWidget(fname_label_dapi)
            hlayout_top1.addWidget(self.fname_entry_dapi)
            hlayout_top1.addWidget(browse_button_dapi)

        export_label = QLabel('Export Directory:')
        self.export_entry = QLineEdit()
        browse_export_button = QPushButton('Browse')
        hlayout_top3.addWidget(export_label)
        hlayout_top3.addWidget(self.export_entry)
        hlayout_top3.addWidget(browse_export_button)

        # %% TABS
        # red tab
        redTab = QWidget()
        tabs.addTab(redTab, "Red")
        self.redChannel = DetectionChannel(redTab, 'r', self.n_dim, name="Red")
        self.Tabs['red'] = 0
        self.channels.append(self.redChannel)
        self.dChannels.append(self.redChannel)
        # green tab
        greenTab = QWidget()
        tabs.addTab(greenTab, "Green")
        self.greenChannel = DetectionChannel(greenTab, 'g', self.n_dim, name="Green")
        self.Tabs['green'] = 1
        self.channels.append(self.greenChannel)
        self.dChannels.append(self.greenChannel)
        # blue tab/Layers
        if self.layerChannelName == "Blue":
            blueTab = QWidget()
            tabs.addTab(blueTab, "Layers")
            self.layersChannel = LayerChannel(blueTab, 'b', 2, name="Layers")
            self.Tabs['blue'] = 2
            self.Tabs['results'] = 3
            self.channels.append(self.layersChannel)
        elif 'b' in self.detectionChannels:
            blueTab = QWidget()
            tabs.addTab(blueTab, "Blue")
            self.blueChannel = DetectionChannel(blueTab, 'b', self.n_dim, name="Blue")
            self.Tabs['blue'] = 2
            self.channels.append(self.blueChannel)
            self.dChannels.append(self.blueChannel)
        # layer tab
        if self.layerChannelName != "Blue":
            layersTab = QWidget()
            tabs.addTab(layersTab, "Layers")
            self.layersChannel = LayerChannel(layersTab, 'w', 2, name="Layers")
            self.channels.append(self.layersChannel)
            if self.layerChannelName == "Separate":
                self.Tabs['layers'] = 3
                self.Tabs['results'] = 4
            else:
                self.Tabs['layers'] = 2
                self.Tabs['results'] = 3
        colocTab = QWidget()
        tabs.addTab(colocTab, "Colocalization")
        # if self.addLayersBlue or self.addBlueChannel == False:
        #    self.resultChannel = ResultsChannel(colocTab, 'y', [self.redChannel, self.greenChannel], name="Coloc")
        # else:
        #     self.resultChannel = ResultsChannel(colocTab, 'y', [self.redChannel, self.greenChannel, self.blueChannel], name="Coloc")
        self.resultChannel = ResultsChannel(colocTab, 'y', self.dChannels, name="Coloc")
        self.channels.append(self.resultChannel)

        # %% CONTROL PANEL
        # run / count buttons
        runControlBox = QGroupBox("Detect / Count / Export")
        bottom_right_layout.addWidget(runControlBox)
        runControlLayout = QVBoxLayout()
        runControlBox.setLayout(runControlLayout)
        # run button
        self.run_button = QPushButton("Detect", enabled=False)
        runControlLayout.addWidget(self.run_button)
        # count button
        count_button = QPushButton("Count Cells")
        runControlLayout.addWidget(count_button)

        #expression test
        if self.reporterChannel != None:
            self.expressionTest_button = QPushButton("Calculate Expression Strength", enabled=False)
            runControlLayout.addWidget(self.expressionTest_button)

        # export button
        export_button = QPushButton("Export")
        runControlLayout.addWidget(export_button)

        # view/edit control box
        viewControlBox = QGroupBox("View / Edit Options")
        bottom_right_layout.addWidget(viewControlBox)
        viewLayout = QVBoxLayout()
        viewControlBox.setLayout(viewLayout)

        # show/hide
        self.showhidelabels_button = QCheckBox("Show Labels")
        self.showhidelabels_button.setChecked(True)
        viewLayout.addWidget(self.showhidelabels_button)
        self.showhidebg_button = QCheckBox("Show Background")
        self.showhidebg_button.setChecked(True)
        viewLayout.addWidget(self.showhidebg_button)
        if self.show_Dapi:
            self.showhidedapi_button = QCheckBox("Show Dapi")
            self.showhidedapi_button.setChecked(True)
            viewLayout.addWidget(self.showhidedapi_button)
            self.showhidecells_button = QCheckBox("Show Cells")
            self.showhidecells_button.setChecked(True)
            viewLayout.addWidget(self.showhidecells_button)

        # brush size slider
        self.brushsize_label = QLabel("Brush Size: {}".format(self.brushsize))
        viewLayout.addWidget(self.brushsize_label)
        brushsize_slider = QSlider(Qt.Horizontal)
        brushsize_slider.setMinimum(1)
        brushsize_slider.setMaximum(50)
        brushsize_slider.setTickInterval(1)
        brushsize_slider.setSliderPosition(self.brushsize)
        viewLayout.addWidget(brushsize_slider)
        # single click label/unlabel

        # algorithm control box
        detectionControlBox = QGroupBox("Detection Options")
        bottom_right_layout.addWidget(detectionControlBox)
        detectionLayout = QVBoxLayout()
        detectionControlBox.setLayout(detectionLayout)
        # threshold slider
        self.threshold_label = QLabel("Detection Threshold: {}".format(self.threshold))
        detectionLayout.addWidget(self.threshold_label)
        threshold_slider = QSlider(Qt.Horizontal)
        threshold_slider.setMinimum(0)
        threshold_slider.setMaximum(100)
        threshold_slider.setTickInterval(1)
        threshold_slider.setSliderPosition(20)
        detectionLayout.addWidget(threshold_slider)
        # minimum slider
        self.min_label = QLabel("Minimum Cell Size: {}".format(self.minSize))
        detectionLayout.addWidget(self.min_label)
        min_slider = QSlider(Qt.Horizontal)
        min_slider.setMinimum(0)
        min_slider.setMaximum(100)
        min_slider.setTickInterval(1)
        min_slider.setSliderPosition(10)
        detectionLayout.addWidget(min_slider)
        # maximum slider
        self.max_label = QLabel("Maximum Cell Size: {}".format(self.maxSize))
        detectionLayout.addWidget(self.max_label)
        max_slider = QSlider(Qt.Horizontal)
        max_slider.setMinimum(100)
        max_slider.setMaximum(1000)
        max_slider.setTickInterval(20)
        max_slider.setSliderPosition(200)
        detectionLayout.addWidget(max_slider)
        # template size
        self.tempsize_label = QLabel("Template Size: {}".format(self.tempsize))
        detectionLayout.addWidget(self.tempsize_label)
        tempsize_slider = QSlider(Qt.Horizontal)
        tempsize_slider.setMinimum(1)
        tempsize_slider.setMaximum(100)
        tempsize_slider.setTickInterval(1)
        tempsize_slider.setSliderPosition(10)
        detectionLayout.addWidget(tempsize_slider)
        # template variance
        self.variance_label = QLabel("Template Variance: {}".format(self.variance))
        detectionLayout.addWidget(self.variance_label)
        self.variance_entry = QLineEdit()
        detectionLayout.addWidget(self.variance_entry)

        # remove horizontal noise checkbox
        # add layers button
        self.layer_button = QPushButton("Add Layers", enabled=False)
        detectionLayout.addWidget(self.layer_button)

        statusBox = QGroupBox("Status")
        bottom_right_layout.addWidget(statusBox)
        statusLayout = QVBoxLayout()
        statusBox.setLayout(statusLayout)
        # add status window
        self.status_box = QTextEdit(readOnly=True)
        statusLayout.addWidget(self.status_box)

        browse_button.pressed.connect(self.browse_button_callback)
        if self.layerChannelName == "Separate":
            browse_button_dapi.pressed.connect(self.browse_button_dapi_callback)
        browse_export_button.pressed.connect(self.browse_export_button_callback)
        export_button.pressed.connect(self.export_button_callback)
        self.showhidelabels_button.stateChanged.connect(self.showhidelabels_button_callback)
        self.showhidebg_button.stateChanged.connect(self.showhidebg_button_callback)
        if self.show_Dapi:
            self.showhidedapi_button.stateChanged.connect(self.showhidedapi_button_callback)
            self.showhidecells_button.stateChanged.connect(self.showhidecells_button_callback)
        brushsize_slider.valueChanged.connect(self.brushsize_slider_callback)
        threshold_slider.valueChanged.connect(self.threshold_slider_callback)
        min_slider.valueChanged.connect(self.min_slider_callback)
        max_slider.valueChanged.connect(self.max_slider_callback)
        tempsize_slider.valueChanged.connect(self.tempsize_slider_callback)
        self.variance_entry.returnPressed.connect(self.variance_entry_callback)
        self.run_button.pressed.connect(self.run_button_callback)
        count_button.pressed.connect(self.count_button_callback)
        self.layer_button.pressed.connect(self.layer_button_callback)
        tabs.currentChanged.connect(self.tab_changed_callback)
        if self.reporterChannel != None:
            self.expressionTest_button.pressed.connect(self.expressionTest_callback)

        # self.setWindowTitle("Cell Counter 2000")
        # self.setGeometry(100,100,1280,960)
        # self.show()
        a, b = hlayout_bottom.sizes()
        hlayout_bottom.setSizes([.8 * (a + b), .2 * (a + b)])

    # def display(self, i):
    # self.stacked_pages.setCurrentIndex(i)
