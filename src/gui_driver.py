import sys
import json
import os
import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog

from context import Context
from dandere2x import Dandere2x
from dandere2x_core.dandere2x_utils import get_valid_block_sizes
from gui.Dandere2xGUI import Ui_Dandere2xGUI
from wrappers.videosettings import VideoSettings


class QtDandere2xThread(QtCore.QThread):
    finished = QtCore.pyqtSignal()

    def __init__(self, parent, config_json):
        super(QtDandere2xThread, self).__init__(parent)
        self.config_json = config_json

    def run(self):
        context = Context(self.config_json)
        d = Dandere2x(context)
        d.run_concurrent()

        self.finished.emit()


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
        self.output_file = ''
        self.scale_factor = None
        self.noise_level = None
        self.image_quality = None
        self.block_size = ''
        self.waifu2x_type = ''

        # theres a bug with qt designer and '80' for default quality needs to be set elsewhere
        _translate = QtCore.QCoreApplication.translate
        self.ui.image_quality_box.setCurrentText(_translate("Dandere2xGUI", "75"))
        self.ui.waifu2x_type_combo_box.setCurrentText(_translate("Dandere2xGUI", "Waifu2x-Vulkan"))
        # self.ui.video_icon.setPixmap(QtGui.QPixmap("assets\\aka.png"))

        self.config_buttons()
        self.refresh_scale_factor()
        self.show()

    # Setup connections for each button
    def config_buttons(self):
        self.ui.select_video_button.clicked.connect(self.press_select_video_button)
        self.ui.select_output_button.clicked.connect(self.press_select_output_button)
        self.ui.upscale_button.clicked.connect(self.press_upscale_button)
        self.ui.waifu2x_type_combo_box.currentIndexChanged.connect(self.refresh_scale_factor)

    # if vulkan is enabled, we cant do scale factor 3 or 4

    # refresh the buttons to see if upscale can be called
    def refresh_buttons(self):
        # allow user to upscale if two output_file are met
        if self.file_dir != '' and self.output_file != '':
            self.ui.upscale_button.setEnabled(True)
            self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
            self.ui.upscale_status_label.setText("Ready to upscale!")

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

        print(os.getcwd())

        with open(os.path.join(self.this_folder, "dandere2x.json"), "r") as read_file:
            config_json = json.load(read_file)

        config_json['dandere2x']['output_file'] = self.output_file
        config_json['dandere2x']['file_dir'] = self.file_dir
        config_json['dandere2x']['block_size'] = self.block_size
        config_json['dandere2x']['quality_low'] = self.image_quality
        config_json['dandere2x']['waifu2x_type'] = self.waifu2x_type
        config_json['dandere2x']['scale_factor'] = self.scale_factor

        print("output_file = " + self.output_file)
        print("file_dir = " + self.file_dir)
        print("block_size = " + str(self.block_size))
        print("quality_low = " + str(self.image_quality))
        print("waifu2x_type = " + self.waifu2x_type)

        self.thread = QtDandere2xThread(self, config_json)
        self.thread.finished.connect(self.update)

        self.disable_buttons()

        try:
            self.thread.start()
        except:
            print("Oops!", sys.exc_info()[0], "occured.")
            self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
            self.ui.upscale_status_label.setText("Upscale Failed. See log")

    def disable_buttons(self):
        self.ui.upscale_button.setEnabled(False)
        self.ui.select_output_button.setEnabled(False)
        self.ui.select_video_button.setEnabled(False)

    def enable_buttons(self):
        self.ui.upscale_button.setEnabled(True)
        self.ui.select_output_button.setEnabled(True)
        self.ui.select_video_button.setEnabled(True)

    def update(self):
        self.ui.upscale_status_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))
        self.ui.upscale_status_label.setText("Upscale Complete!")
        self.enable_buttons()

    # Parse everything we need from the GUI into a dandere2x friendly format
    # Leave everything as STR's since config files are just strings
    def parse_gui_inputs(self):

        self.output_file = self.output_file.replace("/", "\\")
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
            self.waifu2x_type = "converter_cpp"

    def press_select_video_button(self):

        self.file_dir = self.load_file()[0]

        if self.file_dir == '':
            return

        path, name = os.path.split(self.file_dir)

        # set the video label to the selected file name
        self.ui.video_label.setText(name)
        self.ui.video_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 11, QtGui.QFont.Bold))

        with open(os.path.join(self.this_folder, "dandere2x.json"), "r") as read_file:
            config_json = json.load(read_file)

        context = Context(config_json)

        # load the needed video settings for the GUI
        videosettings = VideoSettings(context.ffprobe_dir, self.file_dir)

        # Get a list of valid list block sizes knowing the width and height
        valid_list_blocksize = get_valid_block_sizes(videosettings.height, videosettings.width)

        self.ui.block_size_combo_box.clear()
        self.ui.block_size_combo_box.addItems(valid_list_blocksize)
        self.ui.block_size_combo_box.setEnabled(True)

        # to avoid users leaving it as '1'
        self.ui.block_size_combo_box.setCurrentIndex(len(valid_list_blocksize) / 1.5)

        name_only = name.split(".")[0]

        # parse inputs so we can access variables
        self.parse_gui_inputs()

        # make a default name
        self.output_file = os.path.join(path, (name_only + "_"
                                               + "[" + str(self.waifu2x_type) + "]"
                                               + "[s" + str(self.scale_factor) + "]"
                                               + "[n" + str(self.noise_level) + "]"
                                               + "[b" + str(self.block_size) + "]"
                                               + "[q" + str(self.image_quality) + "]" + ".mkv"))

        self.set_output_file_name()
        self.refresh_buttons()

    def press_select_output_button(self):

        self.output_file = self.save_file_name()

        # If the user didn't select anything, don't continue or it'll break
        # Everything
        if self.output_file == '':
            return

        self.set_output_file_name()

        self.refresh_buttons()

    def set_output_file_name(self):

        # set the label to only display the last 20 elements of the selected workspace
        start_val = len(self.output_file) - 28
        if start_val < 0:
            start_val = 0

        self.ui.workspace_label.setText(".." + self.output_file[start_val:  len(self.output_file)])
        self.ui.workspace_label.setFont(QtGui.QFont("Yu Gothic UI Semibold", 8, QtGui.QFont.Bold))

    def load_dir(self):
        self.ui.w = QWidget()

        self.ui.w.resize(320, 240)
        filename = QFileDialog.getExistingDirectory(w, 'Open Directory', self.this_folder)
        return filename

    def save_file_name(self):
        self.ui.w = QWidget()
        filter = "Images (*.mkv *.mp4)"
        self.ui.w.resize(320, 240)

        default_name = self.output_file
        if self.output_file == '':
            default_name = self.this_folder

        filename = QFileDialog.getSaveFileName(w, 'Save File', default_name, filter)
        return filename[0]

    def load_file(self):
        self.ui.w = QWidget()

        self.ui.w.resize(320, 240)
        filename = QFileDialog.getOpenFileName(w, 'Open File', self.this_folder)
        return filename


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())
