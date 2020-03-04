import sys, argparse

del $LS_COLORS # https://github.com/xonsh/xonsh/issues/3055

$UPDATE_OS_ENVIRON=True
$XXH_HOME = pf"{__file__}".absolute().parent

$PIP_TARGET = $XXH_HOME / 'pip'
$PIP_XONTRIB_TARGET = $PIP_TARGET / 'xontrib'
if not $PIP_XONTRIB_TARGET.exists():
    mkdir -p @($PIP_XONTRIB_TARGET)

$PYTHONPATH = $PIP_TARGET
$PATH = [ p"$PYTHONHOME" / 'bin', $XXH_HOME ] + $PATH
sys.path.append(str($PIP_TARGET))
sys.path.remove('') if '' in sys.path else None
aliases['pip'] = ['python','-m','pip']

def _xxh_pip(args): # https://github.com/xonsh/xonsh/issues/3463
    if args and 'install' in args and '-h' not in args and '--help' not in args:
        print('\033[0;33mRun xpip in xontrib safe mode\033[0m')
        pip_xontrib_tmp = $PIP_XONTRIB_TARGET.parent / 'xontrib-safe'
        mv @($PIP_XONTRIB_TARGET) @(pip_xontrib_tmp)
        pip @(args)
        mkdir -p @($PIP_XONTRIB_TARGET)
        if list(pip_xontrib_tmp.glob('*')):
            bash -c $(echo mv @(pip_xontrib_tmp / '*') @($PIP_XONTRIB_TARGET))
        rm -r @(pip_xontrib_tmp)
    else:
        pip @(args)

aliases['xpip'] = _xxh_pip
del _xxh_pip

for plugin_path in sorted(($XXH_HOME / 'plugins').glob('*')):
    if (plugin_path / 'xonshrc.xsh').exists():
        cd @(plugin_path)
        sys_path = sys.path
        sys.path = [str(plugin_path)]
        __import__('xonshrc')
        del sys.modules['xonshrc']
        sys.path = sys_path
cd