import sys

global_settings = {
    'XXH_VERSION': '0.1'
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        setting_name = sys.argv[1]
        if setting_name in global_settings:
            print(global_settings[setting_name])
        else:
            sys.exit(1)
    else:
        print(global_settings)