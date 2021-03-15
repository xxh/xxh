FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y openssh-client sshpass rsync wget curl git python3-pip vim mc zsh fish sudo locales
RUN python3 -m pip install --upgrade pip
RUN pip install xonsh==0.9.14 pexpect pyyaml asciinema

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8

RUN useradd -m -s $(which bash)  ubash
RUN useradd -m -s $(which xonsh) uxonsh
RUN useradd -m -s $(which zsh)   uzsh
RUN useradd -m -s $(which fish)  ufish

ADD xxh-dev-start*.sh /
RUN /xxh-dev-start.sh

ENTRYPOINT ["/xxh-dev-start-entrypoint.sh"]


