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
import time
from wrappers.frame import Frame


# waits for a text file, then returns the file as a list sperated by lines
# to do - I've gotton permission errors. Perhaps adding a catch for that.
def wait_on_text(text_file: str):
    logger = logging.getLogger(__name__)
    exists = exists = os.path.isfile(text_file)
    count = 0
    while not exists:
        if count % 10000 == 0:
            logger.info(text_file + "dne, waiting")
        exists = os.path.isfile(text_file)
        count += 1
        time.sleep(.01)

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


# many times a file may not exist yet, so just have this function
# wait if it does not.
def wait_on_file(file_string: str):
    logger = logging.getLogger(__name__)
    exists = exists = os.path.isfile(file_string)
    count = 0
    while not exists:
        if count % 1000000 == 0:
            logger.info(file_string + "dne, waiting")
        exists = os.path.isfile(file_string)
        count += 1
        time.sleep(.001)


# custom function to rename file if it already exists
def rename_file(file1, file2):
    try:
        os.rename(file1, file2)
    except FileExistsError:
        os.remove(file2)
        os.rename(file1, file2)


# Both waifu2x-Caffe and waifu2x-conv read images in lexiconic order, so in order
# to maximize efficiency, save the images that will be upscaled by waifu2x in lexiconic ordering.
def get_lexicon_value(digits: int, val: int):
    string = str(val)

    while (len(string) < digits):
        string = '0' + string

    return string


# get frame count from a string input
def get_seconds_from_time(time_frame: int):
    splitted = time_frame.split(":")
    print(splitted)
    hours_seconds = int(splitted[0]) * 3600
    minutes_seconds = int(splitted[1]) * 60
    seconds = int(splitted[2])

    return hours_seconds + minutes_seconds + seconds


def determine_sens(workspace: str, frame: Frame, lower_val: int, higher_val: int):
    from wrappers.frame import Frame

    frame.save_image_quality(workspace + "lower.jpg", lower_val)
    frame.save_image_quality(workspace + "higher.jpg", higher_val)

    lower_image = Frame()
    lower_image.load_from_string(workspace + "lower.jpg")

    higher_image = Frame()
    higher_image.load_from_string(workspace + "higher.jpg")

    lower_mse = frame.mean(lower_image)
    higher_mse = frame.mean(higher_image)

    os.remove(workspace + "lower.jpg")
    os.remove(workspace + "higher.jpg")

    return lower_mse, higher_mse



def main():
    text = wait_on_text("/home/linux/Videos/newdebug/yn2/pframe_data/pframe_1.txt")


if __name__ == "__main__":
    main()
