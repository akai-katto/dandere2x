import json

# if the value in the key value pair exists, add it.
# if the key is just 'true', only add the key
def get_options_from_section(section: json):
    execute = []

    for item in section:
        if section[item]:
            if section[item] != True:
                execute.append(str(item))
                execute.append(str(section[item]))
            else:
                execute.append(str(item))

    return execute


with open("dandere2x.json", "r") as read_file:
    config = json.load(read_file)


print(get_options_from_section(config['ffmpeg']['time_options']))


list_thing = get_options_from_section(config['ffmpeg']['time_options'])

print(list_thing == None)
