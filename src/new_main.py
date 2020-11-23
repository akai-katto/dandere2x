from dandere2x import Dandere2x
from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2x.singleprocess import SingleProcess



"""
Sample Args / Useful for Development
"""


args = Dandere2xServiceRequest.get_args_parser()  # Get the parser specific to dandere2x
root_service_request = Dandere2xServiceRequest.load_from_args(args=args)
root_service_request.log_all_variables()
root_service_request.make_workspace()


young_dandere2x = Dandere2x(service_request=root_service_request)
young_dandere2x.start()
young_dandere2x.join()


