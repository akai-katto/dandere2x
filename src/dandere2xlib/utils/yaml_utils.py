import os

import yaml

# given a list like ["hi", "bye", "kyle"],
# return a list in the shape "hi, bye, kyle"
# This is because ffmpeg expects it in this format
def list_to_string(list_input: list):
    return_str = ''
    for item in list_input:
        return_str += item + ","

    return return_str[:-1]


# This is a pretty messy function, but if it's an ffmpeg command we
# need to be cognizant if an element ia  list or not.
# If it's a list, we need to add it in a very peculiar way so that ffmpeg can recognize the input
def get_options_from_section(section: yaml, ffmpeg_command=False):
    execute = []

    for item in section:
        if section[item] is not None:

            # if the item is any value but 'true', append both the key and value
            if section[item] is not True:

                if type(section[item]) is list and ffmpeg_command is True:
                    execute.append(str(item))
                    execute.append(list_to_string(section[item]))

                else:
                    execute.append(str(item))
                    execute.append(str(section[item]))

            # if it's set to true, simply append the key
            else:
                execute.append(str(item))

    return execute


def load_executable_paths_yaml() -> dict:
    """
    Load the dandere2x_directories yaml file, but replace all the relative path definitions with absolute
    definitions.
    """
    from os import path
    from pathlib import Path
    import sys
    from dandere2xlib.utils.dandere2x_utils import get_operating_system

    # get location of dandere2x directories (will be in the same folder as main)
    configfile = "executable_paths.yaml"
    main_path = Path(path.abspath(sys.modules['__main__'].__file__)).parent
    config_path = Path(path.join(main_path, "config_files"))
    directory_file = os.path.join(config_path, configfile)

    # load yaml
    with open(directory_file, "r") as read_file:
        config = yaml.safe_load(read_file)

    # replace each relative path with it's absolute counter-part (if applicable)
    for key in config:
        if get_operating_system() == "win32":
            """ Modifications needed to take place if we're not unix-based """
            config[key] = config[key].replace("/", "\\")
            config[key] = config[key] + ".exe"

        if not os.path.isabs(config[key]):
            config[key] = os.path.join(main_path, config[key])

    return config
