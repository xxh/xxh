#!/usr/bin/env bash

SHELL=${1:-bash}

VAGRANT_IP="$(VBoxManage showvminfo $(cat .vagrant/machines/default/virtualbox/id) --details  | grep 'name = ssh' | cut -b 18- | egrep -o 'host ip = [0-9.]*' | cut -b 11-)"
VAGRANT_PORT="$(VBoxManage showvminfo $(cat .vagrant/machines/default/virtualbox/id) --details  | grep 'name = ssh' | cut -b 18- | egrep -o 'host port = [0-9]*' | cut -b 13-
)"
SSH="-i .vagrant/machines/default/virtualbox/private_key -o PasswordAuthentication=no vagrant@$VAGRANT_IP -p $VAGRANT_PORT"

TESTING=""
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

for item in $(shopt -s dotglob && cd $CURR_DIR && find . -type d -name 'xxh-*'); do
    TODO="$(basename $item)"
    TESTING="+RI $TODO+path+$CURR_DIR/$TODO $TESTING"
done

echo "Starting with params: $TESTING"
ssh $SSH "ls -l"
if [ $? != 0 ]; then
    ssh-keygen -f "$HOME/.ssh/known_hosts" -R "[$VAGRANT_IP]:$VAGRANT_PORT"
fi

xxh $SSH +s $SHELL $TESTING
