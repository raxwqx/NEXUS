# Changelog

Notable changes to NEXUS are documented here.

## 0.2.0 - IPv6, JSON reports, and safer input handling

### Added

- **IPv6 support:** hostnames, IPv4 literals, and IPv6 literals are resolved
  through `getaddrinfo`; use `-4` or `-6` to force an address family.
- **JSON reports:** `--json` prints a machine-readable report with the target,
  address family, requested port count, open ports, service labels, timing,
  and timeout/worker settings.
- Common service labels for open ports (`22/tcp ssh`, `443/tcp https`, ...).
- Scan duration in the human-readable summary.
- `--version`, unit tests, CI, Dependabot, `SECURITY.md`, `CHANGELOG.md`, and
  packaging metadata.

### Fixed

- Port ranges are validated **before** expansion, so `1-999999` fails cleanly
  instead of exhausting memory.
- Invalid ports, malformed ranges, and empty port lists now produce clear
  error messages instead of Python `int()` tracebacks.
- Non-finite, zero, negative, and excessive timeouts are rejected.
- Worker counts are bounded to 1–1024.
- Ctrl+C now stops the scan with exit code 130 instead of printing a traceback.
- IPv4-only resolution was replaced with address-family aware resolution, so
  IPv6 literals no longer fail with a generic DNS error.
- Per-socket errors are handled without aborting the remaining scan.
- A friendly summary is printed after scanning.

## 0.1.0 - Initial release

- Concurrent TCP port scanning.
- Hostname and IPv4 targets.
- Comma-separated ports and START-END ranges.
- Configurable timeout and worker count.
- Zero third-party runtime dependencies.
