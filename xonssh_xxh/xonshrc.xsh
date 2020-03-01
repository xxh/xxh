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
aliases['xpip'] = lambda args: ![echo "\n\033[0;33mTO INSTALL XONTRIBS USE: xontrib-install <package>\033[0m\n"] and ![pip @(args)]

def _xxh_xontrib_install(args, stdin, stdout): # https://github.com/xonsh/xonsh/issues/3463
    argp = argparse.ArgumentParser(description=f"Install xontribs", prog='xontrib-install')
    argp.add_argument('xontrib',help="pip package with xontrib")
    argp.add_argument('-f', '--force', default=False, action='store_true', help="Force install")
    argp.usage = argp.format_usage().replace('usage: ', '')
    opt = argp.parse_args(args)

    if !(pip search -q @(opt.xontrib)).returncode:
       print(f'pip search {opt.xontrib}: not found')
       return 1

    if not opt.force and opt.xontrib in $(pip list).split():
        print(f'pip list: {opt.xontrib} already installed, try -f option to force install')
        return 1

    if list($PIP_XONTRIB_TARGET.glob('*')):
        pip_xontrib_tmp = str($PIP_XONTRIB_TARGET) + '_'
        mv @($PIP_XONTRIB_TARGET) @(pip_xontrib_tmp)
        xpip install --upgrade @(opt.xontrib)
        mkdir -p @($PIP_XONTRIB_TARGET)
        bash -c $(echo mv @(pip_xontrib_tmp + '/*') @($PIP_XONTRIB_TARGET))
        rm -r @(pip_xontrib_tmp)
    else:
        xpip install --upgrade @(opt.xontrib)

aliases['xontrib-install'] = _xxh_xontrib_install
del _xxh_xontrib_install

for plugin_path in sorted(($XXH_HOME / 'plugins').glob('*')):
    if (plugin_path / 'xonshrc.xsh').exists():
        sys.path.append(str(plugin_path))
        __import__('xonshrc')
        del sys.modules['xonshrc']
        sys.path.remove(str(plugin_path))