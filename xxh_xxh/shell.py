import os
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

def A(args, q=0):
    if type(args) == list:
        args = ' '.join([str(a) for a in args])
    if q == 1:
        return f"'{args}'"
    elif q == 2:
        return f'"{args}"'
    return str(args)

def p(path_str):
    return Path(path_str).expanduser()
