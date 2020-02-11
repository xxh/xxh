<p align="center">
  <img src="https://avatars2.githubusercontent.com/u/57318034?s=60&v=4&"><br>
  <p align="center">
    <b>xxh</b> is for using <a href="https://xon.sh/">xonsh shell</a> wherever you go through the ssh.
  </p>
</p>
<p align="center">  
  <a href="https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7" target="_blank"><img src="https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7.svg"></a><br>
<sup>(in the demo is used <a href="https://github.com/xonssh/xxh-plugin-theme-bar">xxh-plugin-theme-bar</a>)</sup>
</p>
<br>
<p align="center">  
  <a href="https://pypi.org/project/xonssh-xxh/" target="_blank" alt="PyPI Latest Release"><img src="https://img.shields.io/pypi/v/xonssh-xxh.svg"></a>
 <img alt="PyPI - License" src="https://img.shields.io/pypi/l/xonssh-xxh">
  
</p>

## Installation
```
pip install xonssh-xxh
```
Then try:
```
xxh <[user@]host[:port] or servername from ~/.ssh/config>
```

## Usage
```
$ ./xxh --help                                                                                                                                                                                                                         
usage: xxh [user@]host[:port]

usage: xxh [ssh arguments] destination [xxh arguments]

usage: xxh [-h] [-V] [-p SSH_PORT] [-l SSH_LOGIN_NAME] [-i SSH_IDENTITY_FILE]
           [-o SSH_OPTIONS] [+i] [+if] [+lxh LOCAL_XXH_HOME]
           [+rxh REMOTE_XXH_HOME] [+m METHOD] [+v]
           [destination]

The xxh is for using the xonsh shell wherever you go through the ssh. 

      ___  __________     @    _    
   _____  /          \     \__/     
    ___  /    ______  \   /   \           contribution
  ____  /    / __   \  \ /   _/   https://github.com/xonssh/xxh   
    __ (    / /  /   \  \   /          
        \   \___/    /  /  /                plugins            
     ____\          /__/  /   https://github.com/search?q=xxh-plugin
    /     \________/     /                           
   /____________________/       

required arguments:
  destination           Destination may be specified as [user@]hostname[:port] or server name from ~/.ssh/config

common arguments:
  -h, --help            show this help message and exit
  -V, --version         Show xxh version

ssh arguments:
  -p SSH_PORT           Port to connect to on the remote host.
  -l SSH_LOGIN_NAME     Specifies the user to log in as on the remote machine.
  -i SSH_IDENTITY_FILE  Selects a file from which the identity (private key) for public key authentication is read.
  -o SSH_OPTIONS        Options in the ssh configuration format. See ssh man page. Example: xxh -o Port=22 -o User=snail host

xxh arguments:
  +i, ++install         Install xxh to distanation host.
  +if, ++install-force  Delete remote xxh home and install xonsh to distanation host.
  +lxh LOCAL_XXH_HOME, ++local-xxh-home LOCAL_XXH_HOME
                        Local xxh home path. Default: ~/.xxh
  +rxh REMOTE_XXH_HOME, ++remote-xxh-home REMOTE_XXH_HOME
                        Remote xxh home path. Default: ~/.xxh
  +m METHOD, ++method METHOD
                        Installation method: appimage
  +v, ++verbose         Verbose mode.
```

## Plugins

[Search xxh plugins on Github](https://github.com/search?q=xxh-plugin&type=Repositories) or [create plugin with your own lovely functions](README.plugins.md).

Pinned plugins:

* [Pipe Liner](https://github.com/xonssh/xxh-plugin-pipe-liner) — processing the lines easy with python and classic shell pipes
* [Bar Theme](https://github.com/xonssh/xxh-plugin-theme-bar) — theme to stay focused
* [Autojump](https://github.com/xonssh/xxh-plugin-autojump) — save time on moving thru directories

## Notes

### Using pip and python

The xxh xonsh will use pip and python from `xonsh.AppImage` by default. You can install pip packages ordinally with `pip install`. They will appear in `$XXH_HOME/pip`.

## How it works?

When you run `xxh <server>` command:

1. If it needed xxh script will download `xonsh.AppImage`. This is portable version of xonsh. URL you can find in `xxh.xsh`

2. If it needed xxh script copies the portable xonsh on the host (`~/.xxh` by default) along with init scripts and plugins.

3. Finally xxh makes ssh connection to server and running remote portable xonsh shell without any affection on the target system.

## Known Issues

### GLIBs versions

Current method to make xonsh portable is using an [AppImage](https://appimage.org/) which was built on [manylinux2010 (PEP 571)](https://github.com/niess/linuxdeploy-plugin-python/issues/12). In case you see the error like ``/xonsh-x86_64.AppImage: /lib/x86_64-linux-gnu/libc.so.6: version GLIBC_2.25 not found (required by /ppp/xonsh-x86_64.AppImage)`` this means you should rebuild the AppImage for older version of linux distributive. Try [linuxdeploy-plugin-python](https://github.com/niess/linuxdeploy-plugin-python/).

### WSL1: ^Z

```
# xxh YT-1300
^Z
Unknown answer from server when checking direcotry /home/hansolo/.xxh:
```
This issue was addressed to Xonsh team in [3367](https://github.com/xonsh/xonsh/issues/3367). Just try to run command again.

WSL2 is not tested yet.

## Thanks
* @scopatz for https://github.com/xonsh/xonsh
* @probonopd for https://github.com/AppImage
* @niess for https://github.com/niess/linuxdeploy-plugin-python/
* @gforsyth for https://github.com/xonsh/xonsh/issues/3374
