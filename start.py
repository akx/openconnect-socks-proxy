import logging
import os
import subprocess
import time

logger = logging.getLogger("openconnect-socks-proxy")


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s %(name)s] %(message)s",
    )
    try:
        password = os.environ["VPN_PASSWORD"]
        login = os.environ["VPN_LOGIN"]
        server = os.environ["VPN_SERVER"]
        group = os.environ["VPN_GROUP"]
    except KeyError as e:
        raise Exception(f"Environment variable {e} not found")
    totp_secret = os.environ.get("VPN_TOTP_SECRET")
    port = int(os.environ.get("SOCKS_PORT", 8080))
    tunsocks_bin = os.environ.get("TUNSOCKS_BIN", "/opt/bin/tunsocks")
    protocol = os.environ.get("VPN_PROTOCOL", "anyconnect")

    if not os.path.isfile(tunsocks_bin):
        raise Exception(f"tunsocks binary not found: {tunsocks_bin}")
    script = f"{tunsocks_bin} -D 0:{port}"
    if totp_secret:
        token_args = [
            "--token-mode=totp",
            f"--token-secret={totp_secret}",
        ]
    else:
        token_args = []
    command = [
        "openconnect",
        f"--protocol={protocol}",
        "--no-dtls",
        "--passwd-on-stdin",
        f"--authgroup={group}",
        f"--user={login}",
        "--script-tun",
        f"--script={script}",
        *token_args,
        server,
    ]
    while True:
        logger.info("Starting: %s", command)
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, encoding="utf-8")
        proc.stdin.write(password + "\n")
        proc.stdin.flush()
        ret = proc.wait()
        logger.info("Openconnect quit with code %d, restarting soon", ret)
        time.sleep(2)


if __name__ == "__main__":
    main()
