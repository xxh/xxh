#!/bin/bash

ln -s /root /home/root

cat >/home/root/.bash_history <<EOL
su ubash
su ufish
su uzsh
su uxonsh
sshpass -p docker ssh docker@arch_p
xxh docker@arch_p +P docker
ssh -i ~/id_rsa root@ubuntu_k
xxh -i ~/id_rsa root@ubuntu_k
ssh -i ~/id_rsa root@ubuntu_kf
xxh -i ~/id_rsa root@ubuntu_kf
EOL

for user_dir in /home/*; do
  username=`basename $user_dir`
  echo Prepare $user_dir

  cd $user_dir
  cp /home/root/.bash_history .

  if [[ $username == *"root"* ]]; then
    echo 'export PATH=/xxh/xxh:$PATH' >> .bashrc
  elif [[ $username == *"bash"* ]]; then
    # https://github.com/ohmybash/oh-my-bash#manual-installation
    git clone --depth 1 https://github.com/ohmybash/oh-my-bash .oh-my-bash
    cp .bashrc .bashrc.orig
    cp .oh-my-bash/templates/bashrc.osh-template .bashrc
    sed -i -e 's/font/powerline/g' .bashrc
    echo 'export PATH=/xxh/xxh:$PATH' >> .bashrc

  elif [[ $username == *"xonsh"* ]]; then
    echo '$PATH=["/xxh/xxh"]+$PATH' >> .xonshrc
  elif [[ $username == *"zsh"* ]]; then
    # https://github.com/ohmyzsh/ohmyzsh/#manual-installation
    git clone --depth 1 https://github.com/ohmyzsh/ohmyzsh.git .oh-my-zsh
    cp .oh-my-zsh/templates/zshrc.zsh-template .zshrc
    sed -i -e 's/robbyrussell/agnoster/g' .zshrc
    sed -i -e 's/(git/(git docker ubuntu/g' .zshrc

    echo 'export PATH=/xxh/xxh:$PATH' >> .zshrc

  elif [[ $username == *"fish"* ]]; then
    mkdir -p .config/fish/
    echo 'set PATH /xxh/xxh $PATH' >> .config/fish/config.fish
  fi

  chown -R $username:$username $user_dir

done
