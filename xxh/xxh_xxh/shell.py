import os, sys
from pathlib import Path
import subprocess

def S(cmd, trace=False):
    if type(cmd) == list:
        cmd = ' '.join(cmd)
    if trace:
        print(cmd)
    return os.system(cmd)

def SC(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    [out, err] = proc.communicate()
    return (out, err, proc)

def A(args, q=0, i=0):
    if type(args) == list:
        if i == 1:
            args = ' '.join([f"'{a}'" for a in args])
        elif i == 2:
            args = ' '.join([f'"{a}"' for a in args])
        elif i == 3:
            args = ' '.join([f'\\"{a}\\"' for a in args])
        else:
            args = ' '.join([str(a) for a in args])
    if q == 1:
        return f"'{args}'"
    elif q == 2:
        return f'"{args}"'
    return str(args)

def p(path_str):
    return Path(path_str).expanduser()

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def eeprint(*args, **kwargs):
    return_code=1
    if 'return_code' in kwargs:
        return_code = kwargs['return_code']
        del kwargs['return_code']
    print(*args, file=sys.stderr, **kwargs)
    sys.exit(return_code)

if __name__ == '__main__':
    print('Example')
    [o, e, p] = SC('ls')

    if p.returncode == 0:
        print(f'OUTPUT: {o}')
    else:
        print(f'ERROR: {e}')
