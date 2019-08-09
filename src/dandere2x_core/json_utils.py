import json



# given a list like ["hi", "bye", "kyle"],
# return a list in the shape "hi, bye, kyle"
# This is because ffmpeg expects it in this format
def list_to_string(list_input: list):

    print(list_input)

    return_str = ''
    for item in list_input:
        return_str += item + ","

    print(return_str[:-1])

    return return_str[:-1]

# This is a pretty messy function, but if it's an ffmpeg command we
# need to be cognizant if an element ia  list or not.
# If it's a list, we need to add it in a very peculiar way so that ffmpeg can recognize the input
def get_options_from_section(section: json, ffmpeg_command = False):
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
def absolutify_json(config_json: json, current_folder: str, absolutify_key=".."):

    current_folder_json = current_folder.replace("\\", "\\\\")

    config_json_string = str(config_json)

    # turn python's string'd json into a normal json
    config_json_string = config_json_string.replace("\'", "\"")
    config_json_string = config_json_string.replace("True", "true")
    config_json_string = config_json_string.replace("False", "false")
    config_json_string = config_json_string.replace("None", "null")
    config_json_string = config_json_string.replace(absolutify_key, current_folder_json)

    # load the json back into the config
    return json.loads(config_json_string)
