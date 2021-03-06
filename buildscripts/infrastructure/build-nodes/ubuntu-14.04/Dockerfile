FROM ubuntu:14.04

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
    apache2 \
    apache2-threaded-dev \
    build-essential \
    dietlibc-dev \
    dnsutils \
    dpatch \
    flex \
    gettext \
    git-buildpackage \
    libboost-all-dev \
    libcurl4-openssl-dev \
    libevent-dev \
    libffi-dev \
    libgd2-xpm-dev \
    libglib2.0-dev \
    libgnutls-dev \
    libgsf-1-dev \
    libldap2-dev \
    libltdl-dev \
    libmcrypt-dev \
    libmysqlclient15-dev \
    libncurses5-dev \
    libpango1.0-dev \
    libpcap-dev \
    libperl-dev \
    libpq-dev \
    libradiusclient-ng-dev \
    libreadline-dev \
    libsqlite3-dev \
    libssl-dev \
    libxml2-dev \
    openssh-client \
    patch \
    rpcbind \
    smbclient \
    texinfo \
    tk-dev \
    uuid-dev \
    && rm -rf /var/lib/apt/lists/*

ARG ARTIFACT_STORAGE
COPY bw-build-gnu-toolchain.sh /usr/sbin
RUN bw-build-gnu-toolchain.sh -r $ARTIFACT_STORAGE -b
RUN cd /opt \
    && wget https://github.com/Kitware/CMake/releases/download/v3.16.2/cmake-3.16.2-Linux-x86_64.tar.gz \
    && tar xf cmake-3.16.2-Linux-x86_64.tar.gz \
    && ln -s /opt/cmake-3.16.2-Linux-x86_64/bin/* /usr/bin/

RUN apt-get update \
    && apt-get install -y \
    chrpath \
    joe \
    iputils-ping \
    vim \
    && rm -rf /var/lib/apt/lists/*

ARG VERS_TAG
RUN echo $VERS_TAG > /version.txt
