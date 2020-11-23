#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Dandere2X Utils
Author: CardinalPanda
Date Created: March 22, 2019
Last Modified: April 2, 2019
"""

import logging
import os
import shutil
import sys
import time
from sys import platform

from pip._vendor.distlib.compat import raw_input
from wget import bar_adaptive


def get_operating_system():
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "win32":
        return 'win32'


def show_exception_and_exit(exc_type, exc_value, tb):
    """
    To keep Dandere2x window open on death.
    """
    import traceback
    traceback.print_exception(exc_type, exc_value, tb)
    raw_input("Press key to exit.")
    sys.exit(-1)


def force_delete_directory(directory):
    """ Deletes a workspace with really aggressive functions calls. shutil.rm had too many issues. """
    log = logging.getLogger()

    if os.path.isdir(directory):
        log.info("%s exists, attempting to delete the workspace folder." % directory)
        try:
            os.system('rmdir /S /Q "{}"'.format(directory))
        except PermissionError:
            log.warning("Trying to delete workspace with rmtree threw PermissionError - Dandere2x may not work.")
            log.warning("Dandere2x will continue regardless of this. ")

        # Even though os.system rm was called, it's possible for windows to lag behind, so make sure the folder actually
        # was deleted before continuing.
        while file_exists(directory):
            log.warning("%s still exists, waiting..." % directory)
            time.sleep(1)


from dandere2x.__dandere2x_service_controller import Dandere2xController


def get_list_from_file_and_wait(text_file: str, controller=Dandere2xController()):
    logger = logging.getLogger(__name__)
    exists = exists = os.path.isfile(text_file)
    count = 0
    while not exists and controller.is_alive():
        if count / 500 == 0:
            logger.debug(text_file + " does not exist, waiting")
        exists = os.path.isfile(text_file)
        count += 1
        time.sleep(.01)

    if not controller.is_alive():
        return

    file = None
    try:
        file = open(text_file, "r")
    except PermissionError:
        logging.info("permission error on file" + text_file)

    while not file:
        try:
            file = open(text_file, "r")
        except PermissionError:
            logging.info("permission error on file" + text_file)

    text_list = file.read().split('\n')
    file.close()

    if len(text_list) == 1:
        return []

    return text_list


def wait_on_file(file_string: str, controller=Dandere2xController()):
    logger = logging.getLogger(__name__)
    exists = os.path.isfile(file_string)
    count = 0
    while not exists and controller.is_alive():
        if count / 500 == 0:
            logger.debug(file_string + " does not exist, waiting")
        exists = os.path.isfile(file_string)
        count += 1
        time.sleep(.001)


# for renaming function, break when either file exists
def wait_on_either_file_controller(file_1: str, file_2: str, controller=Dandere2xController()):
    logger = logging.getLogger(__name__)
    exists_1 = os.path.isfile(file_1)
    exists_2 = os.path.isfile(file_2)
    count = 0
    while not (exists_1 or exists_2) and controller.is_alive():
        if count / 500 == 0:
            logger.debug(file_1 + " does not exist, waiting")
        exists_1 = os.path.isfile(file_1)
        exists_2 = os.path.isfile(file_2)

        count += 1
        time.sleep(.001)


# many times a file may not exist yet, so just have this function wait if it does not.
def file_exists(file_string: str):
    return os.path.isfile(file_string)


# many times a file may not exist yet, so just have this function wait if it does not.
def file_is_empty(file_string: str):
    return os.path.getsize(file_string) == 0


def dir_exists(file_string: str):
    logger = logging.getLogger(__name__)
    return os.path.isdir(file_string)


def rename_file(file1, file2):
    """Custom rename file method, catches error and overwrites file2 if output file exists already."""
    try:
        os.rename(file1, file2)
    except FileExistsError:
        os.remove(file2)
        os.rename(file1, file2)


def rename_file_wait(file1, file2):
    log = logging.getLogger()
    renamed = False

    while not renamed:
        try:
            os.rename(file1, file2)
            renamed = True
        except PermissionError:
            log.warning("Permission error thrown, attempting again.")
            pass


# Both waifu2x-Caffe and waifu2x-conv read images in lexiconic order, so in order
# to maximize efficiency, save the images that will be upscaled by waifu2x in lexiconic ordering.
def get_lexicon_value(digits: int, val: int):
    return str(val).zfill(digits)


def get_valid_block_sizes(width: int, height: int, minimum=1):
    valid_sizes = []

    larger_val = [width, height][height > width]

    for x in range(minimum, larger_val):
        if width % x == 0 and height % x == 0:
            valid_sizes.append(str(x))

    return valid_sizes


def valid_input_resolution(width: int, height: int, block_size: int):
    return width % block_size == 0 and height % block_size == 0


def create_directories(workspace: str, directories_list: list):
    """
    In dandere2x's context file, there's a list of directories"""
    log = logging.getLogger()
    log.info("Creating directories. Starting with %s first" % workspace)

    # need to create workspace first or else subdirectories wont get made correctly
    try:
        os.makedirs(workspace)
    except:
        log.warning("Creation of directory %s failed.. dandere2x may still work but be advised. " % workspace)
    # create each directory
    for subdirectory in directories_list:
        try:
            os.makedirs(subdirectory)
        except OSError:
            log.warning("Creation of the directory %s failed.. dandere2x may still work but be advised. " % workspace)
        else:
            log.info("Successfully created the directory %s " % subdirectory)


def delete_directories(directories_list: list):
    # create each directory
    for subdirectory in directories_list:
        try:
            shutil.rmtree(subdirectory)
        except OSError:
            print("Deletion of the directory %s failed" % subdirectory)
        else:
            print("Successfully deleted the directory %s " % subdirectory)


def get_a_valid_input_resolution(width: int, height: int, block_size: int):
    width_up = width
    width_down = width

    height_up = height
    height_down = height

    while width_up % block_size != 0:
        width_up = width_up + 1

    while width_down % block_size != 0:
        width_down = width_down - 1

    while height_up % block_size != 0:
        height_up = height_up + 1

    while height_down % block_size != 0:
        height_down = height_down - 1

    smaller_width = width_up if abs(width_up - width) < abs(width_down - width) else width_down

    smaller_height = height_up if abs(height_up - height) < abs(height_down - height) else height_down

    return smaller_width, smaller_height


# TODO bring this to ffprobe's modern settings
# TODO Very outdated!
def verify_user_settings(context):
    from wrappers.frame.frame import Frame

    input_frames_dir = context.input_frames_dir
    extension_type = context.extension_type
    block_size = context.block_size

    f1 = Frame()
    f1.load_from_string(input_frames_dir + "frame1" + extension_type)

    valid = True

    if f1.width % block_size != 0 and f1.height % block_size != 0:
        print("----------------------ERROR---------------------------------------")
        print("Your block size is incompatible with the resolution you provided. ")
        print("Valid Block sizes are:")
        print("------------------------------------------------------------------")
        valid_sizes = []

        larger_val = [f1.width, f1.height][f1.height > f1.width]

        for x in range(1, larger_val):
            if f1.width % x == 0 and f1.height % x == 0:
                valid_sizes.append(x)

        print(valid_sizes)
        print("------------------------------------------------------------------")
        new_block_size = int(input("Enter your value (recommended 25 or greater): "))

        while new_block_size not in valid_sizes:
            new_block_size = int(input("Invalid Choice! Re-Enter a correct value: "))

        context.block_size = new_block_size


def download_and_extract_externals(dandere2x_dir: str):
    import wget
    import zipfile
    import os

    print(
        "Downloading: " + "https://github.com/aka-katto/dandere2x_externals_static/releases/download/1.1/externals.zip")
    download_file = dandere2x_dir + "download.zip"
    wget.download('https://github.com/aka-katto/dandere2x_externals_static/releases/download/1.1/externals.zip',
                  out=download_file, bar=bar_adaptive)

    with zipfile.ZipFile(download_file, 'r') as zip_ref:
        zip_ref.extractall(dandere2x_dir)

    print("finished downloading")
    os.remove(download_file)
