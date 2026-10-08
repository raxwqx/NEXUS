# 🕷️ NEXUS

**Lightweight TCP port scanner built for fast network discovery & security research.**

NEXUS is a simple and lightweight TCP port scanner written in Python.
It is designed to quickly check TCP ports on a hostname or IPv4 address without requiring any third-party Python packages.

## ✨ Features

* 🔎 TCP port scanning
* 🌐 Hostname and IPv4 support
* 🎯 Custom port selection
* 🔢 Port range scanning
* ⏱️ Configurable socket timeout
* ⚡ Concurrent port scanning
* 📦 Zero third-party dependencies
* 🐍 Written entirely in Python
* 💻 Works directly from the command line

## 📥 Installation

### Clone the repository

```bash
git clone https://github.com/raxwqx/NEXUS.git
cd NEXUS
```

NEXUS does not require any external Python packages.

Make sure Python 3 is installed:

```bash
python3 --version
```

### Run NEXUS

You can run NEXUS directly with:

```bash
python3 nexus.py --help
```

## 🚀 Usage

### Basic scan

Scan the default port range (`1-1024`):

```bash
python3 nexus.py 127.0.0.1
```

Example output:

```text
NEXUS
====================================
Target : 127.0.0.1 (127.0.0.1)
Ports  : 1-1024

[+] 22/tcp OPEN
[+] 80/tcp OPEN
[+] 443/tcp OPEN

Scan complete. 3 open port(s).
```

### Scan selected ports

Specify individual ports:

```bash
python3 nexus.py 127.0.0.1 -p 22,80,443
```

### Scan a port range

Scan a specific range:

```bash
python3 nexus.py 127.0.0.1 -p 1-1024
```

### Custom timeout

Set the socket timeout in seconds:

```bash
python3 nexus.py 127.0.0.1 -t 1
```

### Change the number of workers

NEXUS uses concurrent scanning by default. You can change the number of workers:

```bash
python3 nexus.py 127.0.0.1 -w 50
```

### Combine options

Options can be combined:

```bash
python3 nexus.py 192.168.1.1 -p 1-1024 -t 0.5 -w 100
```

## ⚙️ Command-line options

```text
usage: nexus [-h] [-p PORTS] [-t TIMEOUT] [-w WORKERS] target

Minimal TCP port scanner.

positional arguments:
  target                Hostname or IPv4 address to scan

options:
  -h, --help            show this help message and exit
  -p, --ports PORTS     Ports to scan, e.g. 22,80,443 or 1-1024
  -t, --timeout TIMEOUT
                        Socket timeout in seconds
  -w, --workers WORKERS
                        Concurrent scan workers
```

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

## 📂 Project structure

```text
NEXUS/
├── nexus.py
├── README.md
├── LICENSE
└── .gitignore
```

## 🔐 Responsible use

NEXUS is intended for **security research, network administration, and authorized testing**.

Only scan systems and ports that you own or have explicit permission to test.

Do not use NEXUS to access, disrupt, or probe unauthorized systems.

## 📜 License

This project is licensed under the terms of the included `LICENSE` file.
