from pathlib import Path
import colorlog
import logging

from colorlog import ColoredFormatter


def set_dandere2x_logger(input_file_path: str) -> None:
    """
    Create the logging class to be format print statements the dandere2x way.

    The formatted output resembles the following (roughly):
        outputvid0.mkv 2020-08-01 16:03:39,455 INFO     __dandere2x_service.py : Hewwooo
        outputvid0.mkv 2020-08-01 16:03:39,456 WARNING  __dandere2x_service.py : jeeez fuck this warning
        outputvid0.mkv 2020-08-01 16:03:39,456 ERROR    __dandere2x_service.py : oh fuck fuck fuck stop the program an error occurred
    """
    input_file_name = Path(input_file_path).name + " "
    color_log_format = input_file_name + "%(log_color)s%(asctime)-8s%(reset)s %(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(filename)-8s%(reset)s %(log_color)s%(funcName)-8s%(reset)s: %(log_color)s%(message)s"

    formatter = ColoredFormatter(
        color_log_format,
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )

    handler = colorlog.StreamHandler()
    handler.setFormatter(formatter)

    logger = colorlog.getLogger(name=input_file_path)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.info("Dandere2x Console Logger Set")


# def __set_file_logger(self, file: str):
#     self.log.info("Writing log-file at %s" % file)
#     formatter = logging.Formatter(self.file_log_format)
#     self.fh = logging.FileHandler(file, "w", "utf-8")
#     self.fh.setFormatter(formatter)
#     self.log.addHandler(self.fh)
#     self.log.info("Log-file set.")
