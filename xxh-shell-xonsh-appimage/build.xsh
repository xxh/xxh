#!/usr/bin/env xonsh

from sys import exit
from shutil import which

url_appimage = 'https://github.com/niess/linuxdeploy-plugin-python/releases/download/continuous/xonsh-x86_64.AppImage'

script_dir = pf"{__file__}".absolute().parent
build_dir = script_dir / 'build'
rm -rf @(build_dir)/
mkdir -p @(build_dir)

cp @(script_dir / 'entrypoint.sh') @(build_dir)/

cd @(build_dir)
if not p'xonsh'.is_file():
    print(f'Download xonsh AppImage from {url_appimage}')
    if which('wget'):
        r =![wget -q --show-progress @(url_appimage) -O xonsh]
        if r.returncode != 0:
            print(f'Error while download appimage using wget: {r}')
            exit(1)
    elif which('curl'):
        r =![curl @(url_appimage) -o xonsh]
        if r.returncode != 0:
            print(f'Error while download appimage using curl: {r}')
            exit(1)
    else:
        print('Please install wget or curl and try again. Howto: https://duckduckgo.com/?q=how+to+install+wget+in+linux')
        exit(1)

    chmod +x xonsh
else:
    print('Skip xonsh downloading')
