<p align="center">You chosen a favorite command shell and spent hours to adjust it, to stuffed it with aliases, shortcuts and colors. But when you move from local to remote host using ssh you lose it all. The mission of xxh is to allow you bring your favorite shell with your aliases, shortcuts and color theme wherever you go through the ssh.</p>
<p align="center">  
  <a href="https://pypi.org/project/xonssh-xxh/" target="_blank"><img src="https://img.shields.io/pypi/v/xonssh-xxh.svg" alt="[release]"></a>
  <a href="https://asciinema.org/a/osSEzqnmH9pMYEZibNe2K7ZL7" target="_blank"><img alt="[asciinema demo]" src="https://img.shields.io/badge/demo-asciinema-grass"></a>
  <a href="#plugins" target="_blank"><img alt="[plugins]" src="https://img.shields.io/badge/extensions-plugins-yellow"></a>
  <a href="https://gitter.im/xonssh-xxh/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge" target="_blank"><img alt="[gitter chat]" src="https://badges.gitter.im/xonssh-xxh/community.svg"></a>
  <img alt="[BSD license]" src="https://img.shields.io/pypi/l/xonssh-xxh">
</p>

## Install or update
```
python3 -m pip install --upgrade xonssh-xxh
```
After install you can just using `xxh` command as replace `ssh` to connecting to the host because `xxh` has seamless support of basic `ssh` command arguments. 

## Usage
```
$ ./xxh -h
usage: xxh <host from ~/.ssh/config>
usage: xxh [ssh arguments] [user@]host[:port] [xxh arguments]
usage: xxh [-h] [-V] [-p SSH_PORT] [-l SSH_LOGIN] [-i SSH_PRIVATE_KEY]
           [-o SSH_OPTION -o ...] [+P PASSWORD] [+PP]
           [user@]host[:port]
           [+i] [+if] [+iff] [+v] [+vv] [+s SHELL]
           [+hh HOST_XXH_HOME] [+hf HOST_EXECUTE_FILE] [+hc HOST_EXECUTE_COMMAND] 
           [+xc XXH_CONFIG] [+lh LOCAL_XXH_HOME]

Your favorite shell wherever you go through the ssh. 

     ____  __________     @    @    
  ______  /          \     \__/     
   ____  /    ______  \   /   \           contribution
 _____  /    / __   \  \ /   _/   https://github.com/xxh/xxh   
   ___ (    / /  /   \  \   /          
        \   \___/    /  /  /                plugins            
     ____\          /__/  /   https://github.com/search?q=xxh-plugin
    /     \________/     /                           
   /____________________/       
```

## Supported shells
**[Xonsh shell](https://github.com/xxh/xxh-shell-xonsh-appimage)** — used by default.

**[Zsh shell](https://github.com/xxh/xxh-shell-zsh)** — beta version with [oh-my-zsh](https://github.com/xxh/xxh-plugin-zsh-ohmyzsh) and [powerlevel10k](https://github.com/xxh/xxh-plugin-zsh-powerlevel10k) xxh-plugins. Help wanted for testing and improving entrypoint.

**[Fish shell](https://github.com/xxh/xxh-shell-fish-appimage)** — alpha version. Help wanted for testing and improving entrypoint.

**Bash shell** — this shell is almost everywhere. Probably the portable version is not needed. You can just create your entrypoint with your lovely functions.

🔎 [Search xxh shell on Github](https://github.com/search?q=xxh-shell&type=Repositories) or [Bitbucket](https://bitbucket.org/repo/all?name=xxh-shell).

 💡  [Create your shell entrypoint](https://github.com/xxh/xxh-shell-sample) to use another portable shell. 

## Plugins

**xxh plugin** is the set of scripts which will be run on the host when you go using xxh. It could be shell settings, environment variables, plugins, color themes and everything you need. You can find the links to plugins on [xxh-shells repos](https://github.com/search?q=xxh%2Fxxh-shell&type=Repositories). Feel free to fork it.

## Notes

### What about speed?

The first connection takes time for downloading and uploading portable shell. It depends on portable shell size and channel speed. But when xxh is installed on the host and you do just `xxh myhost` then it works as ordinary ssh connection speed.

### How it works?

When you run `xxh myhost` command xxh download portable shell and store locally to future use. Then if it needed xxh upload the portable shell, init scripts and plugins to the host. Finally xxh make ssh connection to the host and run portable shell without any system installs and affection on the target host.

## Development
🛠️ In the [xxh-dev](https://github.com/xxh/xxh-dev) repo there is full [docker](https://www.docker.com/)ised environment for development, testing and contribution. The process of testing and development is orchestrated by `xde` tool and as easy as possible.

## Spread the word
If you like the idea of xxh help spread the word about xxh! Click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Python-powered%20shell%20wherever%20you%20go%20through%20the%20ssh&url=https%3A%2F%2Fgithub.com%2Fxxh%2Fxxh&related=" target="_blank">tweet the link</a>! 

## Thanks
* @scopatz for https://github.com/xonsh/xonsh
* @gforsyth for https://github.com/xonsh/xonsh/issues/3374
* @probonopd for https://github.com/AppImage
* @niess for https://github.com/niess/linuxdeploy-plugin-python/ 
