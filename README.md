<p align="center">You chosen a command shell and spent months to stuffed it with shortcuts and colors. But when you move from local to remote host using ssh you lose it all. The mission of xxh is to bring your favorite shell wherever you go through the ssh.</p>
<p align="center">  
  <a href="https://pypi.org/project/xxh-xxh/" target="_blank"><img src="https://img.shields.io/pypi/v/xxh-xxh.svg" alt="[release]"></a>
  <a href="https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7" target="_blank"><img alt="[demo xonsh]" src="https://img.shields.io/badge/demo-xonsh-grass"></a>
  <a href="https://asciinema.org/a/rCiT9hXQ5IdwqOwg6rifyFZzb" target="_blank"><img alt="[demo zsh]" src="https://img.shields.io/badge/demo-zsh-grass"></a>
  <a href="#plugins" target="_blank"><img alt="[plugins]" src="https://img.shields.io/badge/extensions-plugins-yellow"></a>
  <a href="https://gitter.im/xxh-xxh/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge" target="_blank"><img alt="[gitter chat]" src="https://badges.gitter.im/xxh-xxh/community.svg"></a>
  <img alt="[BSD license]" src="https://img.shields.io/pypi/l/xxh-xxh">
</p>

## Install or update
```shell script
pip install -U xxh-xxh
```

## Usage
Use `xxh` as replace `ssh` to connecting to the host. Seamless support of basic ssh arguments. 

```
$ ./xxh -h 
usage: xxh <host from ~/.ssh/config>
usage: xxh [ssh arguments] [user@]host[:port] [xxh arguments]
usage: xxh [-p SSH_PORT] [-l SSH_LOGIN] [-i SSH_PRIVATE_KEY]
           [-o SSH_OPTION -o ...] [+P PASSWORD] [+PP]
           [user@]host[:port]
           [+i] [+if] [+s SHELL] [+e NAME=VAL +e ...] [+iff] [+hhr]
           [+hh HOST_XXH_HOME] [+hf HOST_EXEC_FILE] [+hc HOST_EXEC_CMD]
           [+xc XXH_CONFIG] [+lh LOCAL_XXH_HOME] [+v] [+vv] [+q]

usage: xxh [+I xxh-package ...] [+L] [+RI xxh-package ...] [+R xxh-package ...]
```

There is `~/.xxh/.xxhc` [yaml](https://en.wikipedia.org/wiki/YAML) config to save arguments and reuse it:
```yaml
hosts:
  myhost:                     # settings for myhost
    -p: 2222                    # set special port
    +s: xxh-shell-zsh           # set zsh shell                         
    +I: xxh-plugin-zsh-ohmyzsh  # install xxh-plugin before connect
    +e: ZSH_THEME="clean"       # set ohmyzsh theme

  "company-.*":        # for all hosts by regex pattern
    +if:                 # don't asking about install (++install-force)
    +hh: /tmp/.xxh       # use special xxh home directory (++host-xxh-home)
    +hhr:                # remove host xxh home after disconnect (++host-xxh-home-remove)
```
The arguments will be automatically added when you run `xxh myhost` or `xxh company-server1`.

## Supported shells
**[Xonsh](https://github.com/xxh/xxh-shell-xonsh-appimage)** — stable version with [pipeliner](https://github.com/xxh/xxh-plugin-xonsh-pipe-liner), [bar](https://github.com/xxh/xxh-plugin-xonsh-theme-bar), [autojump](https://github.com/xxh/xxh-plugin-xonsh-autojump) plugins. 

**[Zsh](https://github.com/xxh/xxh-shell-zsh)** — beta version with [Oh My Zsh](https://github.com/xxh/xxh-plugin-zsh-ohmyzsh) and [powerlevel10k](https://github.com/xxh/xxh-plugin-zsh-powerlevel10k) plugins, waiting for feedback.

**[osquery](https://github.com/xxh/xxh-shell-osquery)** — beta version, waiting for feedback.

**[Fish](https://github.com/xxh/xxh-shell-fish-appimage)** — alpha version, waiting for feedback.

**[Bash](https://github.com/xxh/xxh-shell-bash-zero)** — zero version that just runs bash installed on the host with plugins like [vim](https://github.com/xxh/xxh-plugin-bash-vim). 

[Search xxh shell on Github](https://github.com/search?q=xxh-shell&type=Repositories) or [Bitbucket](https://bitbucket.org/repo/all?name=xxh-shell) or [create your shell entrypoint](https://github.com/xxh/xxh-shell-sample) to use another portable shell. 

## The ideas behind xxh
* **Avoid building on remote host**. The security and careful about environment on the host are behind it. This could be the optional future feature but not now. 
* **No blindfold copying** config files from local to remote host. The privacy and repeatability reasons are behind it. Every xxh package, shell or plugin is the bridge that use only what required, no more.
* **Portable means clean**. If you delete `~/.xxh` directory from the remote host then xxh has never been on the host. Some temporary files of third party tools you use could be in the home directory after usage but we stand for moving them to the xxh home directory. Feel free to report about this cases.
* **Be fork-ready**. Every repo could be forked, customize and used without affection on package management system, xxh releases or any third party lags.
* **Do more**. The xxh packages are not only about shells. Any type of tool or code could be behind "shell entrypoint". If you want to play Super Mario on the remote host just put it as entrypoint.
* **Be open**. Currently supported four shells and the count could be grow by community.

## Q&A

**What is plugin?** It is the set of scripts which will be run on the host when you go using xxh. It could be shell settings, environment variables, plugins, color themes and everything you need. You can find the links to plugins on [xxh-shells repos](https://github.com/search?q=xxh%2Fxxh-shell&type=Repositories). Feel free to fork it.

**How it works?** When you run `xxh myhost` command xxh download portable shell and store locally to future use. Then if it needed xxh upload the portable shell, init scripts and plugins to the host. Finally xxh make ssh connection to the host and run portable shell without any system installs and affection on the target host.

**What about speed?** The first connection takes time for downloading and uploading portable shell. It depends on portable shell size and channel speed. But when xxh is installed on the host and you do just `xxh myhost` then it works as ordinary ssh connection speed. You could monitor all process using `+vv` argument.

**What if my `host_internal` can be reached only from my `host_external`?** Add `ProxyCommand` or `ProxyJump` to your ssh config [as described](https://superuser.com/questions/96489/an-ssh-tunnel-via-multiple-hops#answer-170592) and then do ordinary `xxh host_internal`.

## Use cases
### Python everywhere with xonsh
When you run `xxh myhost +s xonsh` you'll get portable python, pip and python-powered shell on the host without any system installations on the host. Add plugins: [autojump](https://github.com/xxh/xxh-plugin-xonsh-autojump) saves time, [pipeliner](https://github.com/xxh/xxh-plugin-xonsh-pipe-liner) manipulates lines and [bar](https://github.com/xxh/xxh-plugin-xonsh-theme-bar) looks nice. 

### Oh My Zsh seamless SSH ([demo](https://asciinema.org/a/rCiT9hXQ5IdwqOwg6rifyFZzb))
```shell script
source xxh.zsh myhost +I xxh-plugin-zsh-ohmyzsh +if +q 
```
This command brings your current Oh My Zsh session theme to the xxh session. If you need more complex settings just fork the [xxh-plugin-zsh-ohmyzsh](https://github.com/xxh/xxh-plugin-zsh-ohmyzsh) and hack it.

### Read host as a table with osquery
```
$ xxh myhost +s osquery
osquery> SELECT * FROM users WHERE username='news';
+-----+-----+----------+-------------+-----------------+-------------------+
| uid | gid | username | description | directory       | shell             |
+-----+-----+----------+-------------+-----------------+-------------------+
| 9   | 9   | news     | news        | /var/spool/news | /usr/sbin/nologin |
+-----+-----+----------+-------------+-----------------+-------------------+
```   

### All in one portable home
The xxh is very agile. You can create your own `xxh-shell` (shell word means it has entrypoint) which has any portable tools
that you could help you on the host. [Bash-zero](https://github.com/xxh/xxh-shell-bash-zero) xxh-shell is one of this platforms that could be forked and stuffed.

## Development
In the [xxh-dev](https://github.com/xxh/xxh-dev) repo there is full [docker](https://www.docker.com/)ised environment for development, testing and contribution. The process of testing and development is orchestrated by `xde` tool and as easy as possible.

## Community
**Spread the word!** If you like the idea of xxh click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Python-powered%20shell%20wherever%20you%20go%20through%20the%20ssh&url=https%3A%2F%2Fgithub.com%2Fxxh%2Fxxh&related=" target="_blank">tweet the link</a>. 

**We have teams.** If you're in team it does not oblige to do something. The main goal of teams is to create group of passionate people who could help or support in complex questions. Some people could be expert in one shell and newbie in another shell and mutual assistance is the key to xxh evolution. [Ask join.](https://github.com/xxh/xxh/issues/50)

## Thanks
* **niess** for great [linuxdeploy-plugin-python](https://github.com/niess/linuxdeploy-plugin-python/) 
* **probonopd** and **TheAssassin** for hard-working [AppImage](https://github.com/AppImage)
* **Roman Perepelitsa** for incredible [statically-linked, hermetic, relocatable Zsh](https://github.com/romkatv/zsh-bin) 
* **Anthony Scopatz**, **Gil Forsyth**, **Jamie Bliss**, **David Strobach**, **Morten Enemark Lund** and **@xore** for amazing [xonsh](https://github.com/xonsh/xonsh) shell
