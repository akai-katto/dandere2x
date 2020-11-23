import yaml

from dandere2x.dandere2x_service_request import Dandere2xServiceRequest
from dandere2x.__dandere2x_service import Dandere2xServiceThread
from dandere2x.MultiProcess import MultiProcess
from dandere2x.SingleProcess import SingleProcess

with open("config_files/output_options.yaml", "r") as read_file:
    output_config = yaml.safe_load(read_file)

# service_request1 = \
#     Dandere2xServiceRequest(
#         input_file="C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\shortvideo.mp4",
#         output_file="C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\version_upscaled.mkv",
#         workspace="C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\default_workspace1\\",
#         block_size=30,
#         denoise_level=3,
#         quality_minimum=95,
#         scale_factor=2,
#         output_options=output_config,
#         name="service_request1")

service_request1 = \
    Dandere2xServiceRequest(
        input_file="C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\shortvideo.mp4",
        output_file="C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\version_upscaled_sp.mkv",
        workspace="C:\\Users\\windw0z\\Documents\\GitHub\\dandere2x\\src\\workspace\\default_workspace2\\",
        block_size=30,
        denoise_level=3,
        quality_minimum=95,
        scale_factor=2,
        output_options=output_config,
        name="service_request1")

service_request1.make_workspace()

sp1 = SingleProcess(service_request1)

sp1.timer_start()
sp1.start()
sp1.join()
sp1.timer_end()

# sp1 = MultiProcess(service_request1)
#
# sp1.timer_start()
# sp1.start()
# sp1.join()
# sp1.timer_end()

print(sp1.timer_get_duration())


