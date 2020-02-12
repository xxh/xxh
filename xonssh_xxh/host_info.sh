#!/bin/bash

xxh_home_realpath=`realpath _xxh_home_`
mkdir -p $xxh_home_realpath

settings_path=$xxh_home_realpath/settings.py
xxh_version=`[ "$(ls -A $xxh_home_realpath)" ] && echo "0" || echo "-1"`
if [[ -f $settings_path ]]; then
    xxh_version=`cat $settings_path | grep XXH_VERSION | sed -e "s/.*: '\(.*\)'/\\1/g"`
fi

echo xxh_home_realpath=$xxh_home_realpath
echo xxh_version=$xxh_version
echo bash=`command -v bash`
echo rsync=`command -v rsync`
echo scp=`command -v scp`