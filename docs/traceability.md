# İzlenebilirlik Matrisi (Traceability Matrix)

Bu belge, HerAI Studios vaka çalışmasındaki iş kurallarının, işlevsel (FR) ve işlevsel olmayan (NFR) gereksinimlerin, kullanım senaryolarının (UC), kabul kriterlerinin (AC) ve otomatik test senaryolarının (TC) uçtan uca izlenebilirliğini sunar.

## 1. İşlevsel Gereksinimler ve Test Matrisi

| Gereksinim (FR) | Kabul Kriteri (AC) | Use Case (UC) | İlgili Test Senaryoları (TC) | Kod Modülü |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01:** Çoklu format veri yükleme (JSON/Excel/CSV) | AC-01-1, 01-2, 01-3 | UC-01, UC-04 | TC-32...TC-36, TC-38, TC-41, Robot-E2E | `data_loader.py`, `main.py` |
| **FR-02:** Kayıt doğrulama ve güvenlik sanitasyonu (Duplicate ID, XSS, Negative ID) | AC-02-1, 02-2, 02-3 | UC-02 | TC-11...TC-19, TC-21, Fuzzing-Test | `validator.py` |
| **FR-03:** Yalnızca `active` cihazları filtrele | AC-03-1 | UC-03 | TC-20, TC-21 | `analyzer.py` |
| **FR-04:** `threat_score >= 50` kritik cihaz işareti | AC-04-1, 04-2 | UC-03 | TC-22, TC-23 | `analyzer.py` |
| **FR-05:** Aktif cihaz ortalamasını hesapla (yoksa `None` dön) | AC-05-1, 05-2 | UC-03 | TC-20, TC-24, TC-42 | `analyzer.py` |
| **FR-06:** Sonuçları hassas formatta yazdır (2 ondalık basamak) | AC-06-1 | UC-05 | TC-40 | `presenter.py` |
| **FR-07:** API'den ilk 5 başlığı güvenli çek (15 sn timeout) | AC-07-1...07-4 | UC-06 | TC-25...TC-31 | `api_client.py` |
| **FR-08:** API çökse bile yerel analiz tamamlanır (çıkış kodu 0) | AC-08-1 | UC-07 | TC-37, TC-39 | `main.py` |

## 2. Kullanım Senaryoları (Use Cases)

- **UC-01 (Veri yükleme, mutlu yol):** Kullanıcı CLI üzerinden JSON, Excel veya CSV dosyasını verir. Sistem veriyi `pandas`/`json` ile okuyup belleğe aktarır. *(TC-32, TC-38, Robot-E2E)*
- **UC-02 (Güvenlik denetimi ve sanitasyon):** Sistem ham veride bozuk kayıtları, XSS etiketlerini (`<script>`), negatif/mükerrer ID'leri ve geçersiz tipleri tespit eder. Geçersizleri atlar ve uyarı üretir. *(TC-11...TC-19, TC-21, `test_fuzzing_and_malicious_payloads`)*
- **UC-03 (Analiz ve istatistik):** Yalnızca `active` cihazlar filtrelenir, skoru ≥ 50 olanlar kritik işaretlenir ve ortalama tehdit skoru hesaplanır. *(TC-20, TC-22, TC-23, TC-24, TC-42)*
- **UC-04 (Hatalı dosya/şema yönetimi):** Olmayan veya bozuk formatlı dosyada traceback verilmez; özel istisna (`FileFormatError`) yakalanır ve çıkış kodu `1` döner. *(TC-33...TC-36, TC-41)*
- **UC-05 (Konsol raporlama):** Analiz sonuçları ve varsa uyarılar düzenli formatta konsola basılır. *(TC-40)*
- **UC-06 (Harici API entegrasyonu):** JSONPlaceholder servisinden ilk 5 gönderi çekilir. *(TC-25...TC-31)*
- **UC-07 (Hata toleransı ve izolasyon):** API'de zaman aşımı (> 15 sn) veya bağlantı hatası olsa da yerel analiz sunulur ve program `0` çıkış koduyla biter. *(TC-37, TC-39)*

## 3. Fonksiyonel Olmayan Gereksinimler (NFR)

| NFR ID | Gereksinim | Mimari / Teknik Karşılık |
| :--- | :--- | :--- |
| **NFR-01** | Python 3.11+ uyumu | Python 3.11 ortamında geliştirildi ve doğrulandı. |
| **NFR-02** | Clean code standardı | Gereksiz yorumlar temizlendi, type hint'ler ve modüler fonksiyonlar uygulandı. |
| **NFR-03** | Test edilebilirlik | İş mantığı I/O'dan ayrıldı, saf fonksiyonlar yazıldı. |
| **NFR-04** | Kontrollü hata yönetimi | Traceback engellendi; `src/exceptions.py` altında özel istisna hiyerarşisi kuruldu. |
| **NFR-05** | API zaman aşımı | `timeout=15.0` saniye sınırı getirildi. |
| **NFR-06** | Yük ve performans dayanıklılığı | 10.000 kayıtlık veri seti < 0.1 sn'de işlendi (`test_performance_stress_10k_records`). |
| **NFR-07** | İnternetsiz koşabilen testler | API testleri `unittest.mock` ile izole edildi. |
| **NFR-08** | Zaman damgalı HTML raporlama | `conftest.py` hook'u ile her koşumda `reports/test_report_YYYY-MM-DD_HH-MM-SS.htm` üretilir. |
| **NFR-09** | Uçtan uca kabul testleri | Robot Framework (`tests/device_analysis.robot`) ile CLI seviyesinde test edildi. |