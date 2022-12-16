import logging
import time

from dandere2x import Dandere2x, set_dandere2x_logger
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2x.dandere2xlib.utils.dandere2x_utils import show_exception_and_exit


def cli_start():
    args = Dandere2xServiceRequest.get_args_parser()  # Get the parser specific to dandere2x
    root_service_request = Dandere2xServiceRequest.load_from_args(args=args)
    root_service_request.log_all_variables()
    root_service_request.make_workspace()

    dandere2x_session = Dandere2x(service_request=root_service_request)
    dandere2x_session.start()
    dandere2x_session.join()


def start_gui():
    """ Start the dandere2x GUI. We load gui_start inline here, because on import gui_driver gets called and made. """
    from gui_driver import gui_start

    print("Calling GUI start.")
    gui_start()


def main():
    """ Start a Dandere2x session either through CLI or GUI. In either event, the total runtime is printed. """

    # Set a custom 'except hook' to prevent window from closing on crash.
    import sys
    sys.excepthook = show_exception_and_exit
    
    print("version 3.6")
    # set the master logger at the highest level
    set_dandere2x_logger("root")
    logging.propagate = False

    start = time.time()

    if len(sys.argv) == 1:
        start_gui()
    else:
        cli_start()

    print("Total runtime duration:", time.time() - start)


main()