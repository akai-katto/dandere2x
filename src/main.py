import time

from dandere2x import Dandere2x
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2x.dandere2xlib.utils.dandere2x_utils import show_exception_and_exit


def cli_start():
    args = Dandere2xServiceRequest.get_args_parser()  # Get the parser specific to dandere2x
    root_service_request = Dandere2xServiceRequest.load_from_args(args=args)
    root_service_request.log_all_variables()
    root_service_request.make_workspace()

    young_dandere2x = Dandere2x(service_request=root_service_request)
    young_dandere2x.start()
    young_dandere2x.join()


def start_gui():
    """ Start the dandere2x GUI. We load gui_start inline here, because on import gui_driver gets called and made. """
    from gui_driver import gui_start

    print("Calling GUI start.")
    gui_start()


def main():
    """ Start a Dandere2x session either through CLI or GUI. In either event, the total runtime is printed. """

    # Administrative Stuff #
    # Set a custom 'except hook' to prevent window from closing on crash.
    import sys
    sys.excepthook = show_exception_and_exit

    start = time.time()

    if len(sys.argv) == 1:
        start_gui()
    else:
        cli_start()

    print("Total runtime duration:", time.time() - start)


main()
