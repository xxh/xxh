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
for local_package_dir in [local_shell_dir]+sorted(local_plugins_dir.glob(f'*-xonsh-*')):
    plugin_name = local_package_dir.name
    local_package_env = local_package_dir / 'env'
    if local_package_env.exists():
        plugin_env_name = plugin_name.upper().replace('-', '_')
        with open(local_package_env) as f:
            plugin_envs = f.read().split('\n')
        for e in plugin_envs:
            if e in ${...}:
                xonsh_exec = '__xonsh__.env["%s"]=%s' % (e, repr(${e}))
                bash_env = plugin_env_name + '_EXE_' + e
                bash_exec = f'export {bash_env}={b64e(xonsh_exec)}'

                if '+v' in $ARGS or '+vv' in $ARGS:
                    print(f'Plugin {local_package_dir.name} xonsh exec: {xonsh_exec}', file=sys.stderr)
                    print(f'Plugin {local_package_dir.name} bash exec: {bash_exec}', file=sys.stderr)

                env_args += ['+heb', b64e(bash_exec)]

cdir = pf'{__file__}'.absolute().parent
xxh = cdir/'xxh'
if not xxh.exists():
    xxh='xxh'

@(xxh) @($ARGS) +s xonsh @(env_args)

