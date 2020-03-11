#!/bin/bash

xxh_home_realpath=`realpath -m _xxh_home_`

xxh_version='dir_not_found'
if [[ -d $xxh_home_realpath ]]; then
    xxh_version=`[ "$(ls -A $xxh_home_realpath)" ] && echo "version_not_found" || echo "dir_empty"`
    settings_path=$xxh_home_realpath/xxh/package/settings.py
    if [[ -f $settings_path ]]; then
        xxh_version=`cat $settings_path | grep XXH_VERSION | sed -e "s/.*: '\(.*\)'/\\1/g"`
    fi
fi

echo xxh_home_realpath=$xxh_home_realpath
echo xxh_version=$xxh_version
echo xxh_shell_exists=`[ -d $xxh_home_realpath/xxh/shells/_xxh_shell_ ] && echo "1" ||echo "0"`
echo xxh_home_writable=`[ -w $xxh_home_realpath ] && echo "1" ||echo "0"`
echo xxh_parent_home_writable=`[ -w $(dirname $xxh_home_realpath) ] && echo "1" ||echo "0"`
echo rsync=`command -v rsync`
echo scp=`command -v scp`
