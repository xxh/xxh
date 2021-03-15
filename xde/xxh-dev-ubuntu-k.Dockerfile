FROM rastasheep/ubuntu-sshd:18.04
# https://github.com/rastasheep/ubuntu-sshd

ENV DEBIAN_FRONTEND=noninteractive
RUN  apt update && apt install -y vim mc locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

ENTRYPOINT ["/bin/sh","-c", "cp /xxh/xde/keys/id_rsa.pub /root/.ssh/authorized_keys && chown root:root /root/.ssh/authorized_keys && chmod 0600 /root/.ssh/authorized_keys && /usr/sbin/sshd -D"]




