import sys

$UPDATE_OS_ENVIRON=True
del $LS_COLORS # https://github.com/xonsh/xonsh/issues/3055
$XXH_HOME = pf"{__file__}".absolute().parent
$PIP_TARGET = $XXH_HOME / 'pip'
$PYTHONPATH = $PIP_TARGET
$PATH = [ p"$PYTHONHOME" / 'bin', $XXH_HOME ] + $PATH
sys.path.append(str($PIP_TARGET))
sys.path.remove('') if '' in sys.path else None
aliases['pip'] = ['python','-m','pip']
aliases['xpip'] = aliases['pip']

for plugin_path in sorted(($XXH_HOME / 'plugins').glob('*')):
    if (plugin_path / 'xonshrc.xsh').exists():
        sys.path.append(str(plugin_path))
        __import__('xonshrc')
        del sys.modules['xonshrc']
        sys.path.remove(str(plugin_path))