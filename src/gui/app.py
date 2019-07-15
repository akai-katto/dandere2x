import configparser
import sys
import os
import threading

from dandere2x import Dandere2x
from dandere2x_core.dandere2x_utils import get_valid_block_sizes
from wrappers.videosettings import VideoSettings
import subprocess

from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QFileDialog
from Dandere2xGUI import Ui_Dandere2xGUI
from PyQt5 import QtCore, QtGui, QtWidgets

import time


class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dandere2xGUI()
        self.ui.setupUi(self)

        self.file_dir = ''
        self.workspace_dir = ''
        self.scale_factor = ''
        self.noise_level = ''
        self.image_quality = ''
        self.block_size = ''
        self.waifu2x_type = ''

        # theres a bug with qt designer and '80' for default quality needs to be set elsewhere
        _translate = QtCore.QCoreApplication.translate
        self.ui.image_quality_box.setCurrentText(_translate("Dandere2xGUI", "70"))
        #self.ui.video_icon.setPixmap(QtGui.QPixmap("assets\\aka.png"))

        self.config_buttons()
        self.show()


    # Setup connections for each button
    def config_buttons(self):
        self.ui.select_video_button.clicked.connect(self.press_select_video_button)
        self.ui.select_workspace_button.clicked.connect(self.press_select_workspace_button)
        self.ui.upscale_button.clicked.connect(self.press_upscale_button)

    def press_upscale_button(self):
        
        self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
        self.ui.upscale_status_label.setText("Upscaling in Progress")

        self.parse_gui_inputs()

        config = configparser.ConfigParser()
        config.read('C:\\Users\\windwoz\\Documents\\github_projects\\src\\config.ini')
        config.set("dandere2x", "workspace", self.workspace_dir)
        config.set("dandere2x", "file_dir", self.file_dir)
        config.set("dandere2x", "block_size", self.block_size)
        config.set("dandere2x", "quality_low", self.image_quality)
        config.set("dandere2x", "waifu2x_type", self.waifu2x_type)

        print("workspace = " + self.workspace_dir)
        print("file_dir = " + self.file_dir)
        print("block_size = " + self.block_size)
        print("quality_low = " + self.image_quality)
        print("waifu2x_type = " + self.waifu2x_type)

        d = Dandere2x(config)
     #   d.run_concurrent()

        try:
            d.run_concurrent()
        except:
            self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
            self.ui.upscale_status_label.setText("Upscale Failed")



    # Parse everything we need from the GUI into a dandere2x friendly format
    # Leave everything as STR's since config files are just strings
    def parse_gui_inputs(self):


        self.workspace_dir = self.workspace_dir.replace("/", "\\") + "\\"
        self.file_dir = self.file_dir.replace("/", "\\")

        if self.ui.scale_1_radio_button.isChecked():
            self.scale_factor = '1'

        if self.ui.scale_2_radio_button.isChecked():
            self.scale_factor = '2'

        if self.ui.scale_3_radio_button.isChecked():
            self.scale_factor = '3'

        if self.ui.scale_4_radio_button.isChecked():
            self.scale_factor = '4'

        if self.ui.noise_0_radio_button.isChecked():
            self.noise_level = '0'

        if self.ui.noise_1_radio_button.isChecked():
            self.noise_level = '1'

        if self.ui.noise_2_radio_button.isChecked():
            self.noise_level = '2'

        if self.ui.noise_3_radio_button.isChecked():
            self.noise_level = '3'

        self.image_quality = self.ui.image_quality_box.currentText()
        self.block_size = self.ui.block_size_combo_box.currentText()

        if self.ui.waifu2x_type_combo_box.currentText() == 'Waifu2x-Caffe':
            self.waifu2x_type = 'caffe'

        if self.ui.waifu2x_type_combo_box.currentText() == 'Waifu2x-Vulkan':
            self.waifu2x_type = 'vulkan'

        if self.ui.waifu2x_type_combo_box.currentText() == 'Waifu2x-Converter-Cpp':
            self.waifu2x_type = 'conv'

    def press_select_video_button(self):

        print(self.ui.image_quality_box.currentText())

        self.file_dir = self.load_file()[0]

        path, name = os.path.split(self.file_dir)

        self.ui.video_label.setText(name)
        self.ui.video_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))

        valid_list = get_valid_block_sizes(1920,1080)
        self.ui.block_size_combo_box.addItems(valid_list)
        self.ui.block_size_combo_box.setEnabled(True)
        self.ui.block_size_combo_box.setCurrentIndex(len(valid_list) / 1.5) #put the middle most to avoid confusion

        if self.file_dir != '' and self.workspace_dir != '':
            self.ui.upscale_button.setEnabled(True)
            self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
            self.ui.upscale_status_label.setText("Ready to upscale!")

    def press_select_workspace_button(self):

        self.workspace_dir = self.load_dir()

        start_val = len(self.workspace_dir) - 20
        if(start_val < 0):
            start_val = 0

        self.ui.workspace_label.setText(".." + self.workspace_dir[start_val :  len(self.workspace_dir)])
        self.ui.workspace_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))

        if self.file_dir != '' and self.workspace_dir != '':
            self.ui.upscale_button.setEnabled(True)
            self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
            self.ui.upscale_status_label.setText("Ready to upscale!")

    def load_dir(self):
        self.ui.w = QWidget()

        # Set window size.
        self.ui.w.resize(320, 240)
        filename = QFileDialog.getExistingDirectory(w, 'Open Directory', 'C:\\Users\\windwoz\\Desktop\\plz\\pythonreleases\\1.1\\demo_folder\\')
        return filename

    def load_file(self):
        self.ui.w = QWidget()

        # Set window size.
        self.ui.w.resize(320, 240)
        filename = QFileDialog.getOpenFileName(w, 'Open File', 'C:\\Users\\windwoz\\Desktop\\plz\\pythonreleases\\1.1\\demo_folder\\')
        return filename

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())