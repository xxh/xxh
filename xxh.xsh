#!/usr/bin/env xonsh

import os, sys, glob, argparse

appimage_url = 'https://github.com/niess/linuxdeploy-plugin-python/releases/download/continuous/xonsh-x86_64.AppImage'
xonsh_bin = 'xonsh'
target_path = '~/.xxh'

argp = argparse.ArgumentParser(description='XXH is for using the Xonsh shell wherever you go through the SSH. Git: https://github.com/xonssh/xxh')
argp.add_argument('server', help="Destination may be specified as hostname or server name from ~/.ssh/config")
argp.add_argument('-i','--install', default=False, action='store_true', help="Install xonsh to host")
argp.add_argument('-p','--target-path', default=target_path, help="Target path. Default: %s" % target_path)
argp.add_argument('-m','--method', default='appimage', help="Currently supported single 'appimage' method")
argp.add_argument('-f','--force', default=False, action='store_true', help="Delete target directory when install xonsh to host")
opt = argp.parse_args()
srv = opt.server

xxh_home = os.path.dirname(os.path.realpath(__file__))

if opt.target_path == '~/.xxh':
    srv_user_home = $(ssh @(srv) -T "bash -c 'cd ~ && pwd'").strip()

    if srv_user_home == '':
        print('Unknown answer from server when checking user home path')
        sys.exit(1)

    srv_xxh_home = os.path.join(srv_user_home, '.xxh')
else:
    srv_xxh_home = opt.target_path

srv_xonsh_bin = os.path.join(srv_xxh_home, xonsh_bin)
srv_xonshrc = os.path.join( srv_xxh_home, 'xonshrc.xsh')
srv_xonsh_plugins_rc = os.path.join( srv_xxh_home, 'xonsh_plugins_rc.xsh')

srv_has_xxh = $(echo @("[[ -d %s ]] && echo -n 1 || echo -n 0" % srv_xxh_home) | ssh @(srv) -T "bash -s")

if srv_has_xxh not in ['0','1']:
    print('Unknown answer from server when checking direcotry %s: %s' % (srv_xxh_home, srv_has_xxh))
    sys.exit(1)

if not opt.install and srv_has_xxh == '0':
    yn = input("%s:%s not found. Install? [y/n] " % (srv, srv_xxh_home)).lower()
    if yn == 'y':
        opt.install = True
    else:
        sys.exit(1)

if opt.install:
    echo '\033[0;33mInstall'

    if opt.method == 'appimage':
        appimage_fullpath = os.path.join(xxh_home, xonsh_bin)
        if not os.path.isfile(appimage_fullpath):
            echo '\033[0;33mDownload xonsh appimage'
            wget -q --show-progress @(appimage_url) -O @(appimage_fullpath)
            chmod +x @(appimage_fullpath)
    else:
        print('Method "%s" is not supported now' % opt.method)

    if srv_has_xxh == "1":
        if opt.force:
            echo 'Remove target directory' @(srv):@(srv_xxh_home)
            echo @("rm -rf %s" % srv_xxh_home ) | ssh -o LogLevel=QUIET @(srv) -T "bash -s"
        else:
            print('Target directory exists: %s' % srv_xxh_home)
            sys.exit(1)

    echo Upload files to @(srv)
    rsync  -az --info=progress2 --include ".*" @(xxh_home)/ @(srv):@(srv_xxh_home)/

    plugins_dir = 'plugins'
    plugins_fullpath = os.path.join(xxh_home, plugins_dir)
    if os.path.exists(plugins_fullpath):
        echo Run plugins post install on @(srv)
        scripts=''
        for script in sorted(glob.glob(os.path.join(plugins_fullpath, os.path.join('*','install.xsh')), recursive=True)):
            scripts += " && %s -i --rc %s -- %s" % (srv_xonsh_bin, srv_xonshrc, script.replace(xxh_home + os.sep, ''))
            print(' * %s' % script)

        if scripts:
            echo @("cd %s %s" % (srv_xxh_home, scripts) ) | ssh -o LogLevel=QUIET @(srv) -T "bash -s"

    echo First run xonsh on @(srv)
    echo -n '\033[0m'

srv_plugins_rc = $(ssh -o LogLevel=QUIET @(srv) -t @(srv_xonsh_bin) -i --rc @(srv_xonshrc) -- @(srv_xonsh_plugins_rc)).split()
ssh -o LogLevel=QUIET @(srv) -t @(srv_xonsh_bin) -i --rc @(srv_xonshrc) @(srv_plugins_rc)
