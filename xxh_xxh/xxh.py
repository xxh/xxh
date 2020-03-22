import os, sys, argparse, yaml, datetime, re, getpass, pexpect
from shutil import which
from sys import exit
from argparse import RawTextHelpFormatter
from urllib.parse import urlparse
from random import randint
from base64 import b64encode

from .shell import *
from .settings import global_settings

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def eeprint(*args, **kwargs):
    return_code=1
    if 'return_code' in kwargs:
        return_code = kwargs['return_code']
        del kwargs['return_code']
    print(*args, file=sys.stderr, **kwargs)
    exit(return_code)

class xxh:
    def __init__(self):
        self.package_dir_path = p(f"{__file__}").parent
        self.url_xxh_github = 'https://github.com/xxh/xxh'
        self.url_xxh_plugins_search = 'https://github.com/search?q=xxh-plugin'
        self.local_xxh_version = global_settings['XXH_VERSION']
        self.local_xxh_home = p('~/.xxh')
        self.config_file = self.local_xxh_home / '.xxhc'
        self.host_xxh_home = '~/.xxh'
        self.default_shells = {
            'xxh-shell-xonsh-appimage': {
                'alias': 'xonsh',
                'source': 'https://github.com/xxh/xxh-shell-xonsh-appimage.git'
            },
            'xxh-shell-zsh': {
                'alias': 'zsh',
                'source': 'https://github.com/xxh/xxh-shell-zsh.git'
            },
            'xxh-shell-fish-appimage': {
                'alias': 'fish',
                'source': 'https://github.com/xxh/xxh-shell-fish-appimage.git'
            },
            'xxh-shell-bash-zero': {
                'alias': 'bash-zero',
                'source': 'https://github.com/xxh/xxh-shell-bash-zero.git'
            },
            'xxh-shell-osquery': {
                'alias': 'osquery',
                'source': 'https://github.com/xxh/xxh-shell-osquery.git'
            }
        }
        self.default_shells_aliases = {d['alias']:s for s,d in self.default_shells.items() if 'alias' in d}
        current_shell = self.get_current_shell()
        current_shell = self.default_shells_aliases[current_shell] if current_shell in self.default_shells_aliases else current_shell
        self.shell = current_shell
        self.build_file_exts = ['xsh', 'zsh', 'fish', 'sh']
        self.url = None
        self.ssh_arguments = []
        self.ssh_arg_v = []
        self.sshpass = []
        self.use_pexpect = True
        self._password = None
        self._verbose = False
        self._vverbose = False
        self.quiet = False
        self.os = os.name

    def eprint(self, *args, **kwargs):
        if not self.quiet:
            eprint(*args, **kwargs)

    def eeprint(self, *args, **kwargs):
        eeprint(*args, **kwargs)

    def get_current_shell(self):
        if 'SHELL' in os.environ:
            if os.environ['SHELL'].endswith('zsh'):
                return 'zsh'
            if os.environ['SHELL'].endswith('fish'):
                return 'fish'
        return 'xonsh'

    def stripunquote(self, s):
        s = s.strip()
        if s.startswith('"') and s.endswith('"'):
            s = s[1:-1]
        return s

    def get_xxh_env(self):
        xxh_env = {}
        if 'XXH_SH_ENV' in os.environ:
            xxh_env = os.environ['XXH_SH_ENV']
            for kw in ['declare', 'typeset', 'export']:
                xxh_env = xxh_env.replace('\n' + kw + ' ', '\n\n' + kw + ' ')
            xxh_env += '\n\n'
            xxh_env = re.findall('^.+ ([a-zA-Z_0-9]+?)=((?:.+\n)+)', xxh_env, re.MULTILINE)
            xxh_env = {v[0]: self.stripunquote(v[1]) for v in xxh_env}
        return xxh_env

    def pssh(self, cmd, accept_host=None, host_password=None, key_password=None):
        if self.password:
            host_password = self.password

        if self.vverbose:
            self.eprint('Try pexpect command: '+cmd)

        sess = pexpect.spawn(cmd)
        user_host_accept = None
        user_host_password = None
        user_key_password = None
        patterns = ['Are you sure you want to continue connecting.*', "Please type 'yes' or 'no':",
                    'Enter passphrase for key.*', 'password:', pexpect.EOF, '[$#~]', 'Last login.*']
        while True:
            try:
                i = sess.expect(patterns, timeout=3)
            except:
                if self.vverbose:
                    print('Unknown answer details:')
                    print(sess)
                print('Unknown answer from host')
                return {}

            if self.vverbose:
                self.eprint(f'Pexpect caught pattern: {patterns[i]}')

            if i in [0,1]:
                # Expected:
                #   The authenticity of host '<...>' can't be established.
                #   ECDSA key fingerprint is <...>
                #   Are you sure you want to continue connecting (yes/no)?
                print((sess.before + sess.after).decode("utf-8"), end='')
                if accept_host is None:
                    user_host_accept = input()
                    sess.sendline(user_host_accept)
                    if user_host_accept == 'yes':
                        user_host_accept = True
                    elif user_host_accept == 'no':
                        user_host_accept = False
                    else:
                        user_host_accept = None
                elif accept_host:
                    sess.sendline('yes')
                else:
                    sess.sendline('no')

            if i == 2:
                # Expected:
                #   Enter passphrase for key '<keyfile>':
                if key_password is None:
                    user_key_password = getpass.getpass(prompt=(sess.before + sess.after).decode("utf-8")+' ')
                    sess.sendline(user_key_password)
                else:
                    sess.sendline(key_password)

            if i == 3:
                # Expected:
                #   <host>`s password:
                if host_password is None:
                    user_host_password = getpass.getpass(prompt=(sess.before + sess.after).decode("utf-8")+' ')
                    sess.sendline(user_host_password)
                else:
                    sess.sendline(host_password)

            if i == 4:
                # Getting result
                output = sess.before.decode("utf-8")
                output = re.sub('\r\nConnection to (.*) closed.\r\r\n', '', output)
                output = output[:-3] if output.endswith('\r\r\n') else output
                output = output[3:] if output.startswith(' \r\n') else output
                result = {
                    'user_host_accept': user_host_accept,
                    'user_host_password':user_host_password,
                    'user_key_password':user_key_password,
                    'output':output
                }

                return result

            if i == [5,6]:
                # Prompt
                print(sess.before.decode("utf-8"))
                sess.interact()

                result = {
                    'user_host_accept': user_host_accept,
                    'user_host_password':user_host_password,
                    'user_key_password':user_key_password
                }
                return result

        return {}

    def shells(self):
        default_shells = [k for k,v in self.default_shells.items()]
        installed_shells = [str(s.name) for s in p(f'{self.local_xxh_home}/xxh/shells').glob('*')]
        available_shells = list(set(default_shells + installed_shells))
        defaults = [('%s (%s)'%(v['alias'], k) if 'alias' in v else k)  for k,v in self.default_shells.items()]
        list_str = ', '.join(defaults + [s for s in available_shells if s not in default_shells])

        return {
            'default': default_shells,
            'installed': installed_shells,
            'available': available_shells,
            'available_help': list_str
        }

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password
        if password:
            if not which('sshpass'):
                self.eeprint('Install sshpass to using password: https://duckduckgo.com/?q=install+sshpass\n'
                             + 'Note! There are a lot of security reasons to stop using password auth.')
            verbose = '-v' if '-v' in self.sshpass else []
            self.sshpass = ['sshpass', '-p', password] + verbose
        else:
            self.sshpass = []

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value
        if not self._verbose:
            self.vverbose=False

    @property
    def vverbose(self):
        return self._vverbose

    @vverbose.setter
    def vverbose(self, value):
        self._vverbose = value
        if self._vverbose:
            self.verbose = True
            self.ssh_arg_v = ['-v']
            if self.sshpass and ['-v'] not in self.sshpass:
                self.sshpass += ['-v']
        else:
            self.ssh_arg_v = []
            if '-v' in self.sshpass:
                self.sshpass.remove('-v')

    def parse_destination(self, destination):
        destination = f'ssh://{destination}' if 'ssh://' not in destination else destination
        url = urlparse(destination)
        return url

    def get_host_info(self):
        if '|' in self.host_xxh_home:
            self.eeprint(f'Wrong host xxh home: {self.host_xxh_home}')

        host = self.url.hostname
        host_info_sh = self.package_dir_path / 'host_info.sh'
        if self.use_pexpect:
            cmd = "bash -c 'cat {host_info_sh} | sed \"s|_xxh_home_|{host_xxh_home}|\" | sed \"s|_xxh_shell_|{shell}|\" | ssh {ssh_v} {ssh_arguments} {host} -T \"bash -s\"'".format(
                host_info_sh=host_info_sh, host_xxh_home=self.host_xxh_home, shell=self.shell, ssh_v=('' if not self.ssh_arg_v else '-v'), ssh_arguments=' '.join(self.ssh_arguments), host=host)
            pr = self.pssh(cmd)

            if pr == {}:
                self.eeprint('Unexpected result. Try again with +v or +vv or try ssh before xxh')

            if self.verbose:
                self.eprint('Pexpect result:')
                self.eprint(pr)

            if pr['user_host_password'] is not None:
                self.password = pr['user_host_password']

            r = pr['output']
        else:
            [o,e,p] = SC("cat {host_info_sh} | sed 's|_xxh_home_|{host_xxh_home}|' | {sshpass} ssh {ssh_arg_v} {ssh_arguments} {host} -T \"bash -s\"".format(
                host_info_sh=A(host_info_sh),
                host_xxh_home=A(self.host_xxh_home),
                sshpass=A(self.sshpass),
                ssh_arg_v=A(self.ssh_arg_v),
                ssh_arguments=A(self.ssh_arguments),
                host=A(host)
            ))
            r = o.strip()
            print(r)
            exit()

        if self.verbose:
            self.eprint(f'Host info:\n{r}')

        if r == '':
            self.eeprint('Empty answer from host when getting first info. Often this is a connection error.\n'
                    + 'Check your connection parameters using the same command but with ssh.')

        r = dict([l.split('=') for l in r.replace('\r','').split('\n') if l.strip() != '' and '=' in l])

        return r

    def prepare_env_args(self, envs, to_base64=True):
        env_args=[]
        if envs:
            for e in envs:
                el = e.split('=', 1)
                if len(el) != 2:
                    self.eeprint(f'Wrong environment (expected NAME=VAL): {e}')
                if not re.match('^[a-zA-Z_]+$', el[0]):
                    self.eeprint(f'Wrong environment NAME (expected [a-zA-Z-]): {el[0]}')

                val = el[1]
                if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
                    val=val[1:-1]

                if to_base64:
                    val = self.b64e(val)

                env_args += ['-e', "%s=%s" % ( el[0], val ) ]
        return env_args

    def b64e(self, s):
        return b64encode(s.encode()).decode()

    def create_xxh_env(self):
        home = p(self.local_xxh_home)
        if not home.exists():
            S(f"mkdir -p {home} {home / 'xxh/shells'} {home / 'xxh/plugins'}")

        config_file = p(self.config_file)
        sample_config_file = self.package_dir_path / 'config.xxhc'
        if not config_file.exists() and sample_config_file.exists():
            S(f'cp {sample_config_file} {config_file}')

    def d2F0Y2ggLW4uMiB4eGggLWg(self):
        try:
            terminal = os.get_terminal_size()
            terminal_cols = terminal.columns
        except:
            terminal_cols=70
        if terminal_cols < 70:
            return f"\n\nContribution: {self.url_xxh_github}\n\nPlugins: {self.url_xxh_plugins_search}"
        l,r,s,t = (['@','-','_'][randint(0,2)], ['@','-','_'][randint(0,2)], ['_',' '][randint(0,1)], ['_',''][randint(0,1)])
        return f"\n" \
            +f"     {s}___  __________     {l}    {r}\n" \
            +f"  {s}_____  /          \\     \\__/\n" \
            +f"   {s}___  /    ______  \\   /   \\           contribution\n" \
            +f" {s}____  /    / __   \\  \\ /   _/   {self.url_xxh_github}\n" \
            +f"   {s}__ (    / /  /   \\  \\   /\n" \
            +f"        \\   \\___/    /  /  /                plugins\n" \
            +f"{' ' if not t else ''}     _{t}__\\          /__/  /   {self.url_xxh_plugins_search}\n" \
            +f"{' ' if not t else ''}    / {'' if not t else ' '}   \\________/     /\n" \
            +f"{' ' if not t else ''}   /_{t}__________________/\n" \
            +f""

    def packages_install(self, packages):
        arg_q = '-q' if self.quiet else ''
        supported_xxh_packages = ['shell', 'plugin']
        supported_source_types = ['git', 'path']
        supported_xxh_packages_regex = '|'.join(supported_xxh_packages)
        supported_source_types_regex = '|'.join(supported_source_types)
        package_name_regex = f'xxh\-({supported_xxh_packages_regex})-[a-zA-Z0-9_-]+'
        for package in packages:
            subdir = self.package_subdir(package)
            package_dir = self.local_xxh_home / 'xxh' / str(subdir) / package
            if package_dir.exists():
                if self.vverbose:
                    self.eprint(f'Package exists, skip install: {package_dir}')
                continue

            self.eprint(f'Install {package} to local {package_dir}')

            package_name = package
            package_source_type = 'git'
            package_source = f'https://github.com/xxh/{package}'

            parse_source = False
            if package_name in self.default_shells.keys():
                package_source = self.default_shells[package_name]['source']
                parse_source = True
            elif package_name in self.default_shells_aliases.keys():
                package_name = self.default_shells_aliases[package_name]
                package_source = self.default_shells[ package_name ]['source']
                parse_source = True

            if '+' in package_name or parse_source:
                g = re.match(f'^({package_name_regex})\+({supported_source_types_regex})\+(.+)$', package_name)
                if g:
                    package_name = g.group(1)
                    package_source_type = g.group(3)
                    package_source = g.group(4)

            if not re.match(f'^{package_name_regex}$', package_name):
                self.eeprint(f'Invalid package name: {package_name}\n'
                             + f'  Package name format: {package_name_regex}\n'
                             + f'  Package name with source format: xxh-({supported_xxh_packages_regex})-(<package_name>)+({supported_source_types_regex})+(<url>|<path>)')

            subdir = self.package_subdir(package_name) or self.eeprint(f"Unknown package type: {package_name}")

            package_dir = self.local_xxh_home/'xxh'/subdir/package_name
            if package_dir.exists() and len(list(package_dir.glob('*'))) != 0:
                self.eprint(f'Skip installed package: {package_dir}')
                continue

            if package_source_type == 'git':
                self.eprint(f"Git clone {package_source}")
                [o,e,proc] = SC(f'git clone {arg_q} --depth 1 {package_source} {package_dir} 1>&2')
                if proc.returncode != 0:
                    self.eeprint(f'Error:\n{o.decode().strip()}\n{e.decode().strip()}')
            elif package_source_type == 'url':
                self.eeprint(f'URL source type is not supported yet. Contribute: https://github.com/xxh/xxh')
            elif package_source_type == 'path':
                self.eprint(f"Package source path: {package_source}")
                package_source = p(package_source)
                if package_source.exists():
                    S(f'mkdir -p {package_dir} && cp -r {package_source}/* {package_dir}')
            else:
                self.eeprint(f'Unknown source type: {package_source_type}')

            self.eprint(f"Build {package_name}")
            build_file_found = False
            for ext in self.build_file_exts:
                build_file = package_dir / f'build.{ext}'
                if build_file.exists():
                    S(f'{build_file} {arg_q} 1>&2')
                    build_file_found = True
                    break
            if not build_file_found:
                self.eeprint(f"Build file not found in {package_dir}")

            self.eprint(f"Installed {package_dir}")

    def packages_remove(self, packages):
        for package in packages:
            self.eprint(f'Remove {package}')
            subdir = self.package_subdir(package) or self.eeprint(f"Unknown package: {package}")
            package_dir = self.local_xxh_home / 'xxh' / subdir / package
            if package_dir.exists():
                S(f'rm -rf {package_dir}')
                self.eprint(f"Removed {package_dir}")

    def packages_reinstall(self, packages):
        self.packages_remove(packages)
        return self.packages_install(packages)

    def packages_list(self, packages=None):
        packages_dir = (self.local_xxh_home / 'xxh').glob('**/xxh-*')
        for p in sorted(packages_dir):
            if packages:
                if p.name in packages:
                    print(p.name)
            else:
                print(p.name)

    def package_subdir(self, name):
        if 'xxh-shell' in name:
            return 'shells'
        elif 'xxh-plugin' in name:
            return 'plugins'
        return None


    def main(self):
        argp = argparse.ArgumentParser(description=f"Your favorite shell wherever you go through the ssh.\n{self.d2F0Y2ggLW4uMiB4eGggLWg()}", formatter_class=RawTextHelpFormatter, prefix_chars='-+')
        argp.add_argument('--version', '-V', action='version', version=f"xxh/{self.local_xxh_version}")
        argp.add_argument('-p', dest='ssh_port', help="Port to connect to on the remote host.")
        argp.add_argument('-l', dest='ssh_login', help="Specifies the user to log in as on the remote machine.")
        argp.add_argument('-i', dest='ssh_private_key', help="File from which the identity (private key) for public key authentication is read.")
        argp.add_argument('-o', dest='ssh_options', metavar='SSH_OPTION -o ...', action='append', help="SSH options are described in ssh man page. Example: -o Port=22 -o User=snail")
        argp.add_argument('+P','++password', help="Password for ssh auth.")
        argp.add_argument('+PP','++password-prompt', default=False, action='store_true', help="Enter password manually using prompt.")
        argp.add_argument('destination', nargs='?', metavar='[user@]host[:port]', help="Destination may be specified as [ssh://][user@]host[:port] or host from ~/.ssh/config")
        argp.add_argument('+i','++install', default=False, action='store_true', help="Install xxh to destination host.")
        argp.add_argument('+if','++install-force', default=False, action='store_true', help="Removing the host xxh package and install xxh again.")
        argp.add_argument('+iff','++install-force-full', default=False, action='store_true', help="Removing the host xxh home and install xxh again. All installed packages on the host (e.g. pip packages) will be lost.")
        argp.add_argument('+xc','++xxh-config', default=self.config_file, help=f"Xxh config file in yaml. Default: {self.config_file}")
        argp.add_argument('+e','++env', dest='env', metavar='NAME=VAL +e ...', action='append', help="Setting environment variables if supported by shell entrypoint.")
        argp.add_argument('+eb','++envb', dest='envb', metavar='NAME=BASE64 +eb ...', action='append', help="Setting environment variables base64 encoded if supported by shell entrypoint.")
        argp.add_argument('+lh','++local-xxh-home', default=self.local_xxh_home, help=f"Local xxh home path. Default: {self.local_xxh_home}")
        argp.add_argument('+hh','++host-xxh-home', default=self.host_xxh_home, help=f"Host xxh home path. Default: {self.host_xxh_home}")
        argp.add_argument('+hhr','++host-xxh-home-remove', action='store_true', help=f"Remove xxh home on host after disconnect.")
        argp.add_argument('+hf','++host-execute-file', help=f"Execute script file placed on host and exit. If supported by shell entrypoint.")
        argp.add_argument('+hc','++host-execute-command', help=f"Execute command on host and exit. If supported by shell entrypoint.")
        argp.add_argument('+heb','++host-execute-bash', dest='host_execute_bash', metavar='BASE64 +heb ...', action='append', help="Bash command will be executed before shell entrypoint (base64 encoded) if supported by shell entrypoint.")
        argp.add_argument('+s','++shell', default=self.shell, help="Xxh shell: " + self.shells()['available_help'])
        argp.add_argument('+v','++verbose', default=False, action='store_true', help="Verbose mode.")
        argp.add_argument('+vv','++vverbose', default=False, action='store_true', help="Super verbose mode.")
        argp.add_argument('+q','++quiet', default=False, action='store_true', help="Quiet mode.")
        argp.add_argument('+I','++install-xxh-packages', action='append', metavar='xxh-package', dest='install_xxh_packages', help="Local install xxh packages.")
        argp.add_argument('+L','++list-xxh-packages', nargs='*', metavar='xxh-package', dest='list_xxh_packages', help="List local xxh packages.")
        argp.add_argument('+RI','++reinstall-xxh-packages', action='append', metavar='xxh-package', dest='reinstall_xxh_packages', help="Local reinstall xxh packages.")
        argp.add_argument('+R','++remove-xxh-packages', action='append', metavar='xxh-package', dest='remove_xxh_packages', help="Local remove xxh packages.")
        argp.add_argument('+ES','++extract-sourcing-files', action='store_true', dest='extract_sourcing_files', help="Used for AppImage. Extract sourcing files.")
        argp.usage = "xxh <host from ~/.ssh/config>\n" \
            + "usage: xxh [ssh arguments] [user@]host[:port] [xxh arguments]\n" \
            + "usage: xxh [-p SSH_PORT] [-l SSH_LOGIN] [-i SSH_PRIVATE_KEY]\n" \
            + "           [-o SSH_OPTION -o ...] [+P PASSWORD] [+PP]\n" \
            + "           [user@]host[:port]\n" \
            + "           [+i] [+if] [+iff] [+hhr] [+s SHELL] [+e NAME=VAL +e ...] [+v] [+vv] [+q]\n" \
            + "           [+hh HOST_XXH_HOME] [+hf HOST_EXEC_FILE] [+hc HOST_EXEC_CMD]\n" \
            + "           [+xc CONFIG_FILE] [+lh LOCAL_XXH_HOME] [-h] [-V]\n" \
            + "usage: xxh [+I xxh-package +I ...] [+L] [+RI xxh-package +RI ...] [+R xxh-package +R ...]\n"

        help = argp.format_help().replace('\n  +','\n\nxxh arguments:\n  +',1).replace('optional ', 'common ')\
            .replace('number and exit', 'number and exit\n\nssh arguments:').replace('positional ', 'required ') \
            .replace('Quiet mode.', 'Quiet mode.\n\nxxh packages:')
        argp.format_help = lambda: help
        opt = argp.parse_args()

        if opt.extract_sourcing_files:
            cdir = p(sys.argv[0]).absolute().parent
            S(f'cp {self.package_dir_path}/xxh.*sh {cdir}')
            print(f'Sourcing files extracted to {cdir}')
            exit(0)

        self.local_xxh_home = p(f"{opt.local_xxh_home}")
        self.config_file = self.local_xxh_home/'.xxhc'
        self.create_xxh_env()
        xxh_config_file = p(opt.xxh_config)

        if self.config_file != xxh_config_file and not xxh_config_file.exists():
            self.eeprint(f'Config does not exist: {xxh_config_file}')
        else:
            self.config_file = xxh_config_file

        self.quiet = opt.quiet
        arg_q = ['-q'] if self.quiet else []
        if not self.quiet:
            self.verbose = opt.verbose
            self.vverbose = opt.vverbose

        if not opt.destination:
            opt.destination = '`'

        self.url = url = self.parse_destination(opt.destination)

        if self.config_file.exists():
            if self.verbose:
                self.eprint(f'Load xxh config from {self.config_file}')
            with open(self.config_file) as f:
                xxh_config = yaml.safe_load(f)

            if xxh_config and 'hosts' in xxh_config:
                sys_args = sys.argv[1:]
                conf_args = []
                for h, hc in xxh_config['hosts'].items():
                    if re.match(h, url.hostname):
                        if self.verbose:
                            self.eprint('Load xxh config for host ' + h)
                        if hc and len(hc) > 0:
                            for k, v in hc.items():
                                conf_args += [k, v] if v is not None else [k]
                                if k in ['+P', '++password']:
                                    current_user = getpass.getuser()
                                    current_mode = oct(self.config_file.stat().st_mode)[-4:]
                                    if self.config_file.owner() != current_user or current_mode != '0600':
                                        self.eprint('\n\033[0;93mWARN! There is password in the config file but the file is too open!\n'
                                               + f'Run to restrict: chown {current_user}:{current_user} {self.config_file} && chmod 0600 {self.config_file}\033[0m\n')
                args = conf_args + sys_args
                if opt.verbose:
                    print('Final arguments list: ' + str(args))
                opt = argp.parse_args(args)

        self.verbose = opt.verbose
        self.vverbose = opt.vverbose

        if opt.install_xxh_packages:
            self.packages_install(opt.install_xxh_packages)
        if opt.reinstall_xxh_packages:
            self.packages_reinstall(opt.reinstall_xxh_packages)
        if opt.remove_xxh_packages:
            self.packages_remove(opt.remove_xxh_packages)
        if opt.list_xxh_packages or opt.list_xxh_packages == []:
            self.packages_list(opt.list_xxh_packages)

        if not opt.destination or opt.destination == '`':
            self.eeprint(argp.format_usage()+'\nThe following arguments are required: [user@]host[:port]')

        if opt.shell in self.default_shells_aliases:
            opt.shell = self.default_shells_aliases[opt.shell]

        self.shell = opt.shell

        username = getpass.getuser()
        host = url.hostname
        if not host:
            self.eeprint(f"Wrong destination '{host}'")
        if url.port:
            opt.ssh_port = url.port
        if url.username:
            opt.ssh_login = url.username
        if opt.ssh_login:
            username = opt.ssh_login

        self.ssh_arguments = ['-o', 'StrictHostKeyChecking=accept-new']
        if not self.verbose:
           self.ssh_arguments += ['-o', 'LogLevel=QUIET']
        if opt.ssh_port:
            self.ssh_arguments += ['-o', f'Port={opt.ssh_port}']
        if opt.ssh_private_key:
            self.ssh_arguments += ['-o', f'IdentityFile={opt.ssh_private_key}']
        if opt.ssh_login:
            self.ssh_arguments += ['-o', f'User={opt.ssh_login}']
        if opt.ssh_options:
            for ssh_option in opt.ssh_options:
                self.ssh_arguments += ['-o', ssh_option]

        if self.verbose:
            self.eprint(f'ssh arguments: {self.ssh_arguments}')

        if opt.password is not None:
            self.password = opt.password
        elif opt.password_prompt:
            password = ''
            while not password:
                password = getpass.getpass(f"Enter {username}@{host}'s password: ")
            self.password = password

        env_args = self.prepare_env_args(opt.env)
        env_args += self.prepare_env_args(opt.envb, to_base64=False)

        if opt.host_execute_bash:
            for heb in opt.host_execute_bash:
                env_args += ['-b', heb]

        opt.install = True if opt.install_force or opt.install_force_full else opt.install

        local_xxh_home_parent = self.local_xxh_home.parent

        if self.local_xxh_home.exists():
            if not os.access(self.local_xxh_home, os.W_OK):
                self.eeprint(f"The local xxh home path isn't writable: {self.local_xxh_home}" )
        elif local_xxh_home_parent.exists():
            if not os.access(local_xxh_home_parent, os.W_OK):
                self.eeprint(f"Parent for local xxh home path isn't writable: {local_xxh_home_parent}")
        else:
            self.eeprint(f"Paths aren't writable:\n  {local_xxh_home_parent}\n  {self.local_xxh_home}")

        local_plugins_dir = self.local_xxh_home / 'xxh/plugins'
        S("mkdir {ssh_arg_v} -p {local_xxh_home} {local_plugins_dir} {shells_dir}".format(
            ssh_arg_v=A(self.ssh_arg_v),
            local_xxh_home=self.local_xxh_home,
            local_plugins_dir=local_plugins_dir,
            shells_dir=(self.local_xxh_home / 'xxh/shells')
        ))

        if p(opt.host_xxh_home) == p(f'/'):
            self.eeprint("Host xxh home path {host_xxh_home} looks like /. Please check twice!")

        self.host_xxh_home = opt.host_xxh_home
        host_info = self.get_host_info()

        if not host_info:
            self.eeprint(f'Unknown answer from host when getting info')

        if 'xxh_home_realpath' not in host_info or host_info['xxh_home_realpath'] == '':
            self.eeprint(f'Unknown answer from host when getting realpath for directory {host_xxh_home}')

        if 'xxh_version' not in host_info or host_info['xxh_version'] == '':
            self.eeprint(f'Unknown answer from host when getting version for directory {host_xxh_home}')

        host_xxh_home = host_info['xxh_home_realpath']
        host_xxh_home = p(f"{host_xxh_home}")
        host_xxh_version = host_info['xxh_version']

        if host_info['xxh_home_writable'] == '0' and host_info['xxh_parent_home_writable'] == '0':
            yn = input(f"{host}:{host_xxh_home} is not writable. Continue? [y/n] ").strip().lower()
            if yn != 'y':
                self.eeprint('Stopped')

        if host_info['scp'] == '' and host_info['rsync'] == '':
            self.eeprint(f"There are no rsync or scp on target host. Sad but files can't be uploaded.")

        if opt.install_force == False and opt.install_force_full == False:

            # Check version

            ask = False
            if host_xxh_version == 'version_not_found':
                ask = f'Host xxh home is not empty but something went wrong while getting host xxh version.'
            elif host_xxh_version not in ['dir_not_found','dir_empty'] and host_xxh_version != self.local_xxh_version:
                ask = f"Local xxh version '{self.local_xxh_version}' is not equal host xxh version '{host_xxh_version}'."

            if ask:
                choice = input(f"{ask} What's next? \n"
                               + " s  - Stop here. You'll try to connect using ordinary ssh for backup current xxh home.\n"
                               + " u  - Safe update. Host xxh home will be renamed and local xxh version will be installed.\n"
                               + " f  - [default] Force reinstall xxh. Installed packages (e.g. pip) will be saved.\n"
                               + " ff - Force full reinstall on host. Installed packages (e.g. pip) will be lost.\n"
                               + " i  - Ignore, cross fingers and continue the connection.\n"
                               + "s/u/F/i? ").lower()

                if choice == 's':
                    print('Stopped')
                    exit(0)
                elif choice == 'u':
                    local_time = datetime.datetime.now().isoformat()[:19]
                    self.eprint(f"Move {host}:{host_xxh_home} to {host}:{host_xxh_home}-{local_time}")
                    S('echo "mv {host_xxh_home} {host_xxh_home}-{local_time}" | {sshpass} ssh {ssh_arg_v} {ssh_arguments} {host} -T "bash -s"'.format(
                        host_xxh_home=A(host_xxh_home),
                        local_time=A(local_time),
                        sshpass=A(self.sshpass),
                        ssh_arg_v=A(self.ssh_arg_v),
                        ssh_arguments=A(self.ssh_arguments),
                        host=A(host)
                    ))
                    opt.install = True
                elif choice == 'f' or choice.strip() == '':
                    opt.install = True
                    opt.install_force = True
                elif choice == 'ff':
                    opt.install = True
                    opt.install_force_full = True
                elif choice == 'i':
                    pass
                else:
                    self.eeprint('Unknown answer')

        if (host_xxh_version in ['dir_not_found', 'dir_empty'] or host_info['xxh_shell_exists'] == '0') and opt.install_force == False and opt.install_force_full == False:
            yn = input(f"{host}:{host_xxh_home}/xxh/shells/{self.shell} not found. Install {self.shell}? [Y/n] ").strip().lower()
            if yn == 'y' or yn == '':
                opt.install = True
            else:
                self.eeprint('Unknown answer')

        if opt.install:
            self.eprint(f"Install {self.shell} to {host}:{host_xxh_home}" )

            # Download xxh shell
            self.packages_install([self.shell])

            # Build xxh packages

            if self.shell.startswith('xxh-shell-'):
                short_shell_name = self.shell.split('-')[2]
            else:
                short_shell_name = self.shell

            base_dir = self.local_xxh_home / 'xxh'
            shell_build_dir = base_dir / 'shells' / self.shell / 'build'
            build_packages = list([base_dir / 'shells' / self.shell]) + list( (base_dir / 'plugins').glob(f'*-{short_shell_name}-*') )

            for package_dir in build_packages:
                package_name = package_dir.name
                build_dir = package_dir / 'build'
                if not build_dir.exists():
                    build_file_found = False
                    for ext in self.build_file_exts:
                        build_file = package_dir / f'build.{ext}'
                        if build_file.exists():
                            self.eprint(f"First time build {package_dir}")
                            S(f'{build_file} {A(arg_q)} 1>&2')
                            build_file_found = True
                            break
                    if not build_file_found:
                        self.eeprint(f"Build file not found in {package_dir}")

            # Remove xxh home directories

            if opt.install_force_full:
                self.eprint(f'Remove {host}:{host_xxh_home}')
                S('echo "rm -rf {host_xxh_home}" | {sshpass} ssh {ssh_arg_v} {ssh_arguments} {host} -T "bash -s"'.format(
                    host_xxh_home=host_xxh_home,
                    sshpass=A(self.sshpass),
                    ssh_arg_v=A(self.ssh_arg_v),
                    ssh_arguments=A(self.ssh_arguments),
                    host=A(host),

                ))
            elif opt.install_force:
                self.eprint(f'Remove {host}:{host_xxh_home}/xxh')
                S('echo "rm -rf {host_xxh_home}/xxh" | {sshpass} ssh {ssh_arg_v} {ssh_arguments} {host} -T "bash -s"'.format(
                    host_xxh_home=host_xxh_home,
                    sshpass=A(self.sshpass),
                    ssh_arg_v=A(self.ssh_arg_v),
                    ssh_arguments=A(self.ssh_arguments),
                    host=A(host)
                ))

            # Create host xxh home directories

            host_xxh_plugins_dir = host_xxh_home / 'xxh/plugins'
            host_xxh_dirs_str = ''
            for local_plugin_dir in local_plugins_dir.glob(f'*-{short_shell_name}-*'):
                local_plugin_build_dir = local_plugin_dir / 'build'
                host_plugin_build_dir = str(local_plugin_build_dir).replace(str(self.local_xxh_home), str(host_xxh_home))
                host_xxh_dirs_str += ' ' + host_plugin_build_dir

            host_xxh_package_dir = host_xxh_home  / 'xxh/package'
            host_xxh_shell_dir = host_xxh_home / f'xxh/shells/{self.shell}'
            host_xxh_shell_build_dir = host_xxh_shell_dir  / 'build'
            S('echo "mkdir -p {host_xxh_package_dir} {host_xxh_shell_build_dir} {host_xxh_dirs_str}" | {sshpass} ssh {ssh_arg_v} {ssh_arguments} {host} -T "bash -s"'.format(
                host_xxh_package_dir=host_xxh_package_dir,
                host_xxh_shell_build_dir=host_xxh_shell_build_dir,
                host_xxh_dirs_str=host_xxh_dirs_str,
                host_xxh_home=host_xxh_home,
                sshpass=A(self.sshpass),
                ssh_arg_v=A(self.ssh_arg_v),
                ssh_arguments=A(self.ssh_arguments),
                host=A(host)
            ))

            # Upload files

            if which('rsync') and host_info['rsync']:
                self.eprint('First time upload using rsync (this will be omitted on the next connections)')

                rsync = "rsync {ssh_arg_v} -e \"{sshpass} ssh {ssh_arg_v} {ssh_arguments}\" {arg_q} -az {progress} --cvs-exclude".format(
                    host_xxh_home=host_xxh_home,
                    sshpass=A(self.sshpass),
                    ssh_arg_v=('' if self.ssh_arg_v == [] else '-v'),
                    ssh_arguments=A(self.ssh_arguments),
                    arg_q=A(arg_q),
                    progress=('' if self.quiet or not self.verbose else '--progress')
                )
                S("{rsync} {package_dir_path}/settings.py {host}:{host_xxh_package_dir}/ 1>&2".format(
                    rsync=rsync,
                    host=A(host),
                    package_dir_path=self.package_dir_path,
                    host_xxh_package_dir=host_xxh_package_dir
                ))

                S("{rsync} {shell_build_dir}/ {host}:{host_xxh_shell_build_dir}/ 1>&2".format(
                    rsync=rsync,
                    host=A(host),
                    shell_build_dir=shell_build_dir,
                    host_xxh_shell_build_dir=host_xxh_shell_build_dir
                ))
                for local_plugin_dir in local_plugins_dir.glob(f'*-{short_shell_name}-*'):
                    local_plugin_build_dir = local_plugin_dir/'build'
                    local_plugin_name = local_plugin_dir.name
                    S("{rsync} {local_plugin_build_dir}/* {host}:{host_xxh_plugins_dir}/{local_plugin_name}/build/ 1>&2".format(
                        rsync=rsync,
                        host=A(host),
                        local_plugin_build_dir=local_plugin_build_dir,
                        host_xxh_plugins_dir=host_xxh_plugins_dir,
                        local_plugin_name=local_plugin_name
                    ))
            elif which('scp') and host_info['scp']:
                self.eprint("First time upload using scp (this will be omitted on the next connections).\nNote: you can install rsync on local and remote host to increase speed.")
                scp = "{sshpass} scp {ssh_arg_v} {ssh_arguments} -r -C {arg_q}".format(
                    sshpass=A(self.sshpass),
                    ssh_arg_v=A(self.ssh_arg_v),
                    ssh_arguments=A(self.ssh_arguments),
                    arg_q=A(arg_q)
                )
                S('{scp} {package_dir_path}/settings.py {host}:{host_xxh_package_dir}/ 1>&2'.format(
                    scp=scp,
                    package_dir_path=self.package_dir_path,
                    host=host,
                    host_xxh_package_dir=host_xxh_package_dir
                ))
                S('{scp} {shell_build_dir} {host}:{host_xxh_shell_dir}/ 1>&2'.format(
                    scp=scp,
                    shell_build_dir=shell_build_dir,
                    host=host,
                    host_xxh_shell_dir=host_xxh_shell_dir
                ))

                for local_plugin_dir in local_plugins_dir.glob(f'*-{short_shell_name}-*'):
                    local_plugin_build_dir = local_plugin_dir/'build'
                    local_plugin_name = local_plugin_dir.name
                    S('{scp} {local_plugin_build_dir}/* {host}:{host_xxh_plugins_dir}/{local_plugin_name}/build/ 1>&2'.format(
                        scp=scp,
                        local_plugin_build_dir=local_plugin_build_dir,
                        host=host,
                        host_xxh_plugins_dir=host_xxh_plugins_dir,
                        local_plugin_name=local_plugin_name
                    ))

            else:
                self.eprint('Please install rsync or scp!')

            self.eprint(f'First run {self.shell} on {host}')

        # Connect to host

        host_execute_file = host_execute_command = []
        if opt.host_execute_file:
            host_execute_file = ['-f', opt.host_execute_file]
        elif opt.host_execute_command:
            host_execute_command = ['-C', self.b64e(opt.host_execute_command)]

        host_entrypoint_verbose = []
        if self.vverbose:
            host_entrypoint_verbose = ['-v', '2']
        elif self.verbose:
            host_entrypoint_verbose = ['-v', '1']

        lcs = []
        for lc in ['LC_TIME','LC_MONETARY','LC_ADDRESS','LC_IDENTIFICATION','LC_MEASUREMENT','LC_NAME','LC_NUMERIC','LC_PAPER','LC_TELEPHONE']:
            lcs.append(f"{lc}=POSIX")

        S("{lcs} {sshpass} ssh {ssh_arg_v} {ssh_arguments} {host} -t 'bash {entrypoint} {host_execute_file} {host_execute_command} {host_entrypoint_verbose} {env_args}'".format(
            lcs=A(lcs),
            sshpass=A(self.sshpass),
            ssh_arg_v=A(self.ssh_arg_v),
            ssh_arguments=A(self.ssh_arguments),
            host=A(host),
            entrypoint=A(str(host_xxh_home/'xxh/shells'/self.shell/'build/entrypoint.sh')),
            host_execute_file=A(host_execute_file),
            host_execute_command=A(host_execute_command),
            host_entrypoint_verbose=A(host_entrypoint_verbose),
            env_args=A(env_args)
        ))

        if opt.host_xxh_home_remove:
            if self.verbose:
                self.eprint(f'Remove {host}:{host_xxh_home}')
            S('echo "rm -rf {host_xxh_home}" | {sshpass} ssh {ssh_arg_v} {ssh_arguments} {host} -T "bash -s"'.format(
                host_xxh_home=host_xxh_home,
                sshpass=A(self.sshpass),
                ssh_arg_v=A(self.ssh_arg_v),
                ssh_arguments=A(self.ssh_arguments),
                host=A(host)
            ))

