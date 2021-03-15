# Xxh Development Environment (xde)

Development and test environment for [xxh/xxh](https://github.com/xxh/xxh) contains 
network of docker containers which allow to test the ssh connections and xxh functionality 
with or without [FUSE](https://github.com/AppImage/AppImageKit/wiki/FUSE). 

## Workflow

This workflow was originally developed on `ubuntu 20.04`, `docker 19.03.5`, `docker-compose 1.25.3`, `xonsh 0.9.14`, `pycharm 2019.3.3`.

1. Create base environment:
```bash
apt install -y docker git  # Or install docker from official repo - https://docs.docker.com/engine/install/ubuntu/
mkdir -p ~/git && cd ~/git
git clone https://github.com/xxh/xxh
cd xxh/xde
pip install -r requirements.txt
./xde build             # build docker containers
./xde up                # run docker containers
./xde test              # run tests first time
```

2. Open `~/git/xxh` in your IDE to make changes and commit.
3. Now you can go to `start` host and try your first connect using xxh:
```shell script
./xde goto start

# Press UP key to get connection strings to other hosts from bash history.
# Here xxh will be from /xxh/xxh/ that is your local  directory
#root@start> 
xxh -i ~/id_rsa root@ubuntu_k

#root@start> #Try from another shell:
su uzsh
#uzsh@start> 
xxh +I xxh-plugin-zsh-ohmyzsh
#uzsh@start> 
xxh -i ~/id_rsa root@ubuntu_k
#root@ubuntu_k% 
echo $ZSH_THEME && exit
#agnoster
#uzsh@start> 
source xxh.zsh -i ~/id_rsa root@ubuntu_k
#root@ubuntu_k% 
echo $ZSH_THEME
#bira
```

4. Change the code in IDE and run `xxh` on `start` container. It's so easy!
5. Run tests `./xde t` (don't forget about `./xde t --help` and fast mode `./xde t -sr`) 
6. After end of work you can `./xde stop` or `./xde remove` the containers. 
7. You rock! Try to find easter egg in the xxh code now.

## Docker containers in the network

| Hostname  | Auth             | FUSE | rsync | users                            |
|-----------|------------------|------|-------|----------------------------------|
| start     | `./xde g start`  |      |       | `root`, `uxonsh`, `uzsh`, `ufish`, `ubash` |
| ubuntu_k  | key              |      |       | `root`                           |
| ubuntu_kf | key              | yes  |  yes  | `root`                           |
| centos_k  | key              |      |       | `root`                           |
| arch_p    | password         |      |       | `root`, `docker`                 |

Every container has `/xxh` it is the volume. For example if you'll add a file to `tests/new.xsh` 
it appears on all hosts immediately in `/xxh/xde/tests/new.xsh`.

## xxh development environment tool

```shell script
./xde -h
#usage: xde <command>
#
#xxh development environment commands:
#
#   clone       Git clone repos from https://github.com/xxh
#   build       Build the docker containers and get the xxh code if ./xxh is not exists
#   up          Docker-compose up the containers
#   test    t   Run tests
#   goto    g   Open bash by the container name part
#   start       Docker-compose start the containers
#   stop        Docker-compose stop the containers
#   remove      Docker-compose remove the containers
#   
#Try `./xde <command> --help` to get more info.   
#   
#positional arguments:
#  command     Command to run
#
#optional arguments:
#  -h, --help  show this help message and exit

```
