<p align="center">
  <img src="https://avatars2.githubusercontent.com/u/57318034?s=60&v=4&"><br>
  <p align="center">
    <b>xxh</b> is for using portable <a href="https://xon.sh/">xonsh shell</a> wherever you go through the SSH.
  </p>
</p>
<br>
<p align="center">  
  <a href="https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7" target="_blank"><img src="https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7.svg"></a>
</p>

<p align="center">  
  <a href="https://pypi.org/project/xonssh-xxh/" target="_blank" alt="PyPI Latest Release"><img src="https://img.shields.io/pypi/v/xonssh-xxh.svg"></a>
</p>

## Installation
```
pip install xonssh-xxh
```
Then try:
```
xxh <hostname or servername from ~/.ssh/config>
```

## Usage
```
$ xxh -h
usage: xxh [-h] [-i] [-if] [-rxh REMOTE_XXH_HOME] [-m METHOD]
           [-lxh LOCAL_XXH_HOME] [-V]
           [destination]

The xxh is for using the xonsh shell wherever you go through the ssh. 

      ___  _________     @    @    
   _____  /         \     \__/     
    ___  /   ____    \   /   \           contribution
  ____  /   /    \    \ /   _/   https://github.com/xonssh/xxh   
    __ (    \  \_/     )   /          
        \    \_____/  /   /                plugins            
       __\___________/   /   https://github.com/search?q=xxh-plugin
      /_________________/       

positional arguments:
  destination           Destination may be specified as hostname or server name from ~/.ssh/config

optional arguments:
  -h, --help            show this help message and exit
  -i, --install         Install xxh to distanation host
  -if, --install-force  Delete remote xxh home and install xonsh to distanation host
  -rxh REMOTE_XXH_HOME, --remote-xxh-home REMOTE_XXH_HOME
                        Set the remote xxh home directory. Default: ~/.xxh
  -m METHOD, --method METHOD
                        Installation method. Currently supported only 'appimage' method
  -lxh LOCAL_XXH_HOME, --local-xxh-home LOCAL_XXH_HOME
                        Local xxh home path. Default: ~/.xxh
  -V, --version         Show xxh version
```

## Plugins

[Search xxh plugins on Github](https://github.com/search?q=xxh-plugin) or [create plugin with your own lovely functions](README.plugins.md).

## Notes

### Using pip and python

The xxh xonsh will use pip and python from `xonsh.AppImage` by default. You can install pip packages ordinally with `pip install`. They will appear in `$XXH_HOME/pip`.

### Shortcut to reinstall xxh on host
```
xxh <server> -if
```

## How it works?

When you run `xxh <server>` command:

1. If it needed xxh script will download `xonsh.AppImage`. This is portable version of xonsh. URL you can find in `xxh.xsh`

2. If it needed xxh script copies the portable xonsh on the host (`~/.xxh` by default) along with init scripts and plugins.

3. Finally xxh makes ssh connection to server and running remote portable xonsh shell without any affection on the target system.

# Thanks

* @niess for https://github.com/niess/linuxdeploy-plugin-python/
* @gforsyth for https://github.com/xonsh/xonsh/issues/3374
* @scopatz for https://github.com/xonsh/xonsh

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
