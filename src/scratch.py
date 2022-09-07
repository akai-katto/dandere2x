from dandere2x.dandere2xlib.utils.yaml_utils import load_executable_paths_yaml

if __name__ == "__main__":
    test = load_executable_paths_yaml()
    print(test['waifu2x_vulkan'])