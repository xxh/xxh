import os, sys, argparse, yaml, datetime, re, getpass, pexpect
from xxh_xxh import __version__
from shutil import which
from sys import exit
from argparse import RawTextHelpFormatter
from urllib.parse import urlparse
from base64 import b64encode
from signal import signal, SIGINT
from .shell import *

def sigint_handler(signal_received, frame):
    sys.exit(0)

class xxh:
    def __init__(self):
        self.package_dir_path = p(f"{__file__}").parent
        self.url_xxh_github = 'https://github.com/xxh/xxh'
        self.url_xxh_plugins_search = 'https://github.com/search?q=xxh-plugin'
        self.ssh_command = 'ssh'
        self.scp_command = 'scp'
        self.local_xxh_home = p('~/.xxh')
        self.config_file = self.get_config_filepath()
        self.host_xxh_home = '~/.xxh'
        self.shell = self.get_current_shell()
        self.short_shell_name = self.shell.split('-')[2]
        self.build_file_exts = ['xsh', 'zsh', 'fish', 'sh']
        self.url = None
        self.hostname = None
        self.ssh_arguments = []
        self.ssh_arg_v = []
        self.sshpass = []
        self.use_pexpect = True
        self.pexpect_timeout = 6
        self._password = None
        self._verbose = False
        self._vverbose = False
        self.quiet = False
        self.supported_xxh_packages = ['shell', 'plugin']
        self.supported_source_types = ['git', 'path']
        self.supported_xxh_packages_regex = '|'.join(self.supported_xxh_packages)
        self.supported_source_types_regex = '|'.join(self.supported_source_types)
        self.package_name_regex = f'xxh\-({self.supported_xxh_packages_regex})-[a-zA-Z0-9_-]+'
        self.destination_exists = False
        self.local = False

    def S(self, *args, **kwargs):
        if self.vverbose:
            eprint(f'RUN SHELL COMMAND: {args[0]}')
        return S(*args, **kwargs)

    def SC(self, *args, **kwargs):
        if self.vverbose:
            eprint(f'RUN SHELL COMMAND CAPTURED: {args[0]}')
        return SC(*args, **kwargs)

    def eprint(self, *args, **kwargs):
        if not self.quiet:
            eprint(*args, **kwargs)

    def eeprint(self, *args, **kwargs):
        eeprint(*args, **kwargs)

    def get_config_filepath(self):
        if os.environ.get('XDG_CONFIG_HOME'):
            return p(os.environ['XDG_CONFIG_HOME']) / 'xxh/config.xxhc'
        if os.environ.get('HOME'):
            return p(os.environ['HOME']) / '.config/xxh/config.xxhc'
        return p(self.local_xxh_home) / '.config/xxh/config.xxhc'

    def get_current_shell(self):
        if 'SHELL' in os.environ:
            if os.environ['SHELL'].endswith('zsh'):
                return 'xxh-shell-zsh'
            if os.environ['SHELL'].endswith('fish'):
                return 'xxh-shell-fish'
        return 'xxh-shell-xonsh'

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
            self.eprint(f'Pexpect command (timeout={self.pexpect_timeout}): '+cmd)

        sess = pexpect.spawn(cmd)
        user_host_accept = None
        user_host_password = None
        user_key_password = None
        patterns = [
            'Are you sure you want to continue connecting.*',  # 0
            "Please type 'yes' or 'no':",                      # 1
            'Enter passphrase for key.*',                      # 2
            'Password:',                                       # 3
            'password:',                                       # 4
            pexpect.EOF,                                       # 5
            '[$#~]',                                           # 6
            'Last login.*'                                     # 7
        ]
        while True:
            try:
                pattern = sess.expect(patterns, timeout=self.pexpect_timeout)
            except:
                if sess.after is pexpect.exceptions.TIMEOUT:
                    print('Probably the connection takes more time than expected.\n'
                          'Try to increase the timeout by adding "++pexpect-timeout 10" argument.')
                else:
                    print('Unknown answer from host. Check your connection to the host using ssh\n'
                          'and if it works try xxh with +vv argument.')
                if self.vverbose:
                    print('Pexpect details:')
                    print(sess)
                return {}

            if self.vverbose:
                self.eprint(f'Pexpect caught pattern: {patterns[pattern]}')

            if pattern in [0,1]:
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

            if pattern == 2:
                # Expected:
                #   Enter passphrase for key '<keyfile>':
                if key_password is None:
                    user_key_password = getpass.getpass(prompt=(sess.before + sess.after).decode("utf-8")+' ')
                    sess.sendline(user_key_password)
                else:
                    sess.sendline(key_password)

            if pattern in [3,4]:
                # Expected:
                #   <host>`s password:
                if host_password is None:
                    user_host_password = getpass.getpass(prompt=(sess.before + sess.after).decode("utf-8")+' ')
                    sess.sendline(user_host_password)
                else:
                    sess.sendline(host_password)

            if pattern == 5:
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

            if pattern in [6,7]:
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

    def get_case_sensitive_hostname(self, url):
        """
        By default urllib returns hostname in lower case. This function returns case sensitive hostname.
        :param url: urllib object
        :return: case sensitive hostname
        """
        pos_start = url.netloc.lower().find(url.hostname)
        pos_end = pos_start + len(url.hostname)
        return url.netloc[pos_start:pos_end]


    def get_host_info(self):
        if '|' in self.host_xxh_home:
            self.eeprint(f'Wrong host xxh home: {self.host_xxh_home}')

        host = self.hostname
        host_info_s = """
            xxh_home_realpath=$(dirname {host_xxh_home})/$(basename {host_xxh_home})
            xxh_version="dir_not_found"
            if [[ -d $xxh_home_realpath ]]; then
                xxh_version=$([ "$(ls -A $xxh_home_realpath)" ] && echo "version_not_found" || echo "dir_empty")
                settings_path=$xxh_home_realpath/.xxh/xxh_version
                if [[ -f $settings_path ]]; then
                    xxh_version=$(cat $settings_path)
                fi
            fi
            echo xxh_home_realpath=$xxh_home_realpath
            echo xxh_version=$xxh_version
            echo xxh_shell_exists=`[ -d $xxh_home_realpath/.xxh/shells/{shell} ] && echo "1" ||echo "0"`
            echo xxh_home_writable=`[ -w $xxh_home_realpath ] && echo "1" ||echo "0"`
            echo xxh_parent_home_writable=$([ -w $(dirname $xxh_home_realpath) ] && echo "1" ||echo "0")
            echo rsync=`command -v rsync`
            echo scp=`command -v scp`
            echo shell=`command -v {short_shell_name}`
            echo kernel=`uname -s`
            echo arch=`uname -m`
            """.format(
                host_xxh_home=self.host_xxh_home,
                shell=self.shell,
                short_shell_name=self.short_shell_name
            )

        if self.local:
            cmd = "bash -c 'echo -e \"{host_info_s}\" | bash'".format(
                host_info_s=host_info_s.strip().replace('\n', '\\n').replace('"', '\\"').replace('$', '\\$').replace(
                    '`', '\\`')
            )
            o, e, proc = self.SC(cmd)
            r = o.decode().strip()
            if not r:
                self.eeprint('Answer from localhost is empty. Try again with +v or +vv')

        elif self.use_pexpect:
            while 1:
                cmd = "bash -c 'echo -e \"{host_info_s}\" | {ssh} {ssh_v} {ssh_arguments} {host} -T \"bash -s\"'".format(
                    host_info_s=host_info_s.strip().replace('\n','\\n').replace('"','\\"').replace('$','\\$').replace('`','\\`'),
                    ssh=self.ssh_command,
                    ssh_v=('' if not self.ssh_arg_v else '-v'),
                    ssh_arguments=A(self.ssh_arguments, 0, 2),
                    host=host
                )

                pr = self.pssh(cmd)

                if 'output' in pr and 'unsupported option "accept-new"' in pr['output']:
                    if self.vverbose:
                        eprint('StrictHostKeyChecking=accept-new is not supported. Switched to StrictHostKeyChecking=yes and repeat')
                    self.ssh_arguments = [a.replace('StrictHostKeyChecking=accept-new', 'StrictHostKeyChecking=yes') for a in self.ssh_arguments]
                    continue
                break

            if pr == {}:
                self.eeprint('Answer from host is empty. Try again with +v or +vv or try ssh before xxh.')

            if self.verbose:
                self.eprint('Pexpect result:')
                self.eprint(pr)

            if 'user_host_password' in pr and pr['user_host_password'] is not None:
                self.password = pr['user_host_password']

            if 'output' not in pr:
                self.eeprint('Unexpected output. Try again with +v or +vv or try ssh before xxh.')

            r = pr['output']
        else:
            if self.verbose:
                self.eprint('Try ssh without pexpect')
            [o,e,p] = self.SC("bash -c 'echo -e \"{host_info_s}\" | {sshpass} {ssh} {ssh_v} {ssh_arguments} {host} -T \"bash -s\"'".format(
                host_info_s=host_info_s.strip().replace('\n','\\n').replace('"','\\"').replace('$','\\$').replace('`','\\`'),
                host_xxh_home=A(self.host_xxh_home),
                sshpass=A(self.sshpass),
                ssh=A(self.ssh_command),
                ssh_v=('' if not self.ssh_arg_v else '-v'),
                ssh_arguments=A(self.ssh_arguments, 0, 2),
                host=A(host)
            ))
            r = o.strip()
            r = r.decode("utf-8")

        if self.verbose:
            self.eprint(f'Host info:\n{r}')

        if r == '':
            self.eeprint('Empty answer from host when getting first info. Often this is a connection error.\n'
                    + 'Check your connection parameters using the same command but with ssh.')

        r = dict([l.split('=') for l in r.replace('\r','').split('\n') if l.strip() != '' and '=' in l and '|' not in l])
        r = {k: (v[1:-1] if v[:1] == "'" and v[-1:] == "'" else v) for k, v in r.items()}

        return r

    def prepare_env_args(self, envs, to_base64=True):
        env_args=[]
        if envs:
            for e in envs:
                el = e.split('=', 1)
                if len(el) != 2:
                    self.eeprint(f'Wrong environment (expected NAME=VAL): {e}')
                if not re.match('^[a-zA-Z0-9_]+$', el[0]):
                    self.eeprint(f'Wrong environment NAME (expected [a-zA-Z0-9-]): {el[0]}')

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

        check_dirs = [home, home / '.xxh/shells', home / '.xxh/plugins']
        for d in check_dirs:
            if not d.exists():
                self.S(f"mkdir -p {d}")

        xxh_version_file = home / '.xxh/xxh_version'
        if not xxh_version_file.exists():
            self.S(f"echo {__version__} > {xxh_version_file}")

        config_file = p(self.config_file)
        sample_config_file = self.package_dir_path / 'config.xxhc'
        if not config_file.exists() and sample_config_file.exists():
            if not self.quiet:
                eprint(f'Create sample config file in {config_file}')
            self.S(f'mkdir -p {config_file.parent} && cp {sample_config_file} {config_file}')

    def d2F0Y2ggLW4uMiB4eGggLWg(self):
        def randint(a, b):
            return a + datetime.datetime.now().microsecond % (b - a + 1)

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

    def package_parse_name(self, package_name):
        package_source_type='git'
        package_source=f'https://github.com/xxh/{package_name}'

        g = re.match(f'^({self.package_name_regex})\+({self.supported_source_types_regex})\+(.+)$', package_name)
        if g:
            package_name = g.group(1)
            package_source_type = g.group(3)
            package_source = g.group(4)
        else:
            g = re.match(f'.*//github.com/(.+?)/({self.package_name_regex})(/|$)', package_name)
            if g:
                package_source = package_name
                package_name = g.group(2)
                package_source_type = 'git'

        return (package_name, package_source_type, package_source)

    def packages_install(self, packages, kernel=None, arch=None):
        if not kernel and not arch:
            kernel = 'linux'
            arch = 'x86_64'

        arg_q = '-q' if self.quiet else ''
        installed = 0
        packages = list(set(packages))
        for package in packages:
            package_name, package_source_type, package_source = self.package_parse_name(package)

            subdir = self.package_subdir(package_name) or self.eeprint(f"Unknown package type: {package_name}")
            package_dir = self.local_xxh_home / '.xxh' / str(subdir) / package_name
            build_dir = package_dir / 'build'
            if build_dir.exists() and len(list(build_dir.glob('*'))) > 0:
                if self.vverbose or not self.destination_exists:
                    self.eprint(f'Package exists, skip install: {package_dir}')
                continue

            self.eprint(f'Install {package} to local {package_dir}')

            if not re.match(f'^{self.package_name_regex}$', package_name):
                self.eeprint(f'Invalid package name: {package_name}\n'
                             + f'  Package name format: {self.package_name_regex}\n'
                             + f'  Package name with source format: xxh-({self.supported_xxh_packages_regex})-(<package_name>)+({self.supported_source_types_regex})+(<url>|<path>)')

            if package_source_type == 'git':
                if '//github.com/' in package_source and '/tree/' in package_source:
                    github_url = package_source.split('/tree/')[0]
                    github_branch = package_source.split('/tree/')[1]
                    self.eprint(f"Git clone {github_url} from branch '{github_branch}'")
                    [o, e, proc] = self.SC(f"git clone {arg_q} --depth 1 -b '{github_branch}' {github_url} {package_dir} 1>&2")
                else:
                    self.eprint(f"Git clone {package_source}")
                    [o,e,proc] = self.SC(f'git clone {arg_q} --depth 1 {package_source} {package_dir} 1>&2')
                if proc.returncode != 0:
                    self.eeprint(f'Error:\n{o.decode().strip()}\n{e.decode().strip()}')
            elif package_source_type == 'url':
                self.eeprint(f'URL source type is not supported yet. Contribute: https://github.com/xxh/xxh')
            elif package_source_type == 'path':
                self.eprint(f"Package source path: {package_source}")
                package_source = p(package_source)
                if package_source.exists():
                    self.S(f'mkdir -p {package_dir} && cp -r {package_source}/* {package_dir}')
            else:
                self.eeprint(f'Unknown source type: {package_source_type}')

            self.eprint(f"Build {package_name}")
            build_file_found = False
            for ext in self.build_file_exts:
                build_file = package_dir / f'build.{ext}'
                if build_file.exists():
                    if not which(ext):
                        if self.vverbose:
                            self.eprint(f"Not found executor for {build_file}")
                        continue

                    kernel_arg = f"-K '{kernel}'" if kernel else ''
                    arch_arg = f"-A '{arch}'" if arch else ''

                    self.S(f'{build_file} {arg_q} {kernel_arg} {arch_arg} 1>&2')

                    build_file_found = True
                    break
            if not build_file_found:
                self.eeprint(f"Build file not found in {package_dir}")

            self.eprint(f"Installed {package_dir}")
            installed += 1
        return installed

    def packages_remove(self, packages):
        removed = 0
        packages = list(set(packages))
        for package_name in packages:
            package_name, package_source_type, package_source = self.package_parse_name(package_name)
            self.eprint(f'Remove {package_name}')
            subdir = self.package_subdir(package_name) or self.eeprint(f"Unknown package: {package_name}")
            package_dir = self.local_xxh_home / '.xxh' / subdir / package_name
            if package_dir.exists():
                self.S(f'rm -rf {package_dir}')
                self.eprint(f"Removed {package_dir}")
            removed += 1
        return removed

    def packages_reinstall(self, packages):
        self.packages_remove(packages)
        return self.packages_install(packages)

    def packages_list(self, packages=None):
        packages_dir = []
        for p in self.supported_xxh_packages:
            packages_dir += (self.local_xxh_home / '.xxh' / (p+'s')).glob('xxh-*')
        found = 0
        for p in sorted(packages_dir):
            if packages:
                if p.name in packages:
                    print(p.name)
            else:
                print(p.name)
            found += 1
        return found

    def package_subdir(self, name):
        if 'xxh-shell' in name:
            return 'shells'
        elif 'xxh-plugin' in name:
            return 'plugins'
        return None


    def main(self):
        argp = argparse.ArgumentParser(description=f"Your favorite shell wherever you go through the ssh.\n{self.d2F0Y2ggLW4uMiB4eGggLWg()}", formatter_class=RawTextHelpFormatter, prefix_chars='-+')
        argp.add_argument('--version', '-V', action='version', version=f"xxh/{__version__}")
        argp.add_argument('-p', dest='ssh_port', help="Port to connect to on the remote host.")
        argp.add_argument('-l', dest='ssh_login', help="Specifies the user to log in as on the remote machine.")
        argp.add_argument('-i', dest='ssh_private_key', help="File from which the identity (private key) for public key authentication is read.")
        argp.add_argument('-o', dest='ssh_options', metavar='SSH_OPTION -o ...', action='append', help="SSH options are described in ssh man page. Example: -o Port=22 -o User=snail")
        argp.add_argument('+c', dest='ssh_command', default=self.ssh_command, help="Command to execute instead of 'ssh'.")
        argp.add_argument('+P', '++password', help="Password for ssh auth.")
        argp.add_argument('+PP', '++password-prompt', default=False, action='store_true', help="Enter password manually using prompt.")
        argp.add_argument('destination', nargs='?', metavar='[user@]host[:port]', help="Destination may be specified as [ssh://][user@]host[:port] or host from ~/.ssh/config or 'local' to run xxh on current host.")
        argp.add_argument('+i', '++install', default=False, action='store_true', help="Install xxh to destination host without questions.")
        argp.add_argument('+if', '++install-force', default=False, action='store_true', help="Removing the host xxh package and install xxh again.")
        argp.add_argument('+iff', '++install-force-full', default=False, action='store_true', help="Removing the host xxh home and install xxh again. WARNING! All your files, configs, packages in xxh home on the host WILL BE LOST.")
        argp.add_argument('+xc', '++xxh-config', default=self.config_file, help=f"Xxh config file in yaml. Default: {self.config_file}")
        argp.add_argument('+e', '++env', dest='env', metavar='NAME=VAL +e ...', action='append', help="Setting environment variables if supported by shell entrypoint.")
        argp.add_argument('+eb', '++envb', dest='envb', metavar='NAME=BASE64 +eb ...', action='append', help="Setting environment variables base64 encoded if supported by shell entrypoint.")
        argp.add_argument('+lh', '++local-xxh-home', default=self.local_xxh_home, help=f"Local xxh home path. Default: {self.local_xxh_home}")
        argp.add_argument('+hh', '++host-xxh-home', default=self.host_xxh_home, help=f"Host xxh home path. Default: {self.host_xxh_home}")
        argp.add_argument('+hhr', '++host-xxh-home-remove', action='store_true', help=f"Remove xxh home on host after disconnect.")
        argp.add_argument('+hhh', '++host-home', help=f"Default HOME path on host. Could be '~' for default user home. Default: {self.host_xxh_home}")
        argp.add_argument('+hhx', '++host-home-xdg', help=f"Default XDG path on host. Could be '~' for default user home. Default: {self.host_xxh_home}")
        argp.add_argument('+hf', '++host-execute-file', help=f"Execute script file placed on host and exit. If supported by shell entrypoint.")
        argp.add_argument('+hc', '++host-execute-command', help=f"Execute command on host and exit. If supported by shell entrypoint.")
        argp.add_argument('+heb', '++host-execute-bash', dest='host_execute_bash', metavar='BASE64 +heb ...', action='append', help="Bash command will be executed before shell entrypoint (base64 encoded) if supported by shell entrypoint.")
        argp.add_argument('+s', '++shell', default=self.shell, help="xxh shell")
        argp.add_argument('+v', '++verbose', default=False, action='store_true', help="Verbose mode.")
        argp.add_argument('+vv', '++vverbose', default=False, action='store_true', help="Super verbose mode.")
        argp.add_argument('+q', '++quiet', default=False, action='store_true', help="Quiet mode.")
        argp.add_argument('+I', '++install-xxh-packages', action='append', metavar='xxh-package', dest='install_xxh_packages', help="Local install xxh packages.")
        argp.add_argument('+L', '++list-xxh-packages', nargs='*', metavar='xxh-package', dest='list_xxh_packages', help="List local xxh packages.")
        argp.add_argument('+RI', '++reinstall-xxh-packages', action='append', metavar='xxh-package', dest='reinstall_xxh_packages', help="Local reinstall xxh packages.")
        argp.add_argument('+R', '++remove-xxh-packages', action='append', metavar='xxh-package', dest='remove_xxh_packages', help="Local remove xxh packages.")
        argp.add_argument('+ES', '++extract-sourcing-files', action='store_true', dest='extract_sourcing_files', help="Used for AppImage. Extract seamless mode files.")
        argp.add_argument('++pexpect-timeout', default=self.pexpect_timeout, help=f"Set timeout for pexpect in seconds. Default: {self.pexpect_timeout}")
        argp.add_argument('++copy-method', default=None, help="Copy method: scp or rsync. Default is autodetect and prefer rsync.")
        argp.add_argument('++scp-command', default=self.scp_command, help="Command to execute instead of 'scp'.")
        argp.add_argument('++pexpect-disable', default=False, action='store_true', help="Disable pexpect.")
        argp.usage = "xxh <host from ~/.ssh/config>\n" \
            + "usage: xxh [ssh arguments] [user@]host[:port] [xxh arguments]\n" \
            + "usage: xxh local [xxh arguments]\n" \
            + "usage: xxh [-p SSH_PORT] [-l SSH_LOGIN] [-i SSH_PRIVATE_KEY]\n" \
            + "           [-o SSH_OPTION -o ...] [+c SSH_COMMAND] [+P PASSWORD] [+PP]\n" \
            + "           [user@]host[:port]\n" \
            + "           [+i] [+if] [+iff] [+hhr] [+s SHELL] [+e NAME=VAL +e ...] [+v] [+vv] [+q]\n" \
            + "           [+hh HOST_XXH_HOME] [+hhh HOST_HOME] [+hf HOST_EXEC_FILE] [+hc HOST_EXEC_CMD]\n" \
            + "           [+xc CONFIG_FILE] [+lh LOCAL_XXH_HOME] [-h] [-V]\n" \
            + "usage: xxh [+I xxh-package +I ...] [+L] [+RI xxh-package +RI ...] [+R xxh-package +R ...]\n"

        help = argp.format_help().replace('\n  +','\n\nxxh arguments:\n  +',1).replace('optional ', 'common ')\
            .replace('number and exit', 'number and exit\n\nssh arguments:').replace('positional ', 'required ') \
            .replace('Quiet mode.', 'Quiet mode.\n\nxxh packages:').replace('remove xxh packages.', 'remove xxh packages.\n\nxxh special:')
        argp.format_help = lambda: help
        opt = argp.parse_args()

        if opt.extract_sourcing_files:
            cdir = p(sys.argv[0]).absolute().parent
            self.S(f'cp {self.package_dir_path}/xxh.*sh {cdir}')
            print(f'Sourcing files extracted to {cdir}')
            exit(0)

        self.pexpect_timeout = int(opt.pexpect_timeout)
        self.local_xxh_home = p(opt.local_xxh_home).absolute()
        self.host_xxh_home = opt.host_xxh_home
        self.use_pexpect = not opt.pexpect_disable

        if opt.destination == 'local':
            self.local = True

            if self.local_xxh_home == p(self.host_xxh_home).absolute():
                self.local_xxh_home = self.local_xxh_home / '.xxh_local'

        opt.xxh_config = p(opt.xxh_config)
        if self.config_file != opt.xxh_config:
            if not opt.xxh_config.exists():
                self.eeprint(f'Config not found in {opt.xxh_config}')
            else:
                self.config_file = opt.xxh_config

        self.quiet = opt.quiet
        arg_q = ['-q'] if self.quiet else []
        if not self.quiet:
            self.verbose = opt.verbose
            self.vverbose = opt.vverbose

        if not self.verbose:
            signal(SIGINT, sigint_handler)

        if not opt.destination:
            opt.destination = '`'
            self.destination_exists = False
        else:
            self.destination_exists = True

        self.url = url = self.parse_destination(opt.destination)
        self.hostname = self.get_case_sensitive_hostname(url)

        if self.destination_exists and self.config_file and self.config_file.exists():
            if self.verbose:
                self.eprint(f'Load xxh config from {self.config_file}')
            with open(self.config_file) as f:
                xxh_config = yaml.safe_load(f)

            if xxh_config and 'hosts' in xxh_config:
                sys_args = sys.argv[1:]
                conf_args = []
                for h, hc in xxh_config['hosts'].items():
                    if re.match(h, self.hostname):
                        if self.verbose:
                            self.eprint('Load xxh config for host ' + h)
                        if hc and len(hc) > 0:
                            for k, v in hc.items():
                                if type(v) == list:
                                    for vv in v:
                                        if vv:
                                            conf_args += [k, vv]
                                else:
                                    conf_args += [k, v] if v is not None else [k]

                                if k in ['+P', '++password']:
                                    current_user = getpass.getuser()
                                    current_mode = oct(self.config_file.stat().st_mode)[-4:]
                                    if self.config_file.owner() != current_user or current_mode != '0600':
                                        self.eprint('\n\033[0;93mWARN! There is password in the config file but the file is too open!\n'
                                               + f'Run to restrict: chown {current_user}:{current_user} {self.config_file} && chmod 0600 {self.config_file}\033[0m\n')
                args = conf_args + sys_args
                if self.verbose:
                    print('Final arguments list: ' + str(args))
                opt = argp.parse_args(args)

        self.verbose = opt.verbose
        self.vverbose = opt.vverbose
        self.use_pexpect = not opt.pexpect_disable

        self.quiet = opt.quiet
        arg_q = ['-q'] if self.quiet else []
        self.verbose = opt.verbose if not self.quiet else False
        self.vverbose = opt.vverbose if not self.quiet else False

        def packages_operations():
            if opt.install_xxh_packages:
                installed = self.packages_install(opt.install_xxh_packages)
            if opt.reinstall_xxh_packages:
                reinstalled = self.packages_reinstall(opt.reinstall_xxh_packages)
            if opt.remove_xxh_packages:
                removed = self.packages_remove(opt.remove_xxh_packages)

        packages_opration = opt.install_xxh_packages \
                            or opt.reinstall_xxh_packages \
                            or opt.remove_xxh_packages \
                            or opt.list_xxh_packages \
                            or opt.list_xxh_packages == []

        if not self.local:
            packages_operations()

        if packages_opration or self.destination_exists:
            self.create_xxh_env()

        if opt.list_xxh_packages or opt.list_xxh_packages == []:
            found = self.packages_list(opt.list_xxh_packages)

        if not self.destination_exists:
            if packages_opration:
                exit(0)
            else:
                self.eeprint(argp.format_usage()+'\nThe following arguments are required: [user@]host[:port]')

        self.shell = opt.shell if opt.shell.startswith('xxh-shell-') else 'xxh-shell-'+opt.shell

        if self.shell.startswith('xxh-shell-'):
            self.short_shell_name = self.shell.split('-')[2]
        else:
            self.short_shell_name = self.shell

        username = getpass.getuser()
        host = self.hostname
        if not host:
            self.eeprint(f"Wrong destination '{host}'")
        if url.port:
            opt.ssh_port = url.port
        if url.username:
            opt.ssh_login = url.username
        if opt.ssh_login:
            username = opt.ssh_login

        self.ssh_command = opt.ssh_command
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

        if opt.scp_command:
            self.scp_command = opt.scp_command

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

        self.host_xxh_home = opt.host_xxh_home

        if self.local_xxh_home.exists():
            if not os.access(self.local_xxh_home, os.W_OK):
                self.eeprint(f"The local xxh home path isn't writable: {self.local_xxh_home}" )
        elif local_xxh_home_parent.exists():
            if not os.access(local_xxh_home_parent, os.W_OK):
                self.eeprint(f"Parent for local xxh home path isn't writable: {local_xxh_home_parent}")
        else:
            self.eeprint(f"Paths aren't writable:\n  {local_xxh_home_parent}\n  {self.local_xxh_home}")

        local_plugins_dir = self.local_xxh_home / '.xxh/plugins'
        self.S("mkdir {ssh_arg_v} -p {local_xxh_home} {local_plugins_dir} {shells_dir}".format(
            ssh_arg_v=A(self.ssh_arg_v),
            local_xxh_home=self.local_xxh_home,
            local_plugins_dir=local_plugins_dir,
            shells_dir=(self.local_xxh_home / '.xxh/shells')
        ))

        if p(self.host_xxh_home).resolve() == p('/'):
            self.eeprint("Host xxh home path {host_xxh_home} looks like /. Please check twice!")

        host_info = self.get_host_info()

        if not host_info:
            self.eeprint(f'Unknown answer from host when getting info. Try to get more info with +v or +vv arguments.')

        if 'xxh_home_realpath' not in host_info or host_info['xxh_home_realpath'] == '':
            self.eeprint(f'Unknown answer from host when getting realpath for directory {self.host_xxh_home}. Try to get more info with +v or +vv arguments.')

        if 'xxh_version' not in host_info or host_info['xxh_version'] == '':
            self.eeprint(f'Unknown answer from host when getting version for directory {self.host_xxh_home}. Try to get more info with +v or +vv arguments.')

        host_xxh_home = host_info['xxh_home_realpath']
        host_xxh_home = p(f"{host_xxh_home}")
        host_xxh_version = host_info['xxh_version']

        if self.local and host_xxh_version in ['dir_not_found', 'dir_empty', 'version_not_found'] and not opt.quiet and not opt.install_force and not opt.install_force_full:
            self.eprint('The `xxh local` feature is experimental and will be more portable in the next releases.')
            if not which('git'):
                self.eeprint("Git not found on the host. At this time we haven't portable versions of git.")
            yn = input("At this time we haven't portable versions of all tools to build your xxh packages.\n"
                       "The tools from this host will be used.\n"
                       "But there is no guarantee that xxh package you use will not required another missing tools and fails while building.\n"
                       "Continue? [Y/n]").strip().lower()
            if yn == 'n':
                self.eeprint('Stopped')

        if host_info['xxh_home_writable'] == '0' and host_info['xxh_parent_home_writable'] == '0':
            yn = input(f"{host}:{host_xxh_home} is not writable. Continue? [y/n] ").strip().lower()
            if yn != 'y':
                self.eeprint('Stopped')

        if not self.local and host_info['scp'] == '' and host_info['rsync'] == '':
            self.eeprint(f"There are no rsync or scp on target host. Sad but files can't be uploaded.")

        if self.local:
            ssh_pipe_command = 'bash'
        else:
            ssh_pipe_command = '{sshpass} {ssh} {ssh_arg_v} {ssh_arguments} {host} -T "bash -s"'.format(
                sshpass=A(self.sshpass),
                ssh=A(self.ssh_command),
                ssh_arg_v=A(self.ssh_arg_v),
                ssh_arguments=A(self.ssh_arguments, 0, 2),
                host=A(host)
            )

        if opt.install_force is False and opt.install_force_full is False:

            # Check version

            ask = False
            if host_xxh_version not in ['dir_not_found', 'dir_empty', 'version_not_found'] and host_xxh_version != __version__:
                ask = f"Local xxh version '{__version__}' is not equal host xxh version '{host_xxh_version}'."

            if ask:
                choice = input(f"{ask} What's next? \n"
                               + " s   Stop here. You'll try to connect using ordinary ssh for backup current xxh home.\n"
                               + " u   Safe update. Host xxh home will be renamed and new xxh version will be installed.\n"
                               + " f   DEFAULT: Force reinstall xxh. All your files in xxh home on the host will be saved.\n"
                               + " FF  Force full reinstall. WARNING! All your files in xxh home on the host WILL BE LOST.\n"
                               + " i   Ignore, cross fingers and continue the connection.\n"
                               + "s/u/(f)/FF/i? ")

                if choice == 's':
                    print('Stopped')
                    exit(0)
                elif choice == 'u':
                    local_time = datetime.datetime.now().isoformat()[:19]
                    self.eprint(f"Move {host}:{host_xxh_home} to {host}:{host_xxh_home}-{local_time}")
                    if self.local:
                        self.S('echo "mv {host_xxh_home} {host_xxh_home}-{local_time}" | bash'.format(
                            host_xxh_home=A(host_xxh_home),
                            local_time=A(local_time)
                        ))
                    else:
                        self.S('echo "mv {host_xxh_home} {host_xxh_home}-{local_time}" | {ssh_pipe_command}'.format(
                            host_xxh_home=A(host_xxh_home),
                            local_time=A(local_time),
                            ssh_pipe_command=ssh_pipe_command
                        ))
                    opt.install = True
                elif choice == 'f' or choice.strip() == '':
                    opt.install = True
                    opt.install_force = True
                elif choice == 'FF':
                    opt.install = True
                    opt.install_force_full = True
                elif choice == 'i':
                    pass
                else:
                    self.eeprint('Unknown answer')

        if (host_xxh_version in ['dir_not_found', 'dir_empty'] or host_info['xxh_shell_exists'] == '0') and opt.install is False and opt.install_force is False and opt.install_force_full is False and not self.quiet:
            yn = input(f"{host}:{host_xxh_home}/.xxh/shells/{self.shell} not found. Install {self.shell}? [Y/n] ").strip().lower()
            if yn == 'y' or yn == '':
                opt.install = True
            else:
                self.eeprint('Unknown answer')

        if opt.install is True and opt.install_force is False and opt.install_force_full is False and host_xxh_version not in ['dir_not_found', 'dir_empty'] and host_info['xxh_shell_exists'] == '1':
            opt.install = False

        if opt.install:
            self.eprint(f"Install {self.shell} to {host}:{host_xxh_home}" )

            # Remove xxh home directories
            if opt.install_force_full:
                self.eprint(f'Remove {host}:{host_xxh_home}')
                if self.local:
                    self.S('echo "rm -rf {host_xxh_home}" | bash'.format(
                        host_xxh_home=host_xxh_home
                    ))
                else:
                    self.S('echo "rm -rf {host_xxh_home}" | {ssh_pipe_command}'.format(
                        host_xxh_home=host_xxh_home,
                        ssh_pipe_command=ssh_pipe_command
                    ))

            elif opt.install_force:
                self.eprint(f'Remove {host}:{host_xxh_home}/.xxh')
                if self.local:
                    self.S('echo "rm -rf {host_xxh_home}/.xxh" | bash'.format(
                        host_xxh_home=host_xxh_home
                    ))
                else:
                    self.S('echo "rm -rf {host_xxh_home}/.xxh" | {ssh_pipe_command}'.format(
                        host_xxh_home=host_xxh_home,
                        ssh_pipe_command=ssh_pipe_command
                    ))

            # Build xxh packages
            if self.local:
                packages_operations()
            build_any_plugins = [p.name for p in (self.local_xxh_home / '.xxh/plugins').glob(f'xxh-plugin-prerun-*') ]
            build_shell_plugins = [p.name for p in (self.local_xxh_home / '.xxh/plugins').glob(f'xxh-plugin-{self.short_shell_name}-*') ]
            self.packages_install([self.shell] + build_any_plugins + build_shell_plugins)

            # Create host xxh home directories

            host_xxh_plugins_dir = host_xxh_home / '.xxh/plugins'
            host_xxh_dirs_str = ''
            for local_plugin_dir in list(local_plugins_dir.glob(f'xxh-plugin-prerun-*')) + list(local_plugins_dir.glob(f'xxh-plugin-{self.short_shell_name}-*')):
                local_plugin_build_dir = local_plugin_dir / 'build'
                host_plugin_build_dir = str(local_plugin_build_dir).replace(str(self.local_xxh_home), str(host_xxh_home))
                host_xxh_dirs_str += ' ' + host_plugin_build_dir

            host_xdg_config_dir = host_xxh_home / '.config'
            host_xxh_shell_dir = host_xxh_home / f'.xxh/shells/{self.shell}'
            host_xxh_shell_build_dir = host_xxh_shell_dir  / 'build'

            self.S('echo "mkdir -p {host_xdg_config_dir} {host_xxh_shell_build_dir} {host_xxh_dirs_str}" | {ssh_pipe_command}'.format(
                host_xdg_config_dir=host_xdg_config_dir,
                host_xxh_shell_build_dir=host_xxh_shell_build_dir,
                host_xxh_dirs_str=host_xxh_dirs_str,
                host_xxh_home=host_xxh_home,
                ssh_pipe_command=ssh_pipe_command
            ))

            self.S('echo "echo {xxh_version} > {host_xxh_home}/.xxh/xxh_version" | {ssh_pipe_command}'.format(
                host_xxh_home=host_xxh_home,
                xxh_version=__version__,
                ssh_pipe_command=ssh_pipe_command
            ))

            # Upload files
            bash_wrap_begin = "bash -c 'shopt -s dotglob && "
            bash_wrap_end = "'"

            shell_build_dir = self.local_xxh_home / '.xxh/shells' / self.shell / 'build'

            copy_method = None
            if opt.copy_method:
                copy_method = opt.copy_method
            if self.local:
                copy_method = 'cp'

            if copy_method == 'rsync' or (copy_method is None and which('rsync') and host_info['rsync']):
                self.eprint('First time upload using rsync (this will be omitted on the next connections)')

                rsync = "rsync {ssh_arg_v} -e \"{sshpass} {ssh} {ssh_arg_v} {ssh_arguments}\" {arg_q} -az {progress} --cvs-exclude --include core ".format(
                    host_xxh_home=host_xxh_home,
                    sshpass=A(self.sshpass),
                    ssh=A(self.ssh_command),
                    ssh_arg_v=('' if self.ssh_arg_v == [] else '-v'),
                    ssh_arguments=A(self.ssh_arguments, 0, 3),
                    arg_q=A(arg_q),
                    progress=('' if self.quiet or not self.verbose else '--progress')
                )

                self.S("{bb}{rsync} {shell_build_dir}/ {host}:{host_xxh_shell_build_dir}/ 1>&2{be}".format(
                    bb=bash_wrap_begin,
                    be=bash_wrap_end,
                    rsync=rsync,
                    host=A(host),
                    shell_build_dir=shell_build_dir,
                    host_xxh_shell_build_dir=host_xxh_shell_build_dir
                ))
                for local_plugin_dir in list(local_plugins_dir.glob(f'xxh-plugin-prerun-*')) + list(local_plugins_dir.glob(f'xxh-plugin-{self.short_shell_name}-*')):
                    local_plugin_build_dir = local_plugin_dir/'build'
                    local_plugin_name = local_plugin_dir.name
                    self.S("{bb}{rsync} {local_plugin_build_dir}/* {host}:{host_xxh_plugins_dir}/{local_plugin_name}/build/ 1>&2{be}".format(
                        bb=bash_wrap_begin,
                        be=bash_wrap_end,
                        rsync=rsync,
                        host=A(host),
                        local_plugin_build_dir=local_plugin_build_dir,
                        host_xxh_plugins_dir=host_xxh_plugins_dir,
                        local_plugin_name=local_plugin_name
                    ))
            elif copy_method == 'scp' or (copy_method is None and which('scp') and host_info['scp']):
                self.eprint("First time upload using scp (this will be omitted on the next connections).\nNote: you can install rsync on local and remote host to increase speed.")
                scp = "{sshpass} {scp_command} {ssh_arg_v} {ssh_arguments} -r -C {arg_q}".format(
                    sshpass=A(self.sshpass),
                    scp_command=A(self.scp_command),
                    ssh_arg_v=A(self.ssh_arg_v),
                    ssh_arguments=A(self.ssh_arguments, 0, 1),
                    arg_q=A(arg_q)
                )

                self.S('{bb}{scp} {shell_build_dir} {host}:{host_xxh_shell_dir}/ 1>&2{be}'.format(
                    bb=bash_wrap_begin,
                    be=bash_wrap_end,
                    scp=scp,
                    shell_build_dir=shell_build_dir,
                    host=host,
                    host_xxh_shell_dir=host_xxh_shell_dir
                ))

                for local_plugin_dir in list(local_plugins_dir.glob(f'xxh-plugin-prerun-*')) + list(local_plugins_dir.glob(f'xxh-plugin-{self.short_shell_name}-*')):
                    local_plugin_build_dir = local_plugin_dir/'build'
                    local_plugin_name = local_plugin_dir.name
                    self.S('{bb}{scp} {local_plugin_build_dir}/* {host}:{host_xxh_plugins_dir}/{local_plugin_name}/build/ 1>&2{be}'.format(
                        bb=bash_wrap_begin,
                        be=bash_wrap_end,
                        scp=scp,
                        local_plugin_build_dir=local_plugin_build_dir,
                        host=host,
                        host_xxh_plugins_dir=host_xxh_plugins_dir,
                        local_plugin_name=local_plugin_name
                    ))
            elif copy_method == 'cp':
                self.eprint('First time copying using cp (this will be omitted on the next time)')

                self.S('{bb}cp -r {shell_build_dir} {host_xxh_shell_dir}/ 1>&2{be}'.format(
                    bb=bash_wrap_begin,
                    be=bash_wrap_end,
                    shell_build_dir=shell_build_dir,
                    host_xxh_shell_dir=host_xxh_shell_dir
                ))

                for local_plugin_dir in list(local_plugins_dir.glob(f'xxh-plugin-prerun-*')) + list(local_plugins_dir.glob(f'xxh-plugin-{self.short_shell_name}-*')):
                    local_plugin_build_dir = local_plugin_dir/'build'
                    local_plugin_name = local_plugin_dir.name
                    self.S('{bb}cp -r {local_plugin_build_dir}/* {host_xxh_plugins_dir}/{local_plugin_name}/build/ 1>&2{be}'.format(
                        bb=bash_wrap_begin,
                        be=bash_wrap_end,
                        local_plugin_build_dir=local_plugin_build_dir,
                        host_xxh_plugins_dir=host_xxh_plugins_dir,
                        local_plugin_name=local_plugin_name
                    ))
            elif copy_method == 'skip':
                if self.verbose:
                    self.eprint('Skip copying')
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

        host_home = []
        if opt.host_home:
            host_home = f'-H {opt.host_home}'

        host_home_xdg = []
        if opt.host_home_xdg:
            host_home_xdg = f'-X {opt.host_home_xdg}'

        entrypoint_command = "{entrypoint} {host_execute_file} {host_execute_command} {host_entrypoint_verbose} {env_args} {host_home} {host_home_xdg}".format(
            entrypoint=A(str(host_xxh_home/'.xxh/shells'/self.shell/'build/entrypoint.sh')),
            host_execute_file=A(host_execute_file),
            host_execute_command=A(host_execute_command),
            host_entrypoint_verbose=A(host_entrypoint_verbose),
            env_args=A(env_args),
            host_home=A(host_home),
            host_home_xdg=A(host_home_xdg)
        )

        if self.local:
            self.S("bash -i {entrypoint_command}".format(entrypoint_command=entrypoint_command))
        else:
            lcs = []
            for lc in ['LC_TIME', 'LC_MONETARY', 'LC_ADDRESS', 'LC_IDENTIFICATION', 'LC_MEASUREMENT', 'LC_NAME', 'LC_NUMERIC', 'LC_PAPER','LC_TELEPHONE']:
                lcs.append(f"{lc}=POSIX")

            self.S("{lcs} {sshpass} {ssh} {ssh_arg_v} {ssh_arguments} {host} -t '{entrypoint_command}'".format(
                lcs=A(lcs),
                sshpass=A(self.sshpass),
                ssh=A(self.ssh_command),
                ssh_arg_v=A(self.ssh_arg_v),
                ssh_arguments=A(self.ssh_arguments, 0, 1),
                host=A(host),
                entrypoint_command=entrypoint_command
            ))

        if opt.host_xxh_home_remove:
            if self.verbose:
                self.eprint(f'Remove {host}:{host_xxh_home}')

            if self.local:
                self.S('echo "rm -rf {host_xxh_home}" | bash'.format(
                    host_xxh_home=host_xxh_home
                ))
            else:
                self.S('echo "rm -rf {host_xxh_home}" | {ssh_pipe_command}'.format(
                    host_xxh_home=host_xxh_home,
                    ssh_pipe_command=ssh_pipe_command
                ))

