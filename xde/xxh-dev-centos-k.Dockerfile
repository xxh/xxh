FROM robertdebock/docker-centos-openssh
# https://github.com/robertdebock/docker-centos-openssh

RUN yum -y install glibc-locale-source glibc-langpack-en

ENTRYPOINT ["/bin/sh","-c", "mkdir -p /root/.ssh && cp /xxh/xde/keys/id_rsa.pub /root/.ssh/authorized_keys && chown root:root /root/.ssh/authorized_keys && chmod 0600 /root/.ssh/authorized_keys && /start.sh"]
