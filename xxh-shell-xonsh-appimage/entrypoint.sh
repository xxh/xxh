#!/bin/bash

CURRENT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd $CURRENT_DIR

# Check FUSE support
check_result=`./xonsh --no-script-cache -i --rc xonshrc.xsh -- settings.py 2>&1`
if [[ ! -f xonsh-check-done ]]; then
  if [[ $check_result == *"AppImages require FUSE"* ]]; then
    echo "Extract AppImage" 1>&2
    ./xonsh --appimage-extract > /dev/null # TODO: verbose mode
    mv squashfs-root xonsh-squashfs
    mv xonsh xonsh-disabled
    ln -s ./xonsh-squashfs/usr/bin/python3 xonsh
  fi
  echo $check_result > xonsh-check-done
fi

./xonsh --no-script-cache -i --rc xonshrc.xsh #TODO: @(host_execute_file)