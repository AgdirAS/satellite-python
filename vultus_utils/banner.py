import os
import sys


def print_banner(service_name: str) -> None:
    port = os.environ.get("PORT", "8080")
    seq_url = os.environ.get("SEQ_URL", "http://seq:5341")
    log_level = "DEBUG"
    width = 48

    lines = [
        f"  Service    : {service_name}",
        f"  Listening  : 0.0.0.0:{port}",
        f"  Log level  : {log_level}",
        f"  Seq logs   : {seq_url}",
    ]

    border = "═" * width
    print(f"\n╔{border}╗", flush=True)
    for line in lines:
        padded = line.ljust(width)
        print(f"║{padded}║", flush=True)
    print(f"╚{border}╝\n", flush=True)
