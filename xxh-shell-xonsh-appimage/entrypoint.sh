#!/bin/bash

while getopts f:c:v: option
do
case "${option}"
in
f) EXECUTE_FILE=${OPTARG};;
# c) EXECUTE_COMMAND=${OPTARG};;  # https://github.com/xonssh/xxh/issues/36
f) VERBOSE=${OPTARG};;  # TODO: verbose mode
esac
done

EXECUTE_FILE=`[ $EXECUTE_FILE ] && echo -n "-- $EXECUTE_FILE" || echo -n ""`

CURRENT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd $CURRENT_DIR

# Check FUSE support
check_result=`./xonsh --no-script-cache -i --rc xonshrc.xsh -- settings.py 2>&1`
if [[ ! -f xonsh-check-done ]]; then
  if [[ $check_result == *"AppImages require FUSE"* ]]; then
    #echo "Extract AppImage" 1>&2  # TODO: verbose mode
    ./xonsh --appimage-extract > /dev/null # TODO: verbose mode
    mv squashfs-root xonsh-squashfs
    mv xonsh xonsh-disabled
    ln -s ./xonsh-squashfs/usr/bin/python3 xonsh
  fi
  echo $check_result > xonsh-check-done
fi

./xonsh --no-script-cache -i --rc xonshrc.xsh $EXECUTE_FILE

# host_execute_file = ['--', opt.host_execute_file] if opt.host_execute_file else []