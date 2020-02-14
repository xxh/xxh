import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from settings import global_settings

if __name__ == "__main__":
    for e in ['XXH_HOME', 'PIP_TARGET', 'PYTHONPATH']:
        if e in ${...}:
            global_settings[e] = ${e}

    print(global_settings)