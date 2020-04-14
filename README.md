<p align="center">You stuffed command shell with aliases, tools and colors but you lose it all when using ssh. The mission of xxh is to bring your favorite shell wherever you go through the ssh without root access and system installations.</p>
<p align="center">  
  <a href="https://pypi.org/project/xxh-xxh/" target="_blank"><img src="https://img.shields.io/pypi/v/xxh-xxh.svg" alt="[release]"></a>
  <a href="https://gitter.im/xxh-xxh/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge" target="_blank"><img alt="[gitter chat]" src="https://badges.gitter.im/xxh-xxh/community.svg"></a>
  <img alt="[BSD license]" src="https://img.shields.io/pypi/l/xxh-xxh">
</p>
<p align="center">  
If you like the idea of xxh click ⭐ on the repo or ☕️ <a href="https://www.buymeacoffee.com/xxh">buy me a coffee</a>.
</p>

## Demo
<a href='https://github.com/xxh/xxh#installation-methods'><img alt='[xxh demo]' src='https://raw.githubusercontent.com/xxh/static/master/xxh-demo.gif'></a>

## Installation methods
#### [PyPi 3](https://pypi.org/project/xxh-xxh/) 
```shell script
pip3 install xxh-xxh
```

#### [Homebrew](https://brew.sh/)
```shell script
brew install python3 && pip3 install xxh-xxh
```

#### Linux portable binary
```shell script
mkdir ~/xxh && cd ~/xxh
wget https://github.com/xxh/xxh-portable/raw/master/result/xxh-portable-musl-alpine-Linux-x86_64.tar.gz
tar -xzf xxh-portable-musl-alpine-Linux-x86_64.tar.gz
./xxh
```

#### [AppImage](https://appimage.org/)
```shell script
mkdir ~/xxh && cd ~/xxh
wget -O xxh https://github.com/xxh/xxh-appimage/releases/download/continuous/xxh-release-x86_64.AppImage
chmod +x xxh && ./xxh
```

## Shells

Currently supported OS is Linux on x86_64.

| xxh-shell                                                             | status     | [seamless](https://github.com/xxh/xxh#what-is-seamless-mode)    | [plugins](https://github.com/xxh/xxh#what-is-xxh-plugin) | demo |
|-----------------------------------------------------------------------|------------|-------------|---------|------|
| **[xonsh-appimage](https://github.com/xxh/xxh-shell-xonsh-appimage)** | stable     | `xxh.xsh`   | [pipeliner](https://github.com/xxh/xxh-plugin-xonsh-pipe-liner), [bar](https://github.com/xxh/xxh-plugin-xonsh-theme-bar), [autojump](https://github.com/xxh/xxh-plugin-xonsh-autojump), [[+]](https://github.com/xxh/xxh-plugin-xonsh-example) | <a href="https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7" target="_blank"><img alt="[demo xonsh]" src="https://img.shields.io/badge/demo-xonsh-grass"></a> | 
| **[zsh](https://github.com/xxh/xxh-shell-zsh)**                       | stable     | `xxh.zsh`   | [ohmyzsh](https://github.com/xxh/xxh-plugin-zsh-ohmyzsh), [p10k](https://github.com/xxh/xxh-plugin-zsh-powerlevel10k), [[+]](https://github.com/xxh/xxh-plugin-zsh-example) | <a href="https://asciinema.org/a/rCiT9hXQ5IdwqOwg6rifyFZzb" target="_blank"><img alt="[demo zsh]" src="https://img.shields.io/badge/demo-zsh-grass"></a> |
| **[fish](https://github.com/xxh/xxh-shell-fish)**                     | stable     |  [todo](https://github.com/xxh/xxh/issues/74)           | [ohmyfish](https://github.com/xxh/xxh-plugin-fish-ohmyfish), [fisher](https://github.com/xxh/xxh-plugin-fish-fisher), [userconfig](https://github.com/xxh/xxh-plugin-fish-userconfig), [[+]](https://github.com/xxh/xxh-plugin-fish-example) | |
| **[bash-zero](https://github.com/xxh/xxh-shell-bash-zero)**           | prestable  | `xxh.bash`  | [ohmybash](https://github.com/xxh/xxh-plugin-bash-ohmybash), [[+]](https://github.com/xxh/xxh-plugin-bash-example) | <a href="https://asciinema.org/a/314508" target="_blank"><img alt="[demo bash]" src="https://img.shields.io/badge/demo-bash-grass"></a> |
| **[osquery](https://github.com/xxh/xxh-shell-osquery)**               | beta       |             | | |
| **[fish-appimage](https://github.com/xxh/xxh-shell-fish-appimage)**   | alpha      |             | | |

[Search xxh shell on Github](https://github.com/search?q=xxh-shell&type=Repositories) or [Bitbucket](https://bitbucket.org/repo/all?name=xxh-shell) or [create your shell entrypoint](https://github.com/xxh/xxh-shell-example) to use another portable shell.  

### [Prerun plugins](https://github.com/xxh/xxh/wiki#what-is-xxh-prerun-plugin)
Prerun plugins allow to bring any portable tools, dotfiles, aliases to xxh session before running shell. 

Pinned plugins: [mc](https://github.com/xxh/xxh-plugin-prerun-mc), [docker](https://github.com/xxh/xxh-plugin-prerun-docker), [python](https://github.com/xxh/xxh-plugin-prerun-python), [vim](https://github.com/xxh/xxh-plugin-prerun-vim), [xxh](https://github.com/xxh/xxh-plugin-prerun-xxh). 

## Usage
Use `xxh` as replace `ssh` to connecting to the host without changing ssh arguments:
```
xxh <host from ~/.ssh/config>
xxh [ssh arguments] [user@]host[:port] [xxh arguments]
```

Common examples (use `xxh --help` to get info about arguments):
```yaml
xxh myhost                                       # connect to the host
xxh -i id_rsa -p 2222 myhost                     # using ssh arguments: port and key
xxh myhost +s zsh                                # set the shell
xxh myhost +s xonsh-appimage +hhh "~"            # set /home/user as home directory (read Q&A)
xxh myhost +s bash-zero +I xxh-plugin-bash-vim   # preinstall the plugin
xxh myhost +if +q                                # install without questions in quiet mode
xxh myhost +hh /tmp/xxh +hhr                     # upload xxh to /tmp/xxh and remove when disconnect 
source xxh.zsh myhost +I xxh-plugin-zsh-ohmyzsh  # connect in seamless mode with ohmyzsh plugin
```
To reusing arguments and simplifying xxh usage to `xxh myhost` there is [config file](https://github.com/xxh/xxh/wiki#what-is-config-file).

### Install xxh packages
```
xxh [+I xxh-package +I ...] [+L] [+RI xxh-package +RI ...] [+R xxh-package +R ...]
```
Different ways to set the xxh package source:
```
xxh +I xxh-shell-example                                         # install from https://github.com/xxh
xxh +I https://github.com/xxh/xxh-shell-example                  # short url for github only, for other sources use examples below or add support
xxh +I https://github.com/xxh/xxh-shell-example/tree/mybranch    # short url for github only, for other sources use examples below or add support
xxh +I xxh-shell-example+git+https://github.com/xxh/xxh-shell-example                 # long url for any git repo
xxh +I xxh-shell-example+git+https://github.com/xxh/xxh-shell-example/tree/mybranch   # github only branch support
xxh +I xxh-shell-example+path+/home/user/my-xxh-dev/xxh-shell-example                 # install from local path
```

## The ideas behind xxh
**Portable**. Preparing portable shells and plugins occurs locally and then xxh uploads the result to host. 
No installations or root access on the host required. The security and careful about environment on the host are behind it. 

**Careful**. No blindfold copying config files from local to remote host. Following the privacy and repeatability 
reasons the better way is to fork the xxh plugin or shell example and pack your config to it.

**Hermetic**. If you delete `~/.xxh` directory from the remote host then xxh has never been on the host. By default your
home is `.xxh` directory and you can [choose the hermetic level of your xxh session](https://github.com/xxh/xxh/wiki#how-to-set-homeuser-as-home-instead-of-homeuserxxh).

**Be open and fork-ready**. Every repo could be forked, customized and reused without waiting for package management system, 
xxh releases or any third party. Currently supported five shells and the count could be grow by community.

**Do more**. The xxh packages are not only about shells. Any type of tool or code could be behind entrypoint. 
If you want to play Super Mario on the remote host just put it as entrypoint.

## Examples of use cases
### Python everywhere with xonsh
When you run `xxh myhost +s xonsh-appimage` you'll get portable python, pip and python-powered shell on the host without
any system installations on the host. Add plugins: [autojump](https://github.com/xxh/xxh-plugin-xonsh-autojump) 
saves time, [pipeliner](https://github.com/xxh/xxh-plugin-xonsh-pipe-liner) manipulates lines 
and [bar](https://github.com/xxh/xxh-plugin-xonsh-theme-bar) looks nice. 

### Put the cozy configs to xxh session

For example there is [xxh-plugin-prerun-mc](https://github.com/xxh/xxh-plugin-prerun-mc) which creates
[Midnight Commander](https://en.wikipedia.org/wiki/Midnight_Commander) (mc) config when you go to the host using xxh. 
You can fork it and create your cozy settings for mc once and forever.

### Oh My Zsh seamless SSH ([demo](https://asciinema.org/a/rCiT9hXQ5IdwqOwg6rifyFZzb))
```shell script
source xxh.zsh myhost +I xxh-plugin-zsh-ohmyzsh +if +q 
```
This command brings your current Oh My Zsh session theme to the xxh session. If you need more complex settings just fork 
the [xxh-plugin-zsh-ohmyzsh](https://github.com/xxh/xxh-plugin-zsh-ohmyzsh) and hack it.

### Read host as a table with [osquery](https://github.com/xxh/xxh-shell-osquery)
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
that you could help you on the host. [Bash-zero](https://github.com/xxh/xxh-shell-bash-zero) xxh-shell is one of this 
platforms that could be forked and stuffed.

## [Questions and answers](https://github.com/xxh/xxh/wiki)

- [Start](https://github.com/xxh/xxh/wiki#start)
  * [How it works?](https://github.com/xxh/xxh/wiki#how-it-works)
    + [Simple answer](https://github.com/xxh/xxh/wiki#simple-answer)
    + [Detailed workflow with code](https://github.com/xxh/xxh/wiki#detailed-workflow-with-code)
  * [How to set `/home/user` as home instead of `/home/user/.xxh`?](https://github.com/xxh/xxh/wiki#how-to-set-homeuser-as-home-instead-of-homeuserxxh)
  * [What about speed?](https://github.com/xxh/xxh/wiki#what-about-speed)
  * [What is seamless mode?](https://github.com/xxh/xxh/wiki#what-is-seamless-mode)
  * [What is config file?](https://github.com/xxh/xxh/wiki#what-is-config-file)
- [Packages for xxh](https://github.com/xxh/xxh/wiki#packages-for-xxh)
  * [How I can install xxh packages (shells or plugins)?](https://github.com/xxh/xxh/wiki#how-i-can-install-xxh-packages-shells-or-plugins)
  * [What is xxh plugin?](https://github.com/xxh/xxh/wiki#what-is-xxh-plugin)
  * [What is xxh prerun plugin?](https://github.com/xxh/xxh/wiki#what-is-xxh-prerun-plugin)
  * [How to change `pluginrc` run order to run some plugin before others?](https://github.com/xxh/xxh/wiki#how-to-change-pluginrc-run-order-to-run-some-plugin-before-others)
- [Advanced questions](https://github.com/xxh/xxh/wiki#advanced-questions)
  * [What if my `host_internal` can be reached only from my `host_external`?](https://github.com/xxh/xxh/wiki#what-if-my-host_internal-can-be-reached-only-from-my-host_external)
  * [How to add environment variables list?](https://github.com/xxh/xxh/wiki#how-to-add-environment-variables-list)
- [Development and contribution](https://github.com/xxh/xxh/wiki#development-and-contribution)
  * [What is the easiest way to debug shell and plugins?](https://github.com/xxh/xxh/wiki#what-is-the-easiest-way-to-debug-shell-and-plugins)
- [I have a new question!](https://github.com/xxh/xxh/wiki#i-have-a-new-question)

## Development
In the [xxh-dev](https://github.com/xxh/xxh-dev) repo there is full [docker](https://www.docker.com/)ised environment 
for development, testing and contribution. The process of testing and development is orchestrated by `xde` tool and as 
easy as possible.

**We have teams.** If you're in team it does not oblige to do something. The main goal of teams is to create group 
of passionate people who could help or support in complex questions. Some people could be expert in one shell and 
newbie in another shell and mutual assistance is the key to xxh evolution. [Ask join.](https://github.com/xxh/xxh/issues/50)

## Thanks
* **niess** for great [linuxdeploy-plugin-python](https://github.com/niess/linuxdeploy-plugin-python/) 
* **probonopd** and **TheAssassin** for hard-working [AppImage](https://github.com/AppImage)
* **Roman Perepelitsa** for incredible [statically-linked, hermetic, relocatable Zsh](https://github.com/romkatv/zsh-bin) 
* **Anthony Scopatz**, **Gil Forsyth**, **Jamie Bliss**, **David Strobach**, **Morten Enemark Lund** and **@xore** for amazing [xonsh](https://github.com/xonsh/xonsh) shell
* **Johannes Altmanninger** and **Fabian Homborg** for extensive and portable [fish shell](https://github.com/fish-shell/fish-shell)
