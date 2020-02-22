import os, sys, glob

$UPDATE_OS_ENVIRON=True

$XXH_HOME = os.path.dirname(os.path.realpath(__file__))
$PIP_TARGET = os.path.join($XXH_HOME, 'pip')
$PYTHONPATH = $PIP_TARGET
$PATH = [ os.path.join($PYTHONHOME, 'bin'), $XXH_HOME ] + $PATH
sys.path.append($PIP_TARGET)
aliases['xpip'] = ['python','-m','pip']
aliases['xxh'] = os.path.join($XXH_HOME, 'xonsh') + ' ' + os.path.join($XXH_HOME, 'xxh')

for plugin_path in sorted(glob.glob(os.path.join($XXH_HOME, 'plugins/**'))):
    if os.path.exists(os.path.join(plugin_path, 'xonshrc.xsh')):
        sys.path.append(plugin_path)
        __import__('xonshrc')
        del sys.modules['xonshrc']
        sys.path.remove(plugin_path)