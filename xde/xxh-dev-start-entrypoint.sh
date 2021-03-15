#!/bin/bash

for user_dir in /home/*; do
  username=`basename $user_dir`
  echo Prepare $user_dir

  cd $user_dir

  cp /xxh/xde/keys/id_rsa .
  chown $username:$username id_rsa
  chmod 0600 id_rsa
done

tail -f /dev/null
