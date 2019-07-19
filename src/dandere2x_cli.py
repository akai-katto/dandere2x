import argparse
from dandere2x import Dandere2x

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", type = str, nargs = 1,
                        metavar = "file_name", default = None,
                        help = "Input video file")

parser.add_argument("-o", "--output", type = str, nargs = 1,
                        metavar = "directory", default = None,
                        help = "Output directory and workspace.")

parser.add_argument("-b", "--block_size", type = int, nargs = 1,
                        metavar = "block_size", default = None,
                        help = "Block size for Dandere2x to work with")

parser.add_argument("-q", "--quality_low", type = int, nargs = 1,
                        metavar = "quality integer", default = None,
                        help = "Lowest quality to accept a block, relative to JPG standards")

args = parser.parse_args()

print(args.quality_low)

d = Dandere2x('config.ini')

d.context.file_dir = args.input
d.context.workspace = args.output

print(args.quality_low)

#d.run_concurrent()