FROM xxh/xxh-dev-ubuntu-k
# https://github.com/rastasheep/ubuntu-sshd

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y fuse rsync

