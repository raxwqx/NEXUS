# 🕷️ NEXUS

**Lightweight TCP port scanner built for fast network discovery & authorized security research.**

NEXUS is a small, dependency-free TCP port scanner written in Python. It checks hostnames, IPv4 addresses, and IPv6 addresses with concurrent workers and can produce a **machine-readable JSON report** or a compact terminal summary with service labels.

<p>
  <img src="https://img.shields.io/badge/version-0.2.0-9cffb5?style=for-the-badge&labelColor=101713" alt="Version 0.2.0" />
  <img src="https://img.shields.io/badge/Python-3.11%2B-9bdcff?style=for-the-badge&logo=python&logoColor=white&labelColor=101713" alt="Python 3.11 or newer" />
  <img src="https://img.shields.io/badge/License-MIT-f3d58a?style=for-the-badge&labelColor=101713" alt="MIT License" />
</p>

[English](README.md) · [Türkçe](README.tr.md)

---

## ✨ Features

- 🔎 Concurrent TCP port scanning
- 🌐 Hostname, IPv4, and **IPv6** targets
- 🧾 **JSON reports** with `--json`
- 🏷️ Common service labels for open ports (ssh, http, https, …)
- 🎯 Custom port lists and ranges
- 🧱 Safe port parsing with clear validation errors
- ⏱️ Configurable, bounded socket timeout
- ⚡ Configurable worker count (1–1024)
- 🛑 Graceful Ctrl+C handling (exit code 130)
- 📦 Zero third-party runtime dependencies
- 🐍 Written entirely in Python
- 💻 Works directly from the command line

---

## 📥 Installation

### Clone the repository

```bash
git clone https://github.com/raxwqx/NEXUS.git
cd NEXUS
```

NEXUS has no runtime dependencies outside the Python standard library.

Make sure Python 3.11 or newer is installed:

```bash
python3 --version
```

### Run NEXUS

```bash
python3 nexus.py --help
```

Optionally install it as a command:

```bash
python3 -m pip install -e '.[dev]'
nexus --version
```

---

## 🚀 Usage

### Basic scan

Scan the default port range (`1-1024`):

```bash
python3 nexus.py 127.0.0.1
```

Example output:

```text
NEXUS 0.2.0
====================================
Target : 127.0.0.1 (127.0.0.1)
Family : IPv4
Ports  : 1-1024 (1024)
Timeout: 0.5s · Workers: 100

[OPEN]   22/tcp  ssh
[OPEN]   80/tcp  http
[OPEN]   443/tcp  https

Scan complete. 3 open port(s) in 0.04s.
```

### JSON report

```bash
python3 nexus.py 127.0.0.1 -p 22,80,443 --json
```

```json
{
  "tool": "NEXUS",
  "version": "0.2.0",
  "target": "127.0.0.1",
  "address": "127.0.0.1",
  "address_family": "IPv4",
  "ports_requested": 3,
  "timeout_seconds": 0.5,
  "workers": 100,
  "open_ports": [
    {"port": 22, "service": "ssh"},
    {"port": 443, "service": "https"}
  ],
  "open_count": 2,
  "duration_seconds": 0.012
}
```

### Selected ports and ranges

```bash
python3 nexus.py 127.0.0.1 -p 22,80,443
python3 nexus.py 127.0.0.1 -p 1-1024
python3 nexus.py 127.0.0.1 -p 8000-8100,443
```

Reversed ranges such as `8100-8000` are normalized automatically.

### IPv6 and address families

```bash
python3 nexus.py ::1 -p 22,80,443
python3 nexus.py example.com -6 -p 443
python3 nexus.py example.com -4 -p 443
```

`-4` forces IPv4, `-6` forces IPv6, and the default prefers IPv4 when a hostname offers both.

### Timeout and workers

```bash
python3 nexus.py 127.0.0.1 -t 1
python3 nexus.py 127.0.0.1 -w 50
```

Timeouts must be finite numbers up to 3600 seconds; workers must be between 1 and 1024.

### Combine options

```bash
python3 nexus.py 192.168.1.1 -p 1-1024 -t 0.5 -w 100
```

---

## ⚙️ Command-line options

```text
usage: nexus [-h] [-p PORTS] [-t TIMEOUT] [-w WORKERS] [--json] [--version]
             [-4 | -6]
             target

Lightweight TCP port scanner with IPv4 and IPv6 support.

positional arguments:
  target                Hostname, IPv4, or IPv6 address to scan

options:
  -h, --help            show this help message and exit
  -p, --ports PORTS     Ports to scan, e.g. 22,80,443 or 1-1024 (default: 1-1024)
  -t, --timeout TIMEOUT
                        Socket timeout in seconds (default: 0.5)
  -w, --workers WORKERS
                        Concurrent scan workers (default: 100)
  --json                Print a machine-readable JSON report
  --version             show program's version number and exit
  -4, --ipv4            Resolve the target to IPv4 only
  -6, --ipv6            Resolve the target to IPv6 only
```

Valid port ranges are `1–65535`. Ranges are validated before expansion, so an invalid range fails immediately instead of consuming memory.

---

## 🧪 Examples

Scan a local system:

```bash
python3 nexus.py 127.0.0.1
```

Scan a hostname:

```bash
python3 nexus.py example.com
```

Scan common ports:

```bash
python3 nexus.py example.com -p 22,25,53,80,443
```

Scan the first 1000 ports with a custom timeout:

```bash
python3 nexus.py example.com -p 1-1000 -t 1
```

Produce a JSON report for automation:

```bash
python3 nexus.py example.com -p 1-1024 --json > nexus-report.json
```

---

## 📂 Project structure

```text
NEXUS/
├── .github/
│   ├── workflows/
│   │   └── tests.yml
│   └── dependabot.yml
├── tests/
│   └── test_nexus.py
├── nexus.py
├── pyproject.toml
├── CHANGELOG.md
├── SECURITY.md
├── LICENSE
├── README.md        # English (this file)
├── README.tr.md     # Turkish
└── .gitignore
```

---

## 🧪 Testing

Run the unit tests with the standard library:

```bash
python3 -m unittest discover -s tests -v
```

The tests cover port parsing, malformed input, service labels, address handling, JSON reports, and a local open/closed port check. CI runs the suite on Python 3.11, 3.12, and 3.13 together with `compileall` and Ruff.

---

## 🔐 Responsible use

NEXUS is intended for **security research, network administration, and authorized testing**.

Only scan systems and ports that you own or have explicit permission to test.

Do not use NEXUS to access, disrupt, or probe unauthorized systems. Port scanning may be logged, rate-limited, or prohibited by network providers and hosting terms.

---

## 🛡️ Scope

NEXUS only performs TCP connect scans. It does not:

- exploit services or send application payloads,
- perform UDP scanning,
- attempt authentication or brute force,
- hide or spoof source addresses.

---

## 📜 License

MIT License. See [`LICENSE`](LICENSE) for details.

---

<div align="center">
  <strong>NEXUS</strong><br />
  <sub>Lightweight TCP discovery · v0.2.0</sub>
</div>
