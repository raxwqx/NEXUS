#!/usr/bin/env python3
"""NEXUS - Lightweight TCP port scanner with IPv6 and JSON report support."""

from __future__ import annotations

import argparse
import json
import math
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

VERSION = "0.2.0"
DEFAULT_PORTS = "1-1024"
MAX_WORKERS = 1024
MAX_TIMEOUT = 3600.0

SERVICE_NAMES: dict[int, str] = {
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "domain",
    67: "dhcp",
    68: "dhcp",
    69: "tftp",
    80: "http",
    110: "pop3",
    123: "ntp",
    143: "imap",
    161: "snmp",
    443: "https",
    445: "microsoft-ds",
    465: "smtps",
    514: "syslog",
    587: "submission",
    993: "imaps",
    995: "pop3s",
    1194: "openvpn",
    1433: "ms-sql-s",
    1521: "oracle",
    2049: "nfs",
    3306: "mysql",
    3389: "ms-wbt-server",
    5432: "postgresql",
    5900: "vnc",
    6379: "redis",
    8080: "http-alt",
    8443: "https-alt",
    9090: "zeus-admin",
    27017: "mongodb",
}

SockAddr = tuple


def parse_ports(value: str) -> list[int]:
    """Parse comma-separated ports and ranges, validating before expansion."""
    ports: set[int] = set()
    for raw_part in value.split(","):
        part = raw_part.strip()
        if not part:
            continue
        if "-" in part:
            pieces = part.split("-")
            if len(pieces) != 2:
                raise ValueError(f"invalid port range '{part}' (expected START-END)")
            try:
                start, end = int(pieces[0]), int(pieces[1])
            except ValueError:
                raise ValueError(f"invalid port range '{part}' (expected START-END)") from None
            if not (1 <= start <= 65535 and 1 <= end <= 65535):
                raise ValueError(f"port range '{part}' must stay between 1 and 65535")
            if start > end:
                start, end = end, start
            # Validate endpoints before expanding so 1-999999 cannot exhaust memory.
            ports.update(range(start, end + 1))
        else:
            try:
                port = int(part)
            except ValueError:
                raise ValueError(f"invalid port '{part}'") from None
            if not 1 <= port <= 65535:
                raise ValueError(f"port '{part}' must be between 1 and 65535")
            ports.add(port)

    if not ports:
        raise ValueError("no ports specified")
    return sorted(ports)


def service_name(port: int) -> str:
    return SERVICE_NAMES.get(port, "")


def with_port(sockaddr: SockAddr, port: int) -> SockAddr:
    """Replace the port in an IPv4 or IPv6 sockaddr from getaddrinfo."""
    if len(sockaddr) == 2:
        return (sockaddr[0], port)
    return (sockaddr[0], port, sockaddr[2], sockaddr[3])


def resolve_target(target: str, family: int = socket.AF_UNSPEC) -> tuple[int, SockAddr]:
    """Resolve a hostname, IPv4, or IPv6 literal and return (family, sockaddr)."""
    try:
        infos = socket.getaddrinfo(target, 0, family, socket.SOCK_STREAM)
    except socket.gaierror as exc:
        detail = exc.strerror or str(exc)
        raise ValueError(f"cannot resolve '{target}': {detail}") from exc
    if not infos:
        raise ValueError(f"cannot resolve '{target}': no addresses returned")
    # Prefer IPv4 when both families are available unless the user forced IPv6.
    infos.sort(key=lambda info: 0 if info[0] == socket.AF_INET else 1)
    chosen = infos[0]
    return chosen[0], chosen[4]


def scan_port(family: int, sockaddr: SockAddr, port: int, timeout: float) -> tuple[int, bool]:
    address = with_port(sockaddr, port)
    try:
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return port, sock.connect_ex(address) == 0
    except OSError:
        return port, False


def scan_ports(
    family: int,
    sockaddr: SockAddr,
    ports: list[int],
    timeout: float,
    workers: int,
    on_open=None,
) -> list[int]:
    """Scan ports concurrently and return a sorted list of open ports."""
    open_ports: list[int] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(scan_port, family, sockaddr, port, timeout): port for port in ports
        }
        for future in as_completed(futures):
            try:
                port, is_open = future.result()
            except OSError:
                continue
            if is_open:
                open_ports.append(port)
                if on_open is not None:
                    on_open(port)
    return sorted(open_ports)


def build_report(
    target: str,
    address: str,
    family: int,
    ports: list[int],
    open_ports: list[int],
    timeout: float,
    workers: int,
    duration: float,
) -> dict:
    return {
        "tool": "NEXUS",
        "version": VERSION,
        "target": target,
        "address": address,
        "address_family": "IPv6" if family == socket.AF_INET6 else "IPv4",
        "ports_requested": len(ports),
        "timeout_seconds": timeout,
        "workers": workers,
        "open_ports": [
            {"port": port, "service": service_name(port) or None} for port in open_ports
        ],
        "open_count": len(open_ports),
        "duration_seconds": round(duration, 3),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="nexus",
        description="Lightweight TCP port scanner with IPv4 and IPv6 support.",
    )
    parser.add_argument("target", help="Hostname, IPv4, or IPv6 address to scan")
    parser.add_argument(
        "-p",
        "--ports",
        default=DEFAULT_PORTS,
        help=f"Ports to scan, e.g. 22,80,443 or 1-1024 (default: {DEFAULT_PORTS})",
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
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a machine-readable JSON report",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"nexus {VERSION}",
    )
    family_group = parser.add_mutually_exclusive_group()
    family_group.add_argument(
        "-4",
        "--ipv4",
        action="store_true",
        help="Resolve the target to IPv4 only",
    )
    family_group.add_argument(
        "-6",
        "--ipv6",
        action="store_true",
        help="Resolve the target to IPv6 only",
    )
    args = parser.parse_args(argv)

    if not math.isfinite(args.timeout) or args.timeout <= 0 or args.timeout > MAX_TIMEOUT:
        parser.error(f"timeout must be a finite number between 0 and {MAX_TIMEOUT:g} seconds")
    if not 1 <= args.workers <= MAX_WORKERS:
        parser.error(f"workers must be between 1 and {MAX_WORKERS}")

    family = socket.AF_UNSPEC
    if args.ipv4:
        family = socket.AF_INET
    elif args.ipv6:
        family = socket.AF_INET6

    try:
        ports = parse_ports(args.ports)
        family, sockaddr = resolve_target(args.target, family)
    except ValueError as exc:
        print(f"[!] Error: {exc}", file=sys.stderr)
        return 1

    address = str(sockaddr[0])
    family_label = "IPv6" if family == socket.AF_INET6 else "IPv4"

    if not args.json:
        print(f"NEXUS {VERSION}")
        print("=" * 36)
        print(f"Target : {args.target} ({address})")
        print(f"Family : {family_label}")
        print(f"Ports  : {args.ports} ({len(ports)})")
        print(f"Timeout: {args.timeout:g}s · Workers: {args.workers}")
        print()

    def report_open(port: int) -> None:
        if args.json:
            return
        service = service_name(port)
        suffix = f"  {service}" if service else ""
        print(f"[OPEN]   {port}/tcp{suffix}")

    started = time.monotonic()
    try:
        open_ports = scan_ports(
            family,
            sockaddr,
            ports,
            args.timeout,
            args.workers,
            on_open=report_open,
        )
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted.", file=sys.stderr)
        return 130
    duration = time.monotonic() - started

    if args.json:
        report = build_report(
            args.target,
            address,
            family,
            ports,
            open_ports,
            args.timeout,
            args.workers,
            duration,
        )
        print(json.dumps(report, indent=2))
        return 0

    print()
    print(f"Scan complete. {len(open_ports)} open port(s) in {duration:.2f}s.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
