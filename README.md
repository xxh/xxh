<p align="center">You chosen a favorite command shell and spend hours to adjust it, to stuff it with aliases, shortcuts and colors. But when you move from local to remote host using ssh you lose it all. <b>The mission of xxh</b> is to allow you to use your favorite shell with your aliases, shortcuts and color theme wherever you go through the ssh.</p>
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

usage: xxh [-h] [-V] [-p SSH_PORT] [-l SSH_LOGIN] [-i SSH_PRIVATE_KEY] [-o SSH_OPTION -o ...] 
           [user@]host[:port]
           [+i] [+if] [+P PASSWORD] [+PP] 
           [+lxh LOCAL_XXH_HOME] [+hxh HOST_XXH_HOME] [+he HOST_EXECUTE_FILE] 
           [+m METHOD] [+v] [+vv]

The xxh is for using the xonsh shell wherever you go through the ssh. 

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

Currently supported Python-powered [xonsh shell](https://xon.sh).

Experimental: to use another shell you can create your `xxh-shell` entrypoint like in [xxh-shell-xonsh-appimage](https://github.com/xxh/xxh-shell-xonsh-appimage) and add `+s` argument to your `xxh` command. 

## Plugins

**xxh plugin** is the set of xsh scripts which will be run when you'll use xxh. You can create xxh plugin with your lovely aliases, tools or color theme and xxh will bring them to your ssh sessions.

🔎 [Search xxh plugins on Github](https://github.com/search?q=xxh-plugin&type=Repositories) or [Bitbucket](https://bitbucket.org/repo/all?name=xxh-plugin) or 💡 [Create xxh plugin](https://github.com/xxh/xxh-plugin-xonsh-sample)

### xonsh xxh plugins

Pinned:
* [xxh-plugin-xonsh-pipe-liner](https://github.com/xxh/xxh-plugin-xonsh-pipe-liner) — processing the lines easy with python and classic shell pipes
* [xxh-plugin-xonsh-theme-bar](https://github.com/xxh/xxh-plugin-xonsh-theme-bar) — theme to stay focused
* [xxh-plugin-xonsh-autojump](https://github.com/xxh/xxh-plugin-xonsh-autojump) — save time on moving thru directories

## Notes

### Using python, pip and [xontribs](https://xon.sh/xontribs.html)

The xxh is using pip and python from `xonsh.AppImage` by default. You can update pip (`pip install --upgrade pip`) and install packages ordinally: `pip install --upgrade pandas`. The packages will appear in host xxh home `~/.xxh/pip` by default.

To install [xontribs](https://xon.sh/xontribs.html) in xxh session use `xpip install <package>`. Never use `pip` to install xontribs ([details](https://github.com/xonsh/xonsh/issues/3463)).

### How it works?

When you run `xxh myhost` command xxh download portable xonsh and store locally to future use. Then if it needed xxh upload the portable xonsh, init scripts and plugins to the host. Finally xxh make ssh connection to the host and run portable xonsh shell without any system installs and affection on the target host.

## Development
🛠️ In the [xxh-dev](https://github.com/xxh/xxh-dev) repo there is full [docker](https://www.docker.com/)ised environment for development, testing and contribution. The process of testing and development is orchestrated by `xde` tool and as easy as possible.

## Spread the word
If you like the idea of xxh help spread the word about xxh! Click ⭐ on the repo and <a href="https://twitter.com/intent/tweet?text=Python-powered%20shell%20wherever%20you%20go%20through%20the%20ssh&url=https%3A%2F%2Fgithub.com%2Fxxh%2Fxxh&related=" target="_blank">tweet the link</a>! 

## Thanks
* @scopatz for https://github.com/xonsh/xonsh
* @probonopd for https://github.com/AppImage
* @niess for https://github.com/niess/linuxdeploy-plugin-python/
* @gforsyth for https://github.com/xonsh/xonsh/issues/3374
