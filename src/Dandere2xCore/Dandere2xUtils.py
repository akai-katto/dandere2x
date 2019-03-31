import logging
import os
import time


# waits for a text file, then returns
def wait_on_text(text_file):
    logger = logging.getLogger(__name__)
    exists = exists = os.path.isfile(text_file)
    count = 0
    while not exists:
        if count % 10000 == 0:
            logger.info(text_file + "dne, waiting")
        exists = os.path.isfile(text_file)
        count += 1
        time.sleep(.01)

    file = open(text_file, "r")

    text_list = file.read().split('\n')
    file.close()

    if len(text_list) == 1:
        return []

    return text_list


def wait_on_file(file_string):
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


def get_lexicon_value(digits, val):
    string = str(val)

    while (len(string) < digits):
        string = '0' + string

    return string

# get frame count from a string input
def get_seconds_from_time(time_frame):
    splitted = time_frame.split(":")
    print(splitted)
    hours_seconds = int(splitted[0]) * 3600
    minutes_seconds = int(splitted[1]) * 60
    seconds = int(splitted[2])

    return hours_seconds + minutes_seconds + seconds

def main():
    text = wait_on_text("/home/linux/Videos/newdebug/yn2/pframe_data/pframe_1.txt")


if __name__ == "__main__":
    main()
