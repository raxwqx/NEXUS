# 🕷️ NEXUS

**Hızlı ağ keşfi ve yetkilendirilmiş güvenlik araştırmaları için hafif TCP port tarayıcı.**

NEXUS, Python ile yazılmış küçük ve bağımlılıksız bir TCP port tarayıcıdır. Ana makine adlarını, IPv4 ve IPv6 adreslerini eşzamanlı işçilerle kontrol eder; **makine tarafından okunabilir JSON raporu** veya servis etiketleri içeren kompakt bir terminal özeti üretebilir.

<p>
  <img src="https://img.shields.io/badge/version-0.2.0-9cffb5?style=for-the-badge&labelColor=101713" alt="Sürüm 0.2.0" />
  <img src="https://img.shields.io/badge/Python-3.11%2B-9bdcff?style=for-the-badge&logo=python&logoColor=white&labelColor=101713" alt="Python 3.11 veya üzeri" />
  <img src="https://img.shields.io/badge/License-MIT-f3d58a?style=for-the-badge&labelColor=101713" alt="MIT Lisansı" />
</p>

[English](README.md) · [Türkçe](README.tr.md)

---

## ✨ Özellikler

- 🔎 Eşzamanlı TCP port taraması
- 🌐 Ana makine adı, IPv4 ve **IPv6** hedefleri
- 🧾 **`--json` ile JSON raporları**
- 🏷️ Açık portlar için yaygın servis etiketleri (ssh, http, https, …)
- 🎯 Özel port listeleri ve aralıkları
- 🧱 Güvenli port ayrıştırma ve anlaşılır doğrulama hataları
- ⏱️ Yapılandırılabilir ve sınırlandırılmış soket zaman aşımı
- ⚡ Yapılandırılabilir işçi sayısı (1–1024)
- 🛑 Ctrl+C ile düzgün durdurma (çıkış kodu 130)
- 📦 Sıfır üçüncü taraf çalışma zamanı bağımlılığı
- 🐍 Tamamen Python
- 💻 Doğrudan komut satırından çalışır

---

## 📥 Kurulum

### Depoyu klonlayın

```bash
git clone https://github.com/raxwqx/NEXUS.git
cd NEXUS
```

NEXUS'un Python standart kütüphanesi dışında çalışma zamanı bağımlılığı yoktur.

Python 3.11 veya üzerinin kurulu olduğundan emin olun:

```bash
python3 --version
```

### NEXUS'u çalıştırın

```bash
python3 nexus.py --help
```

İsterseniz komut olarak da kurabilirsiniz:

```bash
python3 -m pip install -e '.[dev]'
nexus --version
```

---

## 🚀 Kullanım

### Temel tarama

Varsayılan port aralığını (`1-1024`) tarayın:

```bash
python3 nexus.py 127.0.0.1
```

Örnek çıktı:

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

### JSON raporu

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

### Seçili portlar ve aralıklar

```bash
python3 nexus.py 127.0.0.1 -p 22,80,443
python3 nexus.py 127.0.0.1 -p 1-1024
python3 nexus.py 127.0.0.1 -p 8000-8100,443
```

`8100-8000` gibi ters aralıklar otomatik olarak düzeltilir.

### IPv6 ve adres aileleri

```bash
python3 nexus.py ::1 -p 22,80,443
python3 nexus.py example.com -6 -p 443
python3 nexus.py example.com -4 -p 443
```

`-4` IPv4'ü, `-6` IPv6'yı zorlar. Varsayılan olarak ana makine adı her iki aileyi de sunuyorsa IPv4 tercih edilir.

### Zaman aşımı ve işçi sayısı

```bash
python3 nexus.py 127.0.0.1 -t 1
python3 nexus.py 127.0.0.1 -w 50
```

Zaman aşımı 3600 saniyeye kadar sonlu bir sayı olmalıdır; işçi sayısı 1 ile 1024 arasında olmalıdır.

### Seçenekleri birleştirme

```bash
python3 nexus.py 192.168.1.1 -p 1-1024 -t 0.5 -w 100
```

---

## ⚙️ Komut satırı seçenekleri

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

Geçerli port aralığı `1–65535`'tir. Aralıklar genişletilmeden önce doğrulanır; böylece geçersiz bir aralık bellek tüketmeden hemen reddedilir.

---

## 🧪 Örnekler

Yerel sistemi tarayın:

```bash
python3 nexus.py 127.0.0.1
```

Ana makine adını tarayın:

```bash
python3 nexus.py example.com
```

Yaygın portları tarayın:

```bash
python3 nexus.py example.com -p 22,25,53,80,443
```

İlk 1000 portu özel zaman aşımıyla tarayın:

```bash
python3 nexus.py example.com -p 1-1000 -t 1
```

Otomasyon için JSON raporu üretin:

```bash
python3 nexus.py example.com -p 1-1024 --json > nexus-report.json
```

---

## 📂 Proje yapısı

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
├── README.md        # İngilizce
├── README.tr.md     # Türkçe (bu dosya)
└── .gitignore
```

---

## 🧪 Testler

Birim testlerini standart kütüphaneyle çalıştırın:

```bash
python3 -m unittest discover -s tests -v
```

Testler port ayrıştırma, bozuk girdi, servis etiketleri, adres işleme, JSON raporları ve yerel açık/kapalı port kontrolünü kapsar. CI, test paketini Python 3.11, 3.12 ve 3.13 üzerinde `compileall` ve Ruff ile birlikte çalıştırır.

---

## 🔐 Sorumlu kullanım

NEXUS **güvenlik araştırması, ağ yönetimi ve yetkilendirilmiş testler** için tasarlanmıştır.

Yalnızca sahibi olduğunuz veya açık izin aldığınız sistemleri ve portları tarayın.

Yetkisiz sistemlere erişmek, onları bozmak veya yoklamak için NEXUS'u kullanmayın. Port taraması ağ sağlayıcıları ve barındırma koşulları tarafından günlüğe alınabilir, hız sınırına tabi tutulabilir veya yasaklanabilir.

---

## 🛡️ Kapsam

NEXUS yalnızca TCP connect taraması yapar. Şunları yapmaz:

- servisleri istismar etmek veya uygulama yükü göndermek,
- UDP taraması yapmak,
- kimlik doğrulama denemesi veya kaba kuvvet saldırısı yapmak,
- kaynak adresini gizlemek veya sahte göstermek.

---

## 📜 Lisans

MIT Lisansı. Ayrıntılar için [`LICENSE`](LICENSE) dosyasına bakın.

---

<div align="center">
  <strong>NEXUS</strong><br />
  <sub>Hafif TCP keşfi · v0.2.0</sub>
</div>
