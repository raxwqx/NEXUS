#!/usr/bin/env python3
"""NEXUS - Minimal TCP port scanner."""

import argparse
import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_ports(value: str) -> list[int]:
    ports: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            if start > end:
                start, end = end, start
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))

    if not ports or any(port < 1 or port > 65535 for port in ports):
        raise ValueError("Ports must be between 1 and 65535.")
    return sorted(ports)


def scan_port(target: str, port: int, timeout: float) -> tuple[int, bool]:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        return port, result == 0


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="nexus",
        description="Minimal TCP port scanner.",
    )
    parser.add_argument("target", help="Hostname or IPv4 address to scan")
    parser.add_argument(
        "-p",
        "--ports",
        default="1-1024",
        help="Ports to scan, e.g. 22,80,443 or 1-1024 (default: 1-1024)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=0.5,
        help="Socket timeout in seconds (default: 0.5)",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=100,
        help="Concurrent scan workers (default: 100)",
    )
    args = parser.parse_args()

    if args.timeout <= 0:
        parser.error("timeout must be greater than 0")
    if args.workers < 1:
        parser.error("workers must be at least 1")

    try:
        target_ip = socket.gethostbyname(args.target)
        ports = parse_ports(args.ports)
    except (socket.gaierror, ValueError) as exc:
        print(f"[!] Error: {exc}", file=sys.stderr)
        return 1

    print("NEXUS")
    print("=" * 36)
    print(f"Target : {args.target} ({target_ip})")
    print(f"Ports  : {args.ports}")
    print()

    open_ports: list[int] = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(scan_port, target_ip, port, args.timeout): port
            for port in ports
        }
        for future in as_completed(futures):
            try:
                port, is_open = future.result()
            except OSError:
                continue
            if is_open:
                open_ports.append(port)
                print(f"[OPEN]   {port}")

    open_ports.sort()
    print()
    print(f"Scan complete. {len(open_ports)} open port(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
