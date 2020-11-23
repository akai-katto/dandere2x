from typing import Type
from threading import Thread

from dandere2x.__dandere2x_interface import Dandere2xInterface
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest, ProcessingType

# todo

class Dandere2x(Thread):
    """
    Accepts a "root"-level request and will handle all the logic in spawning the child-dandere2x sessions.

    This folder is a very generic wrapper in that it's mostly there to handle superficial logic in how dandere2x
    should go about processing a service request.
    """

    def __init__(self, service_request: Dandere2xServiceRequest):
        super().__init__()

        self._service_request = service_request

        anonymous_dandere2x_service = self._determine_root_request(self._service_request)
        self._root_service_thread = anonymous_dandere2x_service(service_request=self._service_request)

    @staticmethod
    def _determine_root_request(request) -> Type[Dandere2xInterface]:
        """
        A wrapper to determine what the root service should be - i.e a logical set of operations to determine what
        the user was intending for dandere2x to return given the initial service request.

        @param request: The root service request.
        @return: A Dandere2xInterface-inherited subclass.
        """

        if request.processing_type == ProcessingType.MULTI_PROCESS:
            from dandere2x.multiprocess import MultiProcess
            return MultiProcess

        if request.processing_type == ProcessingType.SINGLE_PROCESS:

            from dandere2x.singleprocess import SingleProcess
            return SingleProcess

    def run(self) -> None:
        self._root_service_thread.run()
