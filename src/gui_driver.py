import configparser
import sys
import os
import threading

from dandere2x import Dandere2x
from dandere2x_core.dandere2x_utils import get_valid_block_sizes
from wrappers.videosettings import VideoSettings
import subprocess

from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QWidget, QFileDialog
from gui.Dandere2xGUI import Ui_Dandere2xGUI
from PyQt5 import QtCore, QtGui, QtWidgets

import time
from context import Context


class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dandere2xGUI()
        self.ui.setupUi(self)
        self.this_folder = os.path.dirname(os.path.realpath(__file__)) + os.path.sep
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
        self.ui.waifu2x_type_combo_box.setCurrentText(_translate("Dandere2xGUI", "Waifu2x-Vulkan"))
        #self.ui.video_icon.setPixmap(QtGui.QPixmap("assets\\aka.png"))

        self.config_buttons()
        self.refresh_scale_factor()
        self.show()


    # Setup connections for each button
    def config_buttons(self):
        self.ui.select_video_button.clicked.connect(self.press_select_video_button)
        self.ui.select_workspace_button.clicked.connect(self.press_select_workspace_button)
        self.ui.upscale_button.clicked.connect(self.press_upscale_button)
        self.ui.waifu2x_type_combo_box.currentIndexChanged.connect(self.refresh_scale_factor)


    # if vulkan is enabled, we cant do scale factor 3 or 4

    def refresh_scale_factor(self):
        if self.ui.waifu2x_type_combo_box.currentText() == 'Waifu2x-Vulkan':
            self.ui.scale_3_radio_button.setEnabled(False)
            self.ui.scale_4_radio_button.setEnabled(False)
        else:
            self.ui.scale_3_radio_button.setEnabled(True)
            self.ui.scale_4_radio_button.setEnabled(True)

    def press_upscale_button(self):
        
        self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
        self.ui.upscale_status_label.setText("Upscaling in Progress")

        self.parse_gui_inputs()

        config = configparser.ConfigParser()
        config.read('gui_config.ini')
        config.set("dandere2x", "workspace", self.workspace_dir)
        config.set("dandere2x", "file_dir", self.file_dir)
        config.set("dandere2x", "block_size", self.block_size)
        config.set("dandere2x", "quality_low", self.image_quality)
        config.set("dandere2x", "waifu2x_type", self.waifu2x_type)
        config.set("dandere2x", "scale_factor", self.scale_factor)

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
            self.ui.upscale_status_label.setText("Upscale Failed. See log")



    # Parse everything we need from the GUI into a dandere2x friendly format
    # Leave everything as STR's since config files are just strings
    def parse_gui_inputs(self):


        self.workspace_dir = self.workspace_dir.replace("/", "\\") + "\\"
        self.file_dir = self.file_dir.replace("/", "\\")

        # Scale Factors

        if self.ui.scale_1_radio_button.isChecked():
            self.scale_factor = '1'

        if self.ui.scale_2_radio_button.isChecked():
            self.scale_factor = '2'

        if self.ui.scale_3_radio_button.isChecked():
            self.scale_factor = '3'

        if self.ui.scale_4_radio_button.isChecked():
            self.scale_factor = '4'

        # Noise factors

        if self.ui.noise_0_radio_button.isChecked():
            self.noise_level = '0'

        if self.ui.noise_1_radio_button.isChecked():
            self.noise_level = '1'

        if self.ui.noise_2_radio_button.isChecked():
            self.noise_level = '2'

        if self.ui.noise_3_radio_button.isChecked():
            self.noise_level = '3'

        # Dandere2x Settings
        self.image_quality = self.ui.image_quality_box.currentText()
        self.block_size = self.ui.block_size_combo_box.currentText()


        # Waifu2x Type
        if self.ui.waifu2x_type_combo_box.currentText() == 'Waifu2x-Caffe':
            self.waifu2x_type = 'caffe'

        if self.ui.waifu2x_type_combo_box.currentText() == 'Waifu2x-Vulkan':
            self.waifu2x_type = 'vulkan'

        if self.ui.waifu2x_type_combo_box.currentText() == 'Waifu2x-Converter-Cpp':
            self.waifu2x_type = 'conv'

    def press_select_video_button(self):

        self.file_dir = self.load_file()[0]

        if self.file_dir == '':
            return

        path, name = os.path.split(self.file_dir)

        self.ui.video_label.setText(name)
        self.ui.video_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))

        config = configparser.ConfigParser()
        config.read('gui_config.ini')
        context = Context(config)

        videosettings = VideoSettings(context.ffprobe_dir, self.file_dir)

        valid_list = get_valid_block_sizes(videosettings.height, videosettings.width)

        self.ui.block_size_combo_box.clear()
        self.ui.block_size_combo_box.addItems(valid_list)
        self.ui.block_size_combo_box.setEnabled(True)
        self.ui.block_size_combo_box.setCurrentIndex(len(valid_list) / 1.5) #put the middle most to avoid confusion

        if self.file_dir != '' and self.workspace_dir != '':
            self.ui.upscale_button.setEnabled(True)
            self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
            self.ui.upscale_status_label.setText("Ready to upscale!")

    def press_select_workspace_button(self):

        self.workspace_dir = self.load_dir()

        if self.workspace_dir == '':
            return

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
        filename = QFileDialog.getExistingDirectory(w, 'Open Directory', self.this_folder)
        return filename

    def load_file(self):
        self.ui.w = QWidget()

        # Set window size.
        self.ui.w.resize(320, 240)
        filename = QFileDialog.getOpenFileName(w, 'Open File', self.this_folder)
        return filename


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())