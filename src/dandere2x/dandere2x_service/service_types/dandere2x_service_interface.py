import time
from abc import abstractmethod, ABC
from threading import Thread

from dandere2x.dandere2x_service_request import Dandere2xServiceRequest


@abstractmethod
class Dandere2xServiceInterface(Thread, ABC):
    """
    An abstract-base-class dictating how dandere2x_service should be utilized.

    As an example, a singleprocess_service will only use one dandere2x-thread to upscale a video file, where as
    multiprocess_service will use multiple. In either case, an upscaled video will still be produced, but the black
    box implementation in between will change.

    This abstract-interface gives enough shared functions / descriptions of how the black-box should be implemented,
    See singleprocess_service.py or gif_service.py for examples of how to use these shared functions / see why they
    exist.
    """

    def __init__(self, service_request: Dandere2xServiceRequest):
        super().__init__()

        self._service_request = service_request

        # meta-data
        self.__start_time: float = 0
        self.__end_time: float = 0

    # Public Methods

    def timer_start(self) -> None:
        self.__start_time = time.time()

    def timer_end(self) -> None:
        self.__end_time = time.time()

    def timer_get_duration(self) -> float:
        return self.__end_time - self.__start_time

    @abstractmethod
    def run(self):
        pass

    # Protected Methods

    @abstractmethod
    def _pre_process(self):
        pass

    @abstractmethod
    def _on_completion(self):
        pass