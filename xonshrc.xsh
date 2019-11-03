import os, sys
$XXH_HOME = os.path.dirname(os.path.realpath(__file__))
$PIP_TARGET = os.path.join($XXH_HOME, 'pip')
$PYTHONPATH = $PIP_TARGET
$PATH = [ os.path.join($PYTHONHOME, 'bin'), $XXH_HOME ] + $PATH
sys.path.append($PIP_TARGET)
aliases['xxh'] = os.path.join($XXH_HOME, 'xonsh') + ' ' + os.path.join($XXH_HOME, 'xxh.xsh')

