import sys, os

global_settings = {
    'XXH_VERSION': '0.6.3'
}

if __name__ == "__main__":

    for e in ['XXH_HOME', 'PIP_TARGET', 'PYTHONPATH']:
        if e in os.environ:
            global_settings[e] = os.environ[e]

    if len(sys.argv) > 1:
        setting_name = sys.argv[1]
        if setting_name in global_settings:
            print(global_settings[setting_name])
        else:
            sys.exit(1)
    else:
        print(global_settings)
