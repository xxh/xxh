#!/usr/bin/env xonsh

mkdir -p build
docker build . -f xxh-portable-musl-alpine.Dockerfile -t tmp/xxh-portable-musl-alpine  #--no-cache --force-rm
docker run --rm -v $PWD/build:/result tmp/xxh-portable-musl-alpine
