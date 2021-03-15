#!/usr/bin/env xonsh

import sys, os, argparse, re, subprocess

verbose = False
vverbose = False
not_interactive = False

def SC(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    [out, err] = proc.communicate()
    return (out, err, proc)

def cmd_str(c):
    return c

def check(name, cmd, expected_result):
    try_count = 3
    while try_count > 0:
        try_count -= 1
        print('TEST: '+name, end='...')
        cmd = cmd.strip()

        if vverbose:
            print(f'\nRUN: {cmd}', end=' ...')

        if 'xxh local' in cmd:
            o, e, p = SC(cmd)
            cmd_result = o.decode().strip()
        else:
            cmd_result = $(bash -c @(cmd)).strip()
        cmd_result = re.sub('\x1b]0;.*\x07','', cmd_result)
        cmd_result = re.sub(r'\x1b\[\d+m','', cmd_result)
        cmd_result = re.sub(r'\x1b\[\d+;\d+;\d+m','', cmd_result)

        # https://github.com/xonsh/xonsh/issues/3555 and https://github.com/xonsh/xonsh/issues/3557
        cmd_result = re.sub(r'bash: cannot set terminal process group \(.*?\): Inappropriate ioctl for device\nbash: no job control in this shell\n', '', cmd_result)

        expected_result = expected_result.strip()
        if cmd_result != expected_result or vverbose:
            print('\n',end='')
            if verbose:
                print(f'CMD: {cmd}')
            print(f"OUTPUT {repr(cmd_result)}\nEXPECT {repr(expected_result)} ")

            if cmd_result != expected_result:
                if try_count > 0 or 'Bad file descriptor' in cmd_result:
                    print('RETRY')
                    continue
                else:
                    print('ERROR!')
                    cmdv = cmd + ' +v  # or with +vv'
                    if not not_interactive:
                        yn = input(f'Run verbose? [Y/n]: %s' % cmdv)
                        if yn.lower().strip() in ['y','']:
                            bash -c @(cmdv)
                            
                    if try_count > 0:
                        continue
                    else:
                        print('To debug run `./xde g start` and then: %s' % cmdv)
                        sys.exit(1)

        print('OK')
        break

if __name__ == '__main__':

    argp = argparse.ArgumentParser(description=f"xde test")
    argp.add_argument('-r', '--remove', default=False, action='store_true', help="Remove xxh home before tests.")
    argp.add_argument('-ni', '--not-interactive', default=False, action='store_true', help="Not interactive mode.")
    argp.add_argument('-v', '--verbose', default=False, action='store_true', help="Verbose mode.")
    argp.add_argument('-vv', '--vverbose', default=False, action='store_true', help="Super verbose mode.")
    argp.add_argument('-s', '--shell', help="Shells to test")
    argp.add_argument('-H', '--hosts', default=[], help="Comma separated hosts list")
    argp.add_argument('-sr', '--skip-repos-update', default=False, action='store_true', help="Skip repos update before test running.")
    argp.usage = argp.format_usage().replace('usage: tests.xsh', 'xde test')
    opt = argp.parse_args()
    verbose = opt.verbose
    not_interactive = opt.not_interactive
    if opt.vverbose:
        verbose = vverbose = True

    git_verbose_arg = [] if verbose else ['-q']

    if opt.hosts:
        opt.hosts = opt.hosts.split(',')

    xxh = '/xxh/xxh/xxh'
    local_xxh_home = '/root/local_xxh_home'
    xxh_args = ['++local-xxh-home', local_xxh_home]

    hosts = {}
    hosts['local'] = {
        'xxh_auth': [],
        'home': '/root'
    }
    hosts['ubuntu_k'] = {
        'user':'root',
        'home':'/root',
        'ssh_auth': ['-i', '/xxh/xde/keys/id_rsa'],
        'xxh_auth': ['-i', '/xxh/xde/keys/id_rsa'],
        'sshpass': []
    }
    hosts['ubuntu_kf'] = hosts['ubuntu_k']
    hosts['centos_k'] = hosts['ubuntu_k']
    hosts['arch_p'] = {
        'user':'docker',
        'home':'/home/docker',
        'ssh_auth':[],
        'xxh_auth':['+P','docker'],
        'sshpass': ['sshpass', '-p', 'docker']
    }

    rm -rf /root/.ssh/known_hosts

    if opt.remove:
        print(f'Remove start:{local_xxh_home}')
        rm -rf @(local_xxh_home)

    if not pf'{local_xxh_home}/.xxh/shells'.exists():
        print("Don't forget `pip uninstall xxh-xxh` before tests")
        print('First time of executing tests takes time because of downloading files. Take a gulp of water or a few :)')

    mkdir -p @(local_xxh_home)/.xxh/plugins @(local_xxh_home)/.xxh/shells

    print('Prepare repos (to avoid full update use --skip-repos-update)')

    xxh_shell_repos = {}
    xxh_shell_repos['xxh-shell-xonsh'] = {
        'shells': ['xxh-shell-xonsh', 'xxh-shell-zsh'],
        'plugins': ['xxh-plugin-xonsh-pipe-liner', 'xxh-plugin-xonsh-theme-bar', 'xxh-plugin-xonsh-autojump']
    }
    xxh_shell_repos['xxh-shell-zsh'] = {
        'shells': ['xxh-shell-zsh'],
        'plugins': ['xxh-plugin-zsh-ohmyzsh']
    }
    xxh_shell_repos['xxh-shell-bash'] = {
        'shells': ['xxh-shell-bash'],
        'plugins': ['xxh-plugin-bash-ohmybash']
    }
    xxh_shell_repos['xxh-shell-fish'] = {
        'shells': ['xxh-shell-fish'],
        'plugins': []
    }

    if opt.shell:
        xxh_shell_repos = {opt.shell: xxh_shell_repos[opt.shell]}

    if not opt.skip_repos_update:
        print(f'Remove {local_xxh_home}/.xxh/shells {local_xxh_home}/.xxh/plugins')
        rm -rf @(local_xxh_home)/.xxh/shells @(local_xxh_home)/.xxh/plugins

    for xxh_shell, install_repos in xxh_shell_repos.items():
        for rtype, repos  in install_repos.items():
            for repo in repos:
                repo_dir = pf'{local_xxh_home}/.xxh/{rtype}/{repo}'
                repo_local_path = pf'/xxh/{repo}'

                if repo_dir.exists():
                    if repo_local_path.exists():
                        print(f'Repo {repo}: skip installing from ../{repo}')
                    else:
                        print(f'Repo {repo}: skip installing from source')
                else:
                    if repo_local_path.exists():
                        print(f'Repo {repo}: replaced from /xxh/{repo}. Do not forget to pull from master!')
                        repo = f'{repo}+path+{repo_local_path}'
                    @(xxh) +I @(repo) ++local-xxh-home @(local_xxh_home)

    ssh_opts = ["-o", "StrictHostKeyChecking=accept-new", "-o", "LogLevel=QUIET"]

    if 'xxh-shell-xonsh' in xxh_shell_repos:
        print('[Local test xonsh xxh plugins]')
        print(f'Remove /root/.xxh_test')
        rm -rf /root/.xxh_test
        check(
            'Local test xonsh xxh plugins',
            $(echo @(xxh) local +iff +hh /root/.xxh_test +lh /root/.xxh_test +I xxh-plugin-xonsh-theme-bar +I xxh-plugin-xonsh-pipe-liner +I xxh-plugin-xonsh-autojump +hf /xxh/xde/tests/xonsh/test_plugins.xsh ),
            "1234\n5678\n\n{bar}\n{WHITE}{prompt_end}{NO_COLOR}"
        )

    for shell in xxh_shell_repos.keys():
        for host, h in hosts.items():
            if opt.hosts and host not in opt.hosts:
                continue

            print(f'\n[{shell} + {host}]')

            if host == 'local':
                server = 'local'
                host_home = h['home']
            else:
                user = h['user']
                server = user + '@' + host
                host_home = h['home']

                check(
                    f'Remove {server}:~/.xxh',
                    $(echo @(h['sshpass']) ssh @(h['ssh_auth']) @(ssh_opts) @(server) "rm -rf ~/.xxh"),
                    ''
                )

                check(
                    'Test connect using ssh',
                    $(echo @(h['sshpass']) ssh @(h['ssh_auth']) @(ssh_opts) @(server) "echo Test!"),
                    'Test!'
                )

            if shell == 'xxh-shell-xonsh':
                check(
                    'Test install xxh',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +iff +s @(shell) +hf /xxh/xde/tests/xonsh/test_env.py ),
                    "{{'XXH_HOME': '{host_home}/.xxh/.xxh/shells/xxh-shell-xonsh/build/../../../..', 'PYTHONPATH': '{host_home}/.xxh/.xxh/shells/xxh-shell-xonsh/build/../../../../.local/lib/python3.8/site-packages'}}".format(host_home=host_home)
                )

                # check(
                #     'Test AppImage extraction on the host',
                #     $(echo @(h['sshpass']) ssh @(h['ssh_auth']) @(ssh_opts) @(server) @(xxh_args) @(f"[ -d {host_home}/.xxh/.xxh/shells/xxh-shell-xonsh/build/xonsh-squashfs ] && echo 'extracted' ||echo 'not_extracted'") ),
                #     'not_extracted' if 'f' in host.split('_')[-1] else 'extracted'
                # )

                check(
                    'Test python',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +hf /xxh/xde/tests/xonsh/test_python.xsh ),
                    "Python 3.8"
                )

                check(
                    'Test xonsh run xonsh script',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +hf /xxh/xde/tests/xonsh/test_xonsh_run_xonsh.xsh +e TESTENV="test env" ),
                    "123\n.xxh\ntest env"
                )

                check(
                    'Test pip upgrade',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +hf /xxh/xde/tests/xonsh/test_pip_upgrade.xsh ),
                    ""
                )
                check(
                    'Test pip package install',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +hf /xxh/xde/tests/xonsh/test_pip_package_install.xsh ),
                    ""
                )
                check(
                    'Test pip package import',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +hf /xxh/xde/tests/xonsh/test_pip_package_import.xsh ),
                    "[[1], [2], [3]]"
                )

                # Xontribs

                check(
                    'Test xontrib',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +iff +hf /xxh/xde/tests/xonsh/test_xontrib.xsh ),
                    "autojump  installed      loaded\nschedule  installed      loaded"
                )

                check(
                    'Test xxh plugins',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +iff +hf /xxh/xde/tests/xonsh/test_plugins.xsh ),
                    "1234\n5678\n\n{bar}\n{WHITE}{prompt_end}{NO_COLOR}"
                )

            elif shell == 'xxh-shell-zsh':
                shell_arg = ['+s', shell]
                check(
                    'Test zsh env',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +if +hf /xxh/xde/tests/zsh/test_env.zsh +e TESTENV="test env" @(shell_arg) ),
                    "test zsh .xxh and env=test env"
                )

                check(
                    'Test zsh command',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +if +hc @('"echo \'test \\"zsh\\" command\'"') @(xxh_args) ),
                    'test "zsh" command'
                )
            elif shell == 'xxh-shell-bash':
                shell_arg = ['+s', shell]
                check(
                    'Test bash env',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +if +hf /xxh/xde/tests/bash/test_env.sh +e TESTENV="test env" @(shell_arg) ),
                    "test bash xxh .xxh and env=test env"
                )

                check(
                    'Test bash command',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +if +hc @('"echo \'test \\"bash\\" command\'"') @(shell_arg) ),
                    'test "bash" command'
                )

                # $OSH_THEME="morris"
                # check(
                #     'Test bash seamless',
                #     $(echo source @(xxh)_xxh/xxh.bash @(h['xxh_auth']) @(server) @(xxh_args) +if +hf /xxh/xde/tests/bash/test_seamless.sh @(shell_arg) ),
                #     "morris"
                # )

            elif shell == 'xxh-shell-fish':
                shell_arg = ['+s', shell]
                check(
                    'Test fish command',
                    $(echo @(xxh) @(h['xxh_auth']) @(server) @(xxh_args) +if +hc @('"echo test"') @(shell_arg) ),
                    "test"
                )

    print('\nDONE')
