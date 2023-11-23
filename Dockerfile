FROM debian:12.2
RUN apt-get update
RUN apt-get install -y openconnect openvpn build-essential git libevent-dev make automake autoconf libtool
WORKDIR /tmp/tunsocks
ARG TUNSOCKS_REVISION=4e4ff8682053412145930b8daf2c55d357cf1e44
RUN git clone --recursive https://github.com/russdill/tunsocks && cd tunsocks && git checkout $TUNSOCKS_REVISION
RUN cd tunsocks && ./autogen.sh && ./configure --prefix=/opt && make -j4 && make install
WORKDIR /app
ADD start.py /app/start.py
CMD ["python3", "/app/start.py"]
