# HerAI Studios: Yerel Veri ve API İşleme Uygulaması

HerAI Studios staj değerlendirme case study çözümü. Uygulama bir JSON dosyasındaki cihaz kayıtlarını okur, aktif ve kritik cihazları belirler, aktif cihazların ortalama tehdit skorunu hesaplar ve sonuçları terminale yazdırır. Ek olarak ücretsiz bir API'den (JSONPlaceholder) ilk 5 gönderinin başlığını gösterir.

## Özellikler

- JSON dosyasından cihaz kaydı okuma (varsayılan `data/devices.json`, isteğe bağlı dosya yolu argümanı)
- Her kaydın doğrulanması: geçersiz kayıt **atlanır ve uyarı yazılır**, program çökmez
- `status == "active"` olan cihazların filtrelenmesi
- Aktif cihazlar arasında `threat_score >= 50` olanların "KRİTİK" işaretlenmesi
- Aktif cihazların ortalama tehdit skorunun hesaplanması (2 ondalık basamak)
- API'den ilk 5 başlığın çekilmesi; API hata verirse yerel analiz yine de gösterilir
- Anlamlı çıkış kodları: başarıda `0`, yerel veri hatasında `1`
- `pytest` ile 61 otomatik test (API testlerinde internet gerekmez, istekler mock'lanır)

## Kullanılan Teknolojiler

| Teknoloji | Neden |
|---|---|
| Python 3.11 | Liste/sözlük ve list comprehension ile bu problem kısa ve okunaklı çözülür |
| `json` (standart kütüphane) | JSON okumak için ek bağımlılık gerekmez |
| `requests` | Timeout, HTTP durum kontrolü ve hata yönetimi için okunaklı API |
| `pytest` | Parametreli testler ve `capsys`, `tmp_path` gibi yardımcılar |
| `unittest.mock` (standart kütüphane) | API testlerini internetten bağımsız yapmak için |

## Gereksinimler

- Python 3.11 (test edilen sürüm: 3.11.4)
- macOS üzerinde geliştirilmiş ve test edilmiştir
- `requests` (çalıştırmak için), `pytest` (testler için)

## Kurulum

```bash
git clone <repo-url>
cd herai_case_study

python3 -m venv venv
source venv/bin/activate

pip install -r requirements-dev.txt
```

Yalnızca uygulamayı çalıştırmak için `requirements-dev.txt` yerine `requirements.txt` yeterlidir.

## Çalıştırma

Komutlar **proje kök dizininden** ve sanal ortam aktifken çalıştırılmalıdır (varsayılan veri yolu göreli olduğu için).

```bash
# Varsayılan veri dosyası (data/devices.json)
python3 main.py

# Başka bir dosya ile
python3 main.py data/devices_bad.json
```

## Testleri Çalıştırma

```bash
python3 -m pytest -v
```

Son çalıştırmanın çıktısı: [`docs/test-results.txt`](docs/test-results.txt) (61 test, tamamı geçti, Python 3.11.4).

| Dosya | Test sayısı | Kapsam |
|---|---|---|
| `tests/test_validator.py` | 32 | Kayıt doğrulama (eksik alan, tip hataları, bool/NaN, geçersiz status) |
| `tests/test_analyzer.py` | 12 | Filtreleme, kritik cihaz, sınır değer (50/49), ortalama, bozuk veriyle pipeline |
| `tests/test_api_client.py` | 7 | Başarı, timeout, bağlantı/HTTP hatası, bozuk JSON, liste olmayan yanıt, geçersiz kayıtlar |
| `tests/test_data_loader.py` | 5 | Geçerli dosya, dosya yok, bozuk JSON, kök liste değil, boş dosya |
| `tests/test_main.py` | 5 | Çıkış kodları (0/1), API hatasında yerel sonuç, terminal çıktı biçimi |

Gereksinim, kabul kriteri, use case, test ve kod modülü ilişkisi için: [`docs/traceability.md`](docs/traceability.md).

## Örnek Çıktı

`python3 main.py` (case'in örnek verisi):

```
=============================================
      HERAI STUDIOS - CIHAZ ANALIZ RAPORU
=============================================

[📊 TÜM AKTİF CİHAZLAR]
  -> ID #1: Kamera-A - Skor: 85 [KRİTİK]
  -> ID #3: Kamera-C - Skor: 45 [NORMAL]
  -> ID #4: Kamera-D - Skor: 90 [KRİTİK]

[🚨 KRİTİK CİHAZLAR (Skor >= 50)]
  -> ID #1: Kamera-A (Skor: 85)
  -> ID #4: Kamera-D (Skor: 90)

[📈 ÖZET İSTATİSTİK]
  -> Aktif Cihaz Ortalama Tehdit Skoru: 73.33

[🌐 HARİCİ API DUYURULARI (JSONPlaceholder - İlk 5)]
  [#1] sunt aut facere repellat provident occaecati excepturi optio reprehenderit
  [#2] qui est esse
  [#3] ea molestias quasi exercitationem repellat qui ipsa sit aut
  [#4] eum et est occaecati
  [#5] nesciunt quas odio
=============================================
```

`python3 main.py data/devices_bad.json` (bozuk kayıtlar uyarıyla atlanır; API bölümü internet durumuna bağlıdır, burada gösterilmemiştir):

```
[⚠️ UYARILAR / DOĞRULAMA HATALARI]
  -> 3. kayıt (id=3) atlandı: 'threat_score' alanı eksik
  -> 4. kayıt (id=4) atlandı: 'threat_score' sayı olmalı, gelen: 'seksen'
  -> 5. kayıt (id=5) atlandı: 'threat_score' sayı olmalı, gelen: True
  -> 6. kayıt (id=6) atlandı: 'status' geçersiz: 'Active'
  -> 7. kayıt atlandı: kayıt bir nesne (dict) değil

[📊 TÜM AKTİF CİHAZLAR]
  -> ID #1: Kamera-A - Skor: 85 [KRİTİK]
  -> ID #8: Kamera-H - Skor: 50 [KRİTİK]

[🚨 KRİTİK CİHAZLAR (Skor >= 50)]
  -> ID #1: Kamera-A (Skor: 85)
  -> ID #8: Kamera-H (Skor: 50)

[📈 ÖZET İSTATİSTİK]
  -> Aktif Cihaz Ortalama Tehdit Skoru: 67.50
```

Var olmayan dosya verilirse hata `stderr`'e yazılır ve çıkış kodu `1` olur:

```
[X] Kritik Hata: Veri dosyası bulunamadı: yok.json
```

## Proje Dizin Yapısı

```
herai_case_study/
├── main.py                 # Giriş noktası: akışı yönetir, çıkış kodunu döndürür
├── pytest.ini
├── requirements.txt        # Çalışma zamanı bağımlılığı (requests)
├── requirements-dev.txt    # Test bağımlılıkları (pytest)
├── data/
│   ├── devices.json        # Case'in örnek verisi
│   └── devices_bad.json    # Bozuk kayıt içeren deneme verisi
├── src/
│   ├── data_loader.py      # JSON dosyasını okur
│   ├── validator.py        # Kayıtları doğrular, uyarı üretir
│   ├── analyzer.py         # Filtreleme, kritik cihaz, ortalama, analiz akışı
│   ├── api_client.py       # API isteği ve hata dönüştürme
│   └── presenter.py        # Terminal çıktısı
├── tests/                  # pytest testleri
└── docs/
    ├── traceability.md     # İzlenebilirlik matrisi
    └── test-results.txt    # Son test çalıştırma çıktısı
```

## İş Kuralları

1. Yalnızca `status` değeri tam olarak `"active"` olan cihazlar analize girer.
2. Kritiklik yalnızca aktif cihazlar için değerlendirilir; pasif ve skoru yüksek bir cihaz kritik **sayılmaz**.
3. Eşik dahildir: `threat_score >= 50` olan cihaz kritiktir (skoru tam 50 olan kritiktir).
4. Ortalama, **tüm aktif cihazların** skorlarının aritmetik ortalamasıdır (kritik olmayanlar dahil).
5. Aktif cihaz yoksa ortalama hesaplanmaz, bilgi mesajı yazılır.
6. Bir kayıt şu durumlarda geçersizdir ve uyarıyla atlanır: sözlük değilse; `id`, `device_name`, `status` veya `threat_score` alanı eksikse; `device_name` boş ya da metin değilse; `status` `"active"` / `"inactive"` dışındaysa (büyük/küçük harf duyarlıdır); `threat_score` sayı değilse (`true`/`false`, `NaN` ve sonsuz değerler dahil).

## Tasarım Kararları

- **Doğrulama ayrı bir modülde (`validator.py`):** Tek sorumluluk. Analiz fonksiyonları verinin geçerli olduğunu varsayabilir; bu sayede eksik veri sessizce 0 sayılmaz.
- **Geçersiz kayıt atlanır, program durmaz:** Tek bir bozuk kayıt tüm analizi öldürmemeli. Her atlanan kayıt için bir uyarı üretilir.
- **API kodu ayrı modülde (`api_client.py`):** Ağ hatası yerel analizi etkilememeli. API hataları `RuntimeError` olarak tek tipe çevrilir; `main.py` bunu yakalar ve yerel sonuçlar yine gösterilir.
- **Bool kontrolü:** Python'da `bool`, `int`'in alt sınıfıdır; `threat_score: true` değerinin skor sayılmaması için ayrıca elenir.
- **Çıkış kodları:** Yerel veri okunamazsa `1`; API hatası yerel analiz başarılıysa çıkış kodunu değiştirmez (`0`).
- **API testleri mock'lanır:** Testler internetten bağımsız ve hızlıdır.
- **Eşik sabiti:** Kritik eşik (`50`) `analyzer.CRITICAL_THRESHOLD` sabitidir, sunum katmanı da aynı sabiti kullanır.
- **Eklenmeyen teknolojiler:** Case'in gerektirmediği için web arayüzü, veritabanı ve Docker kullanılmadı.

## Bilinen Sınırlamalar

- `threat_score` için değer aralığı (ör. 0–100) kontrol edilmez; case aralık belirtmediği için sonlu her sayı geçerlidir.
- `status` büyük/küçük harf duyarlıdır; `"Active"` geçersiz sayılır ve uyarıyla atlanır.
- Uyarılar kaydın sırasına (ve varsa `id`'sine) göre verilir; aynı `id`'nin tekrar edip etmediği kontrol edilmez.
- API'den yalnızca ilk 5 kayda bakılır. Bu 5 kayıt içinde geçersiz olan (sözlük olmayan, `title`'ı eksik veya boş) varsa sessizce atlanır; bu durumda 5'ten az başlık görünebilir.
- API zaman aşımı 5 saniyedir (`fetch_first_five_posts(timeout=...)` ile değiştirilebilir).
- Varsayılan veri yolu çalışma dizinine göredir; program proje kök dizininden çalıştırılmalıdır.
- Yalnızca macOS ve Python 3.11.4 üzerinde test edilmiştir.