<p align="center">You stuffed command shell with aliases, tools and colors but you lose it all when using ssh. The mission of xxh is to bring your favorite shell wherever you go through ssh without root access and system installations.</p>

<p align="center">  
If you like the idea of xxh click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Bring%20your%20favorite%20shell%20wherever%20you%20go%20through%20the%20ssh.&url=https://github.com/xxh/xxh" target="_blank">tweet</a>.
</p>

<a href='https://github.com/xxh/xxh#installation-methods'><img alt='[xxh demo]' src='https://raw.githubusercontent.com/xxh/static/master/xxh-demo2.gif'></a>

<table border="0" width="100%">
<col style="width:33%">
<col style="width:33%">
<col style="width:33%">
<tbody>
<tr style="border: 0px !important;">
<td valign="top" style="border: 0px !important;"><b>Portable</b>. Preparing portable shells and plugins occurs locally and then xxh uploads the result to the host. No installations or root access on the host required. Security and host environment a prime focus.</td>
<td valign="top" style="border: 0px !important;"><b>Hermetic</b>. Deleting <code>~/.xxh</code> directory from the remote host will make the remote environment function as if xxh was never there. By default your home is the <code>.xxh</code> directory and you can <a href="https://github.com/xxh/xxh/wiki#how-to-set-homeuser-as-home-on-host">choose the hermetic level of your xxh session</a>.</td>
<td valign="top" style="border: 0px !important;"><b>Careful</b>. No blindfold copying config files from local to remote host. Following privacy and repeatability practices the best way is to fork the xxh plugin or shell example and pack your configs into it. </td>
</tr>
<tr style="border: 0px !important;">
<td valign="top" style="border: 0px !important;"><b>Be open and fork-ready</b>. Every xxh repo could be forked, customized and reused without waiting for a package management system, xxh release or any third party packages. Five shells are currently supported and more could be added by the community.</td>
<td valign="top" style="border: 0px !important;"><b>Do more</b>. The xxh packages are not only about shells. Any type of tool or code could be behind an entrypoint. If you want to run <a href="https://github.com/browsh-org/browsh">browsh</a> on the remote host, just put its portable version as an entrypoint in the xxh-shell.</td>
<td valign="top" style="border: 0px !important;"><b>Chameleon</b>. Switching the shells is as easy as possible and you don't have to be locked in to one shell. Choose your current shell based on the task you want to solve: <code>xxh anyhost +s xonsh</code> for a python environment, osquery for simple querying, fish for modern features or time-tested zsh and bash for speed. </td>   
</tr>
</tbody>
</table>
 
## Installation methods
#### [PyPi 3](https://pypi.org/project/xxh-xxh/) 
```shell script
pip3 install xxh-xxh
```

#### [pipx](https://pipxproject.github.io/pipx/) - good alternative to brew and pip, read [comparison](https://pipxproject.github.io/pipx/comparisons/)
```shell script
pipx install xxh-xxh
```

#### [Conda-forge](https://conda-forge.org/) [feedstock](https://github.com/conda-forge/xxh-xxh-feedstock)
```shell script
conda config --add channels conda-forge
conda install xxh-xxh
```

#### [Homebrew](https://brew.sh/)
```shell script
brew install xxh
```

#### [Macports](https://www.macports.org/)
```shell script
sudo port install xxh
```

#### Linux portable binary
```shell script
mkdir ~/xxh && cd ~/xxh
wget https://github.com/xxh/xxh/releases/download/0.8.7/xxh-portable-musl-alpine-Linux-x86_64.tar.gz
tar -xzf xxh-portable-musl-alpine-Linux-x86_64.tar.gz
./xxh
```

#### Linux [AppImage](https://appimage.org/)
```shell script
mkdir ~/xxh && cd ~/xxh
wget -O xxh https://github.com/xxh/xxh/releases/download/0.8.7/xxh-x86_64.AppImage
chmod +x xxh && ./xxh
```
To run AppImage on Alpine Linux [install](https://github.com/sgerrand/alpine-pkg-glibc/issues/153#issuecomment-795334536) [alpine-pkg-glibc](https://github.com/sgerrand/alpine-pkg-glibc) with [localedef](https://github.com/sgerrand/alpine-pkg-glibc#locales).

## Shells

Currently supported OS for target host is Linux on x86_64.

| xxh-shell                                                             | status     | [xxh-plugins](https://github.com/xxh/xxh/wiki#plugins) | [seamless](https://github.com/xxh/xxh/wiki#seamless-mode) | demo |
|-----------------------------------------------------------------------|------------|-------------|---------|------|
| **[xonsh](https://github.com/xxh/xxh-shell-xonsh)**                   | stable     | [autojump](https://github.com/xxh/xxh-plugin-xonsh-autojump), [[+]](https://github.com/xxh/xxh-plugin-xonsh-example) | `xxh.xsh` | <a href="https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7" target="_blank">demo</a> | 
| **[zsh](https://github.com/xxh/xxh-shell-zsh)**                       | stable     | [ohmyzsh](https://github.com/xxh/xxh-plugin-zsh-ohmyzsh), [p10k](https://github.com/xxh/xxh-plugin-zsh-powerlevel10k), [[+]](https://github.com/xxh/xxh-plugin-zsh-example)  | `xxh.zsh`   |  <a href="https://asciinema.org/a/rCiT9hXQ5IdwqOwg6rifyFZzb" target="_blank">demo</a> |
| **[fish](https://github.com/xxh/xxh-shell-fish)**                     | stable     | [ohmyfish](https://github.com/xxh/xxh-plugin-fish-ohmyfish), [fisher](https://github.com/xxh/xxh-plugin-fish-fisher), [userconfig](https://github.com/xxh/xxh-plugin-fish-userconfig), [[+]](https://github.com/xxh/xxh-plugin-fish-example) | [todo](https://github.com/xxh/xxh/issues/74) |
| **[bash](https://github.com/xxh/xxh-shell-bash)**                     | stable     | [ohmybash](https://github.com/xxh/xxh-plugin-bash-ohmybash), [[+]](https://github.com/xxh/xxh-plugin-bash-example) | `xxh.bash`  | <a href="https://asciinema.org/a/314508" target="_blank">demo</a> |
| **[osquery](https://github.com/xxh/xxh-shell-osquery)**               | beta       |             | | |
| **[fish-appimage](https://github.com/xxh/xxh-shell-fish-appimage)**   | alpha      |             | | |
| **[elvish](https://github.com/krageon/xxh-shell-elvish)**   | alpha      |             | | |

[Search xxh shell on Github](https://github.com/search?q=xxh-shell&type=Repositories) or [Bitbucket](https://bitbucket.org/repo/all?name=xxh-shell) or [create your shell entrypoint](https://github.com/xxh/xxh-shell-example) to use another portable shell.  

### Prerun plugins
[Prerun plugins](https://github.com/xxh/xxh/wiki#plugins) allow you to bring any portable tools, dotfiles or aliases to xxh session before running shell. 

Pinned plugins: **[core](https://github.com/xxh/xxh-plugin-prerun-core)** (xxh-sudo, xxh-screen, xxh-tmux), **[dotfiles](https://github.com/xxh/xxh-plugin-prerun-dotfiles)**, **[docker](https://github.com/xxh/xxh-plugin-prerun-docker)**, **[python](https://github.com/xxh/xxh-plugin-prerun-python)**, **[xxh](https://github.com/xxh/xxh-plugin-prerun-xxh)**, **[vim](https://github.com/xxh/xxh-plugin-prerun-vim)**, **[zoxide](https://github.com/xxh/xxh-plugin-prerun-zoxide)**, **[starship](https://github.com/izissise/xxh-plugin-prerun-starship)**. There is [cookiecutter template to create prerun plugin](https://github.com/xxh/cookiecutter-xxh-plugin-prerun).

## Usage
Use `xxh` instead of `ssh` when connecting to Linux hosts without changing ssh arguments:
```
xxh <host from ~/.ssh/config>
xxh [ssh arguments] [user@]host[:port] [xxh arguments]
xxh local [xxh arguments]
```

Common examples (use `xxh --help` to get info about arguments):
```yaml
xxh anyhost                                       # Connect to the host
xxh -i id_rsa -p 2222 anyhost                     # Using ssh arguments: port and key
xxh user@host +c et                               # Using EternalTerminal (https://github.com/MisterTea/EternalTerminal)
xxh anyhost +s zsh +i                             # Set the shell and install it without yes/no question
xxh anyhost +s xonsh +hhh "~"                     # Set /home/user as home directory (read Q&A)
xxh anyhost +s bash +I xxh-plugin-bash-vim        # Preinstall a plugin
xxh anyhost +if +q                                # Force reinstall xxh on the host in quiet mode
xxh anyhost +hh /tmp/xxh +hhr                     # Upload xxh to /tmp/xxh and remove when disconnecting
source xxh.zsh anyhost +I xxh-plugin-zsh-ohmyzsh  # Connect in seamless mode with ohmyzsh plugin
xxh local +s xonsh                                # Experimental: build xxh environment inplace and without ssh
```
For reusing arguments and simplifying xxh usage (like shortening to `xxh anyhost`) there is a [config file](https://github.com/xxh/xxh/wiki#config-file).

**Why the plus sign for the xxh arguments?** The xxh is using the plus sign for the xxh arguments to save the ability to use the minus sign for the original ssh arguments. This allows just replace the first two letters in the `ssh` command to convert it to the `xxh` command. Also see the [discussion](https://github.com/xxh/xxh/issues/129).
 
### Installing xxh packages
```bash
xxh [+I xxh-package +I ...] [+L] [+RI xxh-package +RI ...] [+R xxh-package +R ...]
```
Different ways to set the xxh package source:
```yaml
xxh +I xxh-shell-example                                         # install from https://github.com/xxh
xxh +I https://github.com/xxh/xxh-shell-example                  # short url for github only, for other sources use examples below or add support
xxh +I https://github.com/xxh/xxh-shell-example/tree/mybranch    # short url for github only, for other sources use examples below or add support
xxh +I xxh-shell-example+git+https://github.com/xxh/xxh-shell-example                 # long url for any git repo
xxh +I xxh-shell-example+git+https://github.com/xxh/xxh-shell-example/tree/mybranch   # github only branch support
xxh +I xxh-shell-example+git+git@github.com:githubuser/xxh-shell-example.git          # install from private repository using ssh
xxh +I xxh-shell-example+path+/home/user/my-xxh-dev/xxh-shell-example                 # install from local path
```

### Using xxh inplace without ssh connection

This is experimental magic. Please read the text below twice.

If you have shell access on the host or you're in a docker container and you can't ssh to it 
then you can download and build hermetic xxh environment inplace. The `xxh local` command works 
exactly like `xxh remote_host` and creates a hermetic environment in `~/.xxh` by default.

At this time we don't have portable build tools like `git`, `wget`, `curl`, `tar` and others which 
could be required by some xxh package build scripts. When running `xxh local` it is expected that the tools are present on the host.

To run xxh inplace on Linux x86_64 just copy and paste these bash commands:
```bash
XH=~/.xxh \
 && XD=https://github.com/xxh/xxh-portable/raw/master/result/xxh-portable-musl-alpine-Linux-x86_64.tar.gz \
 && mkdir -p $XH && cd $XH \
 && ( [[ -x $(command -v curl) ]] && curl -L $XD || wget -O- $XD ) | tar zxf - xxh \
 && echo 'Usage: ./xxh local [+s xonsh/zsh/fish/osquery/bash]'
```
Next time you're on host just run `~/.xxh/xxh local` and you will enter your xxh environment. 

## Examples of use cases
### Python with pip everywhere without installation
#### Way 1. Using xonsh
```
xxh anyhost +s xonsh

anyhost> python --version
Python 3.8.2
```
You'll get python-powered [xonsh](https://xon.sh) shell with portable python and pip on the host without any system installations on the host. 
You can install PyPi packages manually or bring them with you automatically by using [xxh-plugin-prerun-dotfiles](https://github.com/xxh/xxh-plugin-prerun-dotfiles). Also don't forget about xxh-plugins like [zoxide](https://github.com/xxh/xxh-plugin-prerun-zoxide).

#### Way 2. Using portable python on any xxh shell
```
xxh +RI xxh-plugin-prerun-python
xxh anyhost +s zsh

anyhost> python --version
Python 3.8.2
anyhost> pip install pandas
```
Using [xxh-plugin-prerun-python](https://github.com/xxh/xxh-plugin-prerun-python) you'll get a portable 
Python AppImage which can be used on a host without python and with any xxh shell.

### Using docker on host without root access

Try [xxh-plugin-prerun-docker](https://github.com/xxh/xxh-plugin-prerun-docker):
```
xxh +RI xxh-plugin-prerun-docker
xxh anyhost +if

anyhost> xxh-docker-run
anyhost> docker ps                                                                                                                                                                                                                            
CONTAINER ID        IMAGE               COMMAND
anyhost> docker run --rm hello-world | grep Hello
Hello from Docker!
anyhost> xxh-docker-stop
```

### Bring dotfiles to xxh session

There is the [xxh-plugin-prerun-dotfiles](https://github.com/xxh/xxh-plugin-prerun-dotfiles) plugin which creates config files 
when you go to the host using xxh. You can fork it and create your cozy settings once and forever.

### Seamless Oh My Zsh ([demo](https://asciinema.org/a/rCiT9hXQ5IdwqOwg6rifyFZzb))
```shell script
source xxh.zsh anyhost +I xxh-plugin-zsh-ohmyzsh +if +q 
```
This command brings your current Oh My Zsh session theme to the xxh session. If you need more complex settings just fork 
the [xxh-plugin-zsh-ohmyzsh](https://github.com/xxh/xxh-plugin-zsh-ohmyzsh) and hack it.

### Read host as a table with [osquery](https://github.com/xxh/xxh-shell-osquery)
```
$ xxh anyhost +s osquery
osquery> SELECT * FROM users WHERE username='news';
+-----+-----+----------+-------------+-----------------+-------------------+
| uid | gid | username | description | directory       | shell             |
+-----+-----+----------+-------------+-----------------+-------------------+
| 9   | 9   | news     | news        | /var/spool/news | /usr/sbin/nologin |
+-----+-----+----------+-------------+-----------------+-------------------+
```   

### All in one portable home
xxh is very agile. You can create your own `xxh-shell` (the shell part means it has an entrypoint) which can have any portable tools
that could help you on the host. [Bash](https://github.com/xxh/xxh-shell-bash) xxh-shell is one of these 
platforms that could be forked and stuffed.

## [Questions and answers](https://github.com/xxh/xxh/wiki)

- [Welcome to xxh family](https://github.com/xxh/xxh/wiki#welcome-to-xxh-family)
  * [How it works](https://github.com/xxh/xxh/wiki#how-it-works)
    + [Simple answer](https://github.com/xxh/xxh/wiki#simple-answer)
    + [Detailed workflow with code](https://github.com/xxh/xxh/wiki#detailed-workflow-with-code)
  * [Plugins](https://github.com/xxh/xxh/wiki#plugins)
  * [Connection speed](https://github.com/xxh/xxh/wiki#connection-speed)
  * [Seamless mode](https://github.com/xxh/xxh/wiki#seamless-mode)
  * [Config file](https://github.com/xxh/xxh/wiki#config-file)
- [Packages for xxh](https://github.com/xxh/xxh/wiki#packages-for-xxh)
  * [Install shells and plugins](https://github.com/xxh/xxh/wiki#install-shells-and-plugins)
- [Advanced](https://github.com/xxh/xxh/wiki#advanced)
  * [How to set /home/user as home on host](https://github.com/xxh/xxh/wiki#how-to-set-homeuser-as-home-on-host)
  * [Using sudo](https://github.com/xxh/xxh/wiki#using-sudo)
  * [Using xxh in xxh session](https://github.com/xxh/xxh/wiki#using-xxh-in-xxh-session)
  * [Target host is behind another host](https://github.com/xxh/xxh/wiki#target-host-is-behind-another-host)
  * [Environment variables](https://github.com/xxh/xxh/wiki#environment-variables)
- [Development and contribution](https://github.com/xxh/xxh/wiki#development-and-contribution)
  * [The easiest way to debug shell and plugins](https://github.com/xxh/xxh/wiki#the-easiest-way-to-debug-shell-and-plugins)
  * [Prerun plugins](https://github.com/xxh/xxh/wiki#prerun-plugins)
  * [Change plugin run order](https://github.com/xxh/xxh/wiki#change-plugin-run-order)
- [New questions](https://github.com/xxh/xxh/wiki#new-questions)

## Development

### xxh Development Environment

In the [xxh development environment](https://github.com/xxh/xxh/tree/master/xde) there is full [dockerised](https://www.docker.com/) environment
for development, testing and contribution. The process of testing and development is orchestrated by `xde` tool and is as 
easy as possible.

### Vagrant based Plugin Development

To develop plugins, [Vagrant](https://www.vagrantup.com) supports starting [many configurations](https://app.vagrantup.com/boxes/search) of virtual machines using Virtualbox.

See [the Plugin Development folder](./plugin-development) for more details

### We have teams

If you're in a team it does not mean you have an obligation to do something. The main goal of teams is to create groups
of passionate people who could help or support solving complex problems. Some people could be an expert in one shell and a
newbie in another shell and mutual assistance is the key to xxh evolution. [Ask join.](https://github.com/xxh/xxh/issues/50)

## Thanks
* **niess** for great [python-appimage](https://github.com/niess/python-appimage)
* **probonopd** and **TheAssassin** for hard-working [AppImage](https://github.com/AppImage)
* **Anthony Scopatz**, **Gil Forsyth**, **Jamie Bliss**, **David Strobach**, **Morten Enemark Lund** and **@xore** for amazing [xonsh shell](https://github.com/xonsh/xonsh)
* **Roman Perepelitsa** for incredible [statically-linked, hermetic, relocatable Zsh](https://github.com/romkatv/zsh-bin)
* **Johannes Altmanninger** and **Fabian Homborg** for extensive and portable [fish shell](https://github.com/fish-shell/fish-shell)
