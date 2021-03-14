FROM python:3.8-slim-buster
VOLUME /result

RUN apt update && apt install -y git file gpg && pip install git+https://github.com/niess/python-appimage

ADD . /xxh
RUN mkdir -p /result

WORKDIR /xxh/appimage
RUN echo '/xxh' > requirements.txt && cat pre-requirements.txt >> requirements.txt

WORKDIR /xxh
RUN python -m python_appimage build app /xxh/appimage
CMD cp /xxh/xxh-x86_64.AppImage /result && ls -sh1 /result