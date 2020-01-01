
import time

import yaml

from context import Context
from dandere2x import Dandere2x
from dandere2xlib.utils.dandere2x_utils import get_operating_system
from dandere2x import Dandere2x

configfile = "dandere2x_%s.yaml" % get_operating_system()

# load yaml

with open(configfile, "r") as read_file:
    config = yaml.safe_load(read_file)


context = Context(config)


dandere2x = Dandere2x(context)

dandere2x.start()