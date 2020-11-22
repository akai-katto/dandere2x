import argparse
import os
import yaml

from dandere2x.dandere2x_service_request import Dandere2xServiceRequest, ProcessingType, \
    get_root_thread_from_root_service_request


def create_parser():
    """
    Create a parser for dandere2x for the needed arguments.
    :return: ArgsParse for dandere2x.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('-b', '--block_size', action="store", dest="block_size", type=int, default=30,
                        help='Block Size (Default 30)')

    parser.add_argument('-i', '--input', action="store", dest="input_file", help='Input Video (no default)')

    parser.add_argument('-o', '--output', action="store", dest="output_file", help='Output Video (no default)')

    parser.add_argument('-q', '--quality', action="store", dest="image_quality", type=int, default=85,
                        help='Image Quality (Default 85)')

    parser.add_argument('-w', '--waifu2x_type', action="store", dest="waifu2x_type", type=str, default="vulkan",
                        help='Waifu2x Type. Options: "vulkan" "converter-cpp" "caffe". Default: "vulkan"')

    parser.add_argument('-s', '--scale_factor', action="store", dest="scale_factor", type=int, default=2,
                        help='Scale Factor (Default 2)')

    parser.add_argument('-n', '--noise_level', action="store", dest="noise_level", type=int, default=3,
                        help='Denoise Noise Level (Default 3)')

    parser.add_argument('-p', '--process_type', action="store", dest="processing_type", type=str, default="single",
                        help='Processing Type (Options: "single", "multi"')

    parser.add_argument('-ws', '--workspace', action="store", dest="workspace", type=str, default=".",
                        help='Workspace Directory (Default "." ) ')

    args = parser.parse_args()
    return args


def service_request_from_args(args) -> Dandere2xServiceRequest:
    """
    Constructs a service request from args.
    @param args: An argsparse instance
    @return: The "root" Dandere2xServiceRequest
    """

    with open("output_options.yaml", "r") as read_file:
        output_config = yaml.safe_load(read_file)

    request = \
        Dandere2xServiceRequest(
            input_file=args.input_file,
            output_file=args.output_file,
            workspace=os.path.abspath(args.workspace),
            block_size=args.block_size,
            denoise_level=args.noise_level,
            quality_minimum=args.image_quality,
            scale_factor=args.scale_factor,
            output_options=output_config,
            processing_type=ProcessingType.from_str(args.processing_type),
            name="Master Service Request")

    return request


def main():
    args = create_parser()  # Get the parser specific to dandere2x
    root_service_request = service_request_from_args(args)

    root_service_request.log_all_variables()

    AnonymousDandere2xService = get_root_thread_from_root_service_request(root_service_request)

    root_thread = AnonymousDandere2xService(service_request=root_service_request)

    root_thread.start()
    root_thread.join()




if __name__ == '__main__':
    main()
