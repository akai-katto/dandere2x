import json

# if the value in the key value pair exists, add it.
# if the key is just 'true', only add the key
def get_options_from_section(section: json):
    execute = []

    for item in section:
        print(section[item])

        if section[item]:
            if section[item] != True:
                execute.append(str(item))
                execute.append(str(section[item]))
            else:
                execute.append(str(item))


    return execute

def _read_configuration(self, phase, section=None):
        """ read configuration from JSON
        Read the configurations (arguments) from the JSON
        configuration file and append them to the end of the
        FFmpeg command.
        Arguments:
            execute {list} -- list of arguments to be executed
            phase {str} -- phase of operation
        """

        configuration = []

        # if section is specified, read configurations or keys
        # from only that section
        if section:
            source = self.ffmpeg_settings[phase][section].keys()

            # if pixel format is not specified, use the source pixel format
            try:
                if self.ffmpeg_settings[phase][section].get('-pix_fmt') is None:
                    self.ffmpeg_settings[phase][section]['-pix_fmt'] = self.pixel_format
            except KeyError:
                pass
        else:
            source = self.ffmpeg_settings[phase].keys()

        for key in source:

            if section:
                value = self.ffmpeg_settings[phase][section][key]
            else:
                value = self.ffmpeg_settings[phase][key]

            # null or None means that leave this option out (keep default)
            if value is None or value is False or isinstance(value, list) or isinstance(value, dict):
                continue
            else:
                configuration.append(key)

                # true means key is an option
                if value is True:
                    continue

                configuration.append(str(value))

        return configuration

with open("dandere2x.json", "r") as read_file:
    config = json.load(read_file)


print(get_options_from_section(config['ffmpeg']['migrating_tracks']['output_options']))


list_thing = config['ffmpeg']['migrating_tracks']['output_options']

print(list_thing == None)

print(isinstance(list_thing, dict))

print(list_thing)
