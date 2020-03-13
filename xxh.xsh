#!/usr/bin/env xonsh
#
# This entrypoint is to allow xxh getting current environment variables
# and pass some of them to xxh session to seamless transition to host.
#
# Usage in xonsh: source xxh.xsh [ordinary xxh arguments]
#

from base64 import b64encode

def b64e(s):
    return b64encode(str(s).encode()).decode()

local_xxh_home = p"~/.xxh"

env_args = []
local_shell_dir = local_xxh_home / 'xxh/shells/xxh-shell-xonsh-appimage'
local_plugins_dir = local_xxh_home / 'xxh/plugins'
for local_plugin_dir in sorted(local_plugins_dir.glob(f'*-xonsh-*'))+[local_shell_dir]:
    local_plugin_env = local_plugin_dir / 'env'
    if local_plugin_env.exists():
        with open(local_plugin_env) as f:
            plugin_envs = f.read().split('\n')
        for e in plugin_envs:
            if e in ${...}:
                if '+v' in $ARGS or '+vv' in $ARGS:
                    print(f'Plugin {local_plugin_dir.name} environment: {e}='+str(${e}), file=sys.stderr)
                env_args += ['+eb', "%s=%s" % ( e, b64e(${e}) ) ]

./xxh @($ARGS) +s xonsh @(env_args)

