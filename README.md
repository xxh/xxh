**xxh** is for using portable Xonsh shell wherever you go through the SSH.

[![asciicast](https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7.svg)](https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7)

## Installation
```
xonsh> cd ~
xonsh> git clone --depth 1 https://github.com/xonssh/xxh ~/.xxh
xonsh> echo "aliases['xxh'] = 'xonsh ~/.xxh/xxh.xsh'" >> ~/.xonshrc
xonsh> aliases['xxh'] = 'xonsh ~/.xxh/xxh.xsh'

xonsh> xxh server
```

## Usage
```
> xxh -h
usage: xxh.xsh [-h] [-i] [-p TARGET_PATH] [-m METHOD] [-f] server

positional arguments:
  server                Destination may be specified as hostname or server
                        name from ~/.ssh/config

optional arguments:
  -h, --help            show this help message and exit
  -i, --install         Install xonsh to host
  -p TARGET_PATH, --target-path TARGET_PATH
                        Target path. Default: ~/.xxh
  -m METHOD, --method METHOD
                        Currently supported single 'appimage' method
  -f, --force           Delete target directory when install xonsh to host
```

## Plugins

You can [add plugins to xxh](plugins/README.md).

## Notes

### Using pip and python

The xxh xonsh will use pip and python from `xonsh.AppImage` by default.

You can install pip packages ordinally with `pip install`. They will appear in `$XXH_HOME/pip`.

### Shortcut for reinstall xxh on host
```
xxh server -i -f
```

## Known Issues

### WSL1: ^Z

```
# xxh YT-1300
^Z
Unknown answer from server when checking direcotry /home/hansolo/.xxh:
```
This issue was addressed to Xonsh team in [3367](https://github.com/xonsh/xonsh/issues/3367)

## How it works?

When you run `xxh server` command:

1. If it needed xxh script will download `xonsh.AppImage`. This is portable version of xonsh. URL you can find in `xxh.xsh`

2. If it needed xxh script copies the portable xonsh on the host (`~/.xxh` by default) along with init scripts and plugins.

3. Finally xxh makes ssh connection to server and running remote portable xonsh shell without any affection on of system.
