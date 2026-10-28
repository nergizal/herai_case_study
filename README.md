# HerAI Studios: Yerel Veri ve API İşleme Uygulaması

HerAI Studios staj değerlendirme case study çözümü. Uygulama JSON, Excel (`.xlsx`, `.xls`) ve CSV formatındaki cihaz kayıtlarını okur, kayıtları güvenlik odaklı bir doğrulamadan geçirir, aktif ve kritik cihazları belirler, aktif cihazların ortalama tehdit skorunu hesaplar ve sonuçları terminale yazdırır. Ek olarak ücretsiz bir API'den (JSONPlaceholder) ilk 5 gönderinin başlığını gösterir; API çökerse yerel analiz yine de tamamlanır.

Test kapsamı: birim, entegrasyon, güvenlik/fuzzing, performans (10.000 kayıt) ve **Robot Framework** ile uçtan uca (E2E) kabul testleri.

## Özellikler

- **Çoklu format:** `.json`, `.xlsx`, `.xls` ve `.csv` dosyalarını uzantıdan otomatik algılar (varsayılan `data/devices.json`, isteğe bağlı dosya yolu argümanı)
- **Kayıt doğrulama (Skip & Warn):** geçersiz kayıt **atlanır ve uyarı yazılır**, program çökmez
  -  duplicate `id` reddedilir
  - `id` pozitif olmalıdır (negatif ve 0 reddedilir)
  - `device_name` içindeki `<script>` ve zararlı HTML etiketleri (XSS) süzülür
  - Katı tip denetimi: `bool`, `NaN`, `inf` ve metin türevi skorlar elenir
- `status == "active"` olan cihazların filtrelenmesi
- Aktif cihazlar arasında `threat_score >= 50` olanların "KRİTİK" işaretlenmesi
- Aktif cihazların ortalama tehdit skoru (2 ondalık basamak)
- API'den ilk 5 başlığın çekilmesi (15 sn zaman aşımı); API hata verirse yerel analiz yine de gösterilir
- Anlamlı çıkış kodları: başarıda `0`, yerel veri hatasında `1`
- Her `pytest` koşumunda zaman damgalı HTML test raporu (`reports/`)
- API testlerinde internet gerekmez, istekler mock'lanır


### Çalışma Akışı (Sekans Diyagramı)

Başarılı akış, dosya hatası durumundaki erken çıkış (çıkış kodu `1`) ve API izolasyonu (API hatası yerel analizi etkilemez, çıkış kodu `0`):

![Sekans diyagramı](docs/diagrams/sekans.png)

## Kullanılan Teknolojiler

| Teknoloji | Neden |
|---|---|
| Python 3.11+ | Liste/sözlük ve list comprehension ile problem kısa ve okunaklı çözülür |
| `pandas` + `openpyxl` | Excel / CSV / JSON verisini tek motorla okumak için |
| `requests` | Timeout, HTTP durum kontrolü ve hata yönetimi için okunaklı API |
| `pytest` + `pytest-html` | Parametreli testler, `capsys`/`tmp_path` yardımcıları ve HTML raporlama |
| `Robot Framework` | CLI seviyesinde E2E kabul testleri |
| `unittest.mock` (standart kütüphane) | API testlerini internetten bağımsız yapmak için |

## Gereksinimler

- Python 3.11+ (geliştirme ve test: 3.11.4)
- macOS üzerinde geliştirilmiş ve test edilmiştir
- Bağımlılıklar `requirements.txt` içindedir

## Kurulum

```bash
git clone <repo-url>
cd herai_case_study

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Çalıştırma

Komutlar **proje kök dizininden** ve sanal ortam aktifken çalıştırılmalıdır (varsayılan veri yolu göreli olduğu için).

```bash
# Varsayılan JSON verisi
python3 main.py

# Excel verisi
python3 main.py data/devices.xlsx

# Bozuk kayıt içeren deneme verisi
python3 main.py data/devices_bad.json
```

## Testleri Çalıştırma

```bash
# Birim, entegrasyon, güvenlik/fuzzing ve performans testleri
python3 -m pytest -v

# Robot Framework E2E kabul testleri
robot --timestamp-outputs --outputdir reports/robot_logs tests/device_analysis.robot
```

Toplam 58 test vardır ve tamamı geçer.

### Test Raporları

Raporlar üzerine yazılmadan, zaman damgasıyla `reports/` klasörüne kaydedilir:

- **Pytest:** `reports/test_report_YYYY-MM-DD_HH-MM-SS.htm` (herhangi bir tarayıcıda açılır)
- **Robot Framework:** `reports/robot_logs/report.htm`

Gereksinim, kabul kriteri, use case, test ve kod modülü ilişkisi için: [`docs/traceability.md`](docs/traceability.md).

## Örnek Çıktı

`python3 main.py` (case'in örnek verisi):

```
=============================================
      HERAI STUDIOS - CIHAZ ANALIZ RAPORU
=============================================

[ TÜM AKTİF CİHAZLAR]
  -> ID #1: Kamera-A - Skor: 85 [KRİTİK]
  -> ID #3: Kamera-C - Skor: 45 [NORMAL]
  -> ID #4: Kamera-D - Skor: 90 [KRİTİK]

[ KRİTİK CİHAZLAR (Skor >= 50)]
  -> ID #1: Kamera-A (Skor: 85)
  -> ID #4: Kamera-D (Skor: 90)

[ÖZET İSTATİSTİK]
  -> Aktif Cihaz Ortalama Tehdit Skoru: 73.33

[ HARİCİ API DUYURULARI (JSONPlaceholder - İlk 5)]
  [#1] sunt aut facere repellat provident occaecati excepturi optio reprehenderit
  [#2] qui est esse
  [#3] ea molestias quasi exercitationem repellat qui ipsa sit aut
  [#4] eum et est occaecati
  [#5] nesciunt quas odio
=============================================
```

`python3 main.py data/devices_bad.json` (bozuk kayıtlar uyarıyla atlanır; API bölümü internet durumuna bağlıdır, burada gösterilmemiştir):

```
[ UYARILAR / DOĞRULAMA HATALARI]
  -> 3. kayıt (id=3) atlandı: 'threat_score' alanı eksik
  -> 4. kayıt (id=4) atlandı: 'threat_score' sayı olmalı, gelen: 'seksen'
  -> 5. kayıt (id=5) atlandı: 'threat_score' sayı olmalı, gelen: True
  -> 6. kayıt (id=6) atlandı: 'status' geçersiz: 'Active'
  -> 7. kayıt atlandı: kayıt bir nesne (dict) değil

[ TÜM AKTİF CİHAZLAR]
  -> ID #1: Kamera-A - Skor: 85 [KRİTİK]
  -> ID #8: Kamera-H - Skor: 50 [KRİTİK]

[KRİTİK CİHAZLAR (Skor >= 50)]
  -> ID #1: Kamera-A (Skor: 85)
  -> ID #8: Kamera-H (Skor: 50)

[ ÖZET İSTATİSTİK]
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
├── conftest.py             # Pytest zaman damgalı .htm rapor hook'u
├── pytest.ini
├── requirements.txt        # Proje ve test bağımlılıkları
├── data/
│   ├── devices.json        # Case'in örnek verisi
│   ├── devices.xlsx        # Örnek Excel verisi
│   └── devices_bad.json    # Bozuk kayıt içeren deneme verisi
├── src/
│   ├── exceptions.py       # Özel hata hiyerarşisi
│   ├── data_loader.py      # Çoklu format (JSON/Excel/CSV) veri yükleyici
│   ├── validator.py        # Kayıtları doğrular ve süzer, uyarı üretir
│   ├── analyzer.py         # Filtreleme, kritik cihaz, ortalama, analiz akışı
│   ├── api_client.py       # API isteği ve hata dönüştürme
│   └── presenter.py        # Terminal çıktısı
├── tests/
│   ├── test_validator.py
│   ├── test_analyzer.py
│   ├── test_api_client.py
│   ├── test_main.py
│   ├── test_performance_fuzzing.py   # 10.000 kayıt stres ve güvenlik testleri
│   └── device_analysis.robot         # Robot Framework E2E testleri
├── reports/                # Zaman damgalı test raporları
└── docs/
    ├── traceability.md     # İzlenebilirlik matrisi
    └── diagrams/
        ├── mimari-akis.png # Katmanlı mimari diyagramı
        └── sekans.png      # Sekans diyagramı
```

## İş Kuralları

1. Yalnızca `status` değeri tam olarak `"active"` olan cihazlar analize girer.
2. Kritiklik yalnızca aktif cihazlar için değerlendirilir; pasif ve skoru yüksek bir cihaz kritik **sayılmaz**.
3. Eşik dahildir: `threat_score >= 50` olan cihaz kritiktir (skoru tam 50 olan kritiktir).
4. Ortalama, **tüm aktif cihazların** skorlarının aritmetik ortalamasıdır (kritik olmayanlar dahil).
5. Aktif cihaz yoksa ortalama hesaplanmaz, bilgi mesajı yazılır.
6. Bir kayıt şu durumlarda geçersizdir ve uyarıyla atlanır: sözlük değilse; `id`, `device_name`, `status` veya `threat_score` alanı eksikse; `id` pozitif bir sayı değilse veya daha önce görülmüşse; `device_name` boş ya da metin değilse; `status` `"active"` / `"inactive"` dışındaysa (büyük/küçük harf duyarlıdır); `threat_score` sayı değilse (`true`/`false`, `NaN` ve sonsuz değerler dahil). `device_name` içindeki script/HTML etiketleri süzülür.

## Tasarım Kararları

- **Doğrulama ayrı bir modülde (`validator.py`):** Tek sorumluluk. Analiz fonksiyonları verinin geçerli olduğunu varsayabilir; bu sayede eksik veri sessizce 0 sayılmaz.
- **Geçersiz kayıt atlanır, program durmaz:** Tek bir bozuk kayıt tüm analizi öldürmemeli. Her atlanan kayıt için bir uyarı üretilir.
- **API kodu ayrı modülde (`api_client.py`):** Ağ hatası yerel analizi etkilememeli. API hataları tek bir hata tipine çevrilir; `main.py` bunu yakalar ve yerel sonuçlar yine gösterilir.
- **Özel hata hiyerarşisi (`exceptions.py`):** Dosya/şema ve API hataları ayrı tiplerle ifade edilir; kullanıcıya traceback yerine anlaşılır mesaj gösterilir.
- **Bool kontrolü:** Python'da `bool`, `int`'in alt sınıfıdır; `threat_score: true` değerinin skor sayılmaması için ayrıca elenir.
- **Çıkış kodları:** Yerel veri okunamazsa `1`; API hatası yerel analiz başarılıysa çıkış kodunu değiştirmez (`0`).
- **API testleri mock'lanır:** Testler internetten bağımsız ve hızlıdır.
- **Eşik sabiti:** Kritik eşik (`50`) `analyzer.CRITICAL_THRESHOLD` sabitidir, sunum katmanı da aynı sabiti kullanır.
- **Eklenmeyen teknolojiler:** Case'in gerektirmediği için web arayüzü, veritabanı ve Docker kullanılmadı.

