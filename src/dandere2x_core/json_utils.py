import json

def get_options_from_section(section: json):
    execute = []

    for item in section:
        if section[item] != None:
            if section[item] != True:
                execute.append(str(item))
                execute.append(str(section[item]))
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
