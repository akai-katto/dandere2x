from dandere2x.dandere2x_interface import Dandere2xInterface
from dandere2x.dandere2x_service import Dandere2xServiceThread
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest


class Raw(Dandere2xInterface):

    def __init__(self, service_request: Dandere2xServiceRequest):
        super().__init__(service_request=service_request)
        self.thread = Dandere2xServiceThread(service_request=service_request)

    def pre_process(self):
        pass

    def start(self):
        self.thread.start()

    def join(self):
        self.thread.join()

    def on_completion(self):
        pass
