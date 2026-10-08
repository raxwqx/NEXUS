# NEXUS

Minimal TCP port scanner written in Python.

## Features

- TCP port scanning
- Hostname or IPv4 target
- Custom port list or range
- Configurable timeout
- Concurrent scanning
- Zero third-party dependencies

## Usage

```bash
python3 nexus.py 127.0.0.1
```

Scan selected ports:

```bash
python3 nexus.py 127.0.0.1 -p 22,80,443
```

Scan a range:

```bash
python3 nexus.py 127.0.0.1 -p 1-1024
```

Only scan systems and ports you are authorized to test.
