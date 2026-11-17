# Security Policy / Güvenlik Politikası

## Supported versions / Desteklenen sürümler

Security fixes are applied to the latest release on the `main` branch.

Güvenlik düzeltmeleri `main` dalındaki en son sürüme uygulanır.

## Reporting a vulnerability / Güvenlik açığı bildirme

Please **do not** open a public issue for a security problem. Do not attach
real host lists, credentials, or sensitive network data.

Güvenlik sorunları için lütfen **herkese açık issue açma**. Gerçek ana makine
listesi, kimlik bilgisi veya hassas ağ verisi ekleme.

Use GitHub private vulnerability reporting:

- <https://github.com/raxwqx/NEXUS/security/advisories/new>

Please include:

- affected version or commit,
- steps to reproduce,
- expected and actual behavior,
- impact assessment,
- whether the issue can cause unintended scanning or network traffic.

Lütfen şunları ekle:

- etkilenen sürüm veya commit,
- yeniden üretme adımları,
- beklenen ve gerçek davranış,
- etki değerlendirmesi,
- sorunun istenmeyen taramaya veya ağ trafiğine yol açıp açamayacağı.

## Scope / Kapsam

Relevant reports include command-injection risks, unsafe target parsing,
resource exhaustion from crafted port ranges, unexpected outbound connections,
and denial-of-service conditions in the scanner.

İlgili bildirimler arasında komut enjeksiyonu riskleri, güvensiz hedef
ayrıştırma, hazırlanmış port aralıklarıyla kaynak tükenmesi, beklenmeyen dış
bağlantılar ve tarayıcıdaki hizmet reddi koşulları yer alır.

## Authorized use / Yetkili kullanım

NEXUS sends TCP connection attempts to the target you specify. Only scan hosts
and ports that you own or have explicit written permission to test. Unauthorized
scanning may be illegal and may violate provider terms.

NEXUS belirttiğiniz hedefe TCP bağlantı denemeleri gönderir. Yalnızca sahibi
olduğunuz veya açık yazılı izin aldığınız ana makineleri ve portları tarayın.
Yetkisiz tarama yasa dışı olabilir ve sağlayıcı koşullarını ihlal edebilir.
