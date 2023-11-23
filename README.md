# openconnect-socks-proxy

Dockerfile + Python start script to configure an [openconnect] + [tunsocks] SOCKS proxy.

Lets you connect to VPN'd networks without having to install anything on your host machine,
or having to configure your host machine's network settings.

## Build docker image

```
docker build . -t osp
```

## Run docker image

Example `.env`:

```
VPN_SERVER=my-vpn-server.example.com
VPN_LOGIN=my-username
VPN_GROUP=my-group
VPN_PASSWORD=my-password
VPN_TOTP_SECRET=... (optional)
```

```
docker run -it -p 8080:8080 --env-file=.env osp
```

## Use proxy

```
curl --verbose --socks4a 127.0.0.1:8080 "https://something-that-requires-vpn.com"
```

Use [`--socks4a`](https://en.wikipedia.org/wiki/SOCKS#SOCKS4a) to have DNS lookups also occur via the VPN.

[openconnect]: https://www.infradead.org/openconnect/
[tunsocks]: https://github.com/russdill/tunsocks
