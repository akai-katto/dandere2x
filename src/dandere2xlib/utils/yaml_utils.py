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

    # absolutify a json method by replacing ".." into "current_folder".
    # there's some trickery to do this, but it works


def absolutify_yaml(unparsed_yaml: yaml, current_folder: str, absolutify_key=".."):
    """
    The function to translates ".." in a loaded .yaml config file into 'current_folder'.
    For example, ../folder/stuff -> C:/temp/folder/stuff.

    Note that when python does str(yaml) some values are changed, so we also have to convert those
    values back to their yaml equivalent.
    """

    current_folder_yaml = current_folder.replace("\\", "\\\\")
    parsed_yaml_str = str(unparsed_yaml)

    # turn python's string'd json into a normal json
    parsed_yaml_str = parsed_yaml_str.replace("\'", "\"")
    parsed_yaml_str = parsed_yaml_str.replace("True", "true")
    parsed_yaml_str = parsed_yaml_str.replace("False", "false")
    parsed_yaml_str = parsed_yaml_str.replace("None", "null")
    parsed_yaml_str = parsed_yaml_str.replace(absolutify_key, current_folder_yaml)

    # load the json back into the config
    return yaml.safe_load(parsed_yaml_str)
