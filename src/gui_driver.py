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
import json

class AppWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dandere2xGUI()
        self.ui.setupUi(self)


        # load 'this folder' in a pyinstaller friendly way
        self.this_folder = ''
        if getattr(sys, 'frozen', False):
            self.this_folder = os.path.dirname(sys.executable) + os.path.sep
        elif __file__:
            self.this_folder = os.path.dirname(__file__) + os.path.sep

        self.file_dir = ''
        self.workspace_dir = ''
        self.scale_factor = None
        self.noise_level = None
        self.image_quality = None
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

        with open("dandere2x.json", "r") as read_file:
            config_json = json.load(read_file)

        config_json['dandere2x']['workspace'] = self.workspace_dir
        config_json['dandere2x']['file_dir'] = self.file_dir
        config_json['dandere2x']['block_size'] = self.block_size
        config_json['dandere2x']['quality_low'] = self.image_quality
        config_json['dandere2x']['waifu2x_type'] = self.waifu2x_type
        config_json['dandere2x']['scale_factor'] = self.scale_factor

        with open('jsondump.json', 'w') as outfile:
            json.dump(config_json, outfile)


        print("workspace = " + self.workspace_dir)
        print("file_dir = " + self.file_dir)
        print("block_size = " + str(self.block_size))
        print("quality_low = " + str(self.image_quality))
        print("waifu2x_type = " + self.waifu2x_type)

        context = Context(config_json)
        d = Dandere2x(context)
     #   d.run_concurrent()

        try:
            d.run_concurrent()
        except:
            print("Oops!", sys.exc_info()[0], "occured.")
            self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
            self.ui.upscale_status_label.setText("Upscale Failed. See log")



    # Parse everything we need from the GUI into a dandere2x friendly format
    # Leave everything as STR's since config files are just strings
    def parse_gui_inputs(self):


        self.workspace_dir = self.workspace_dir.replace("/", "\\") + "\\"
        self.file_dir = self.file_dir.replace("/", "\\")

        # Scale Factors

        if self.ui.scale_1_radio_button.isChecked():
            self.scale_factor = 1

        if self.ui.scale_2_radio_button.isChecked():
            self.scale_factor = 2

        if self.ui.scale_3_radio_button.isChecked():
            self.scale_factor = 3

        if self.ui.scale_4_radio_button.isChecked():
            self.scale_factor = 4

        # Noise factors

        if self.ui.noise_0_radio_button.isChecked():
            self.noise_level = 0

        if self.ui.noise_1_radio_button.isChecked():
            self.noise_level = 1

        if self.ui.noise_2_radio_button.isChecked():
            self.noise_level = 2

        if self.ui.noise_3_radio_button.isChecked():
            self.noise_level = 3

        # Dandere2x Settings
        self.image_quality = int(self.ui.image_quality_box.currentText())
        self.block_size = int(self.ui.block_size_combo_box.currentText())


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

        # set the video label to the selected file name
        self.ui.video_label.setText(name)
        self.ui.video_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))


        with open("dandere2x.json", "r") as read_file:
            config_json = json.load(read_file)

        ffprobe_path = os.path.join(config_json['ffmpeg']['ffmpeg_path'], "ffprobe.exe")
        # load the needed video settings for the GUI
        videosettings = VideoSettings(ffprobe_path, self.file_dir)

        # Get a list of valid list block sizes knowing the width and height
        valid_list_blocksize = get_valid_block_sizes(videosettings.height, videosettings.width)

        self.ui.block_size_combo_box.clear()
        self.ui.block_size_combo_box.addItems(valid_list_blocksize)
        self.ui.block_size_combo_box.setEnabled(True)
        self.ui.block_size_combo_box.setCurrentIndex(len(valid_list_blocksize) / 1.5) # Put the blocksize to be in the middleish
                                                                            # to avoid users leaving it as '1'

        # allow user to upscale if two conditions are met
        if self.file_dir != '' and self.workspace_dir != '':
            self.ui.upscale_button.setEnabled(True)
            self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
            self.ui.upscale_status_label.setText("Ready to upscale!")



    def press_select_workspace_button(self):

        self.workspace_dir = self.load_dir()

        # If the user didn't select anything, don't continue or it'll break
        # Everything
        if self.workspace_dir == '':
            return

        # set the label to only display the last 20 elements of the selected workspace
        start_val = len(self.workspace_dir) - 20
        if(start_val < 0):
            start_val = 0

        self.ui.workspace_label.setText(".." + self.workspace_dir[start_val :  len(self.workspace_dir)])
        self.ui.workspace_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))

        # allow user to upscale if two conditions are met
        if self.file_dir != '' and self.workspace_dir != '':
            self.ui.upscale_button.setEnabled(True)
            self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
            self.ui.upscale_status_label.setText("Ready to upscale!")

    def load_dir(self):
        self.ui.w = QWidget()

        self.ui.w.resize(320, 240)
        filename = QFileDialog.getExistingDirectory(w, 'Open Directory', self.this_folder)
        return filename

    def load_file(self):
        self.ui.w = QWidget()

        self.ui.w.resize(320, 240)
        filename = QFileDialog.getOpenFileName(w, 'Open File', self.this_folder)
        return filename


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())