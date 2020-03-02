#!/usr/bin/env xonsh

from sys import exit
from shutil import which

current_dir = pf"{__file__}".absolute().parent
url_appimage = 'https://github.com/niess/linuxdeploy-plugin-python/releases/download/continuous/xonsh-x86_64.AppImage'

xonsh_appimage_path = current_dir / 'xonsh'
if not xonsh_appimage_path.is_file():
    print(f'First time download and save xonsh AppImage from {url_appimage}')
    if which('wget'):
        r =![wget -q --show-progress @(url_appimage) -O @(xonsh_appimage_path)]
        if r.returncode != 0:
            print(f'Error while download appimage using wget: {r}')
            exit(1)
    elif which('curl'):
        r =![curl @(url_appimage) -o @(xonsh_appimage_path)]
        if r.returncode != 0:
            print(f'Error while download appimage using curl: {r}')
            exit(1)
    else:
        print('Please install wget or curl and try again. Howto: https://duckduckgo.com/?q=how+to+install+wget+in+linux')
        exit(1)

    chmod +x @(xonsh_appimage_path)
