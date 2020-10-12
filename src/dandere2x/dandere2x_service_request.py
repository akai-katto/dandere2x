import copy


class Dandere2xServiceRequest:

    def __init__(self,
                 input_file: str,
                 output_file: str,
                 workspace: str,
                 block_size: int,
                 denoise_level: int,
                 quality_minimum: int,
                 scale_factor: int,
                 output_options: dict):

        self.workspace = workspace
        self.scale_factor = scale_factor
        self.quality_minimum = quality_minimum
        self.denoise_level = denoise_level
        self.block_size = block_size
        self.output_file = output_file
        self.input_file = input_file
        self.output_options = copy.copy(output_options)
