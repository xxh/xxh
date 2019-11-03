**xxh plugins** - is the set of files which will be run when xonsh will be installed or started though xxh.

## Install xxh plugin

To install xxh plugin just place the folder to this directory.

Example:
```xonsh
cd ~/.xxh/plugins/
git clone --depth 1 https://github.com/xonssh/xxh-plugin-theme-bar
xxh server
```

## xxh plugins list

* [Bar Theme](https://github.com/xonssh/xxh-plugin-theme-bar)
* [Autojump](https://github.com/xonssh/xxh-plugin-autojump)

[Search more plugins on Github](https://github.com/search?q=xxh-plugin)

## Create xxh plugin

To create xxh plugin you can create directory in `~/.xxh` (by default) on your home host with files:
* `install.xsh` will be executed once after xxh installation on the host
* `xonshrc.xsh` will be executed every time you'll be connect via xxh to the host
