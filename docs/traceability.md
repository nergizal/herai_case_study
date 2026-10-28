# İzlenebilirlik Matrisi (Traceability Matrix)

Bu belge, HerAI Studios vaka çalışmasındaki iş kurallarının, işlevsel  ve işlevsel olmayan  gereksinimlerin, kullanım senaryolarının , kabul kriterlerinin  ve otomatik test senaryolarının modüler bazda uçtan uca haritasını sunar.

## 1. İşlevsel Gereksinimler ve Test Matrisi

| Gereksinim (FR) | Kabul Kriteri (AC) | Use Case (UC) | İlgili Test Senaryoları (TC) | Kod Modülü |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01:** JSON dosyasını oku (Varsayılan + Argüman) | AC-01-1, 01-2, 01-3 | UC-01, UC-04 | TC-32, TC-33, TC-34, TC-35, TC-36, TC-38, TC-41 | `data_loader.py`, `main.py` |
| **FR-02:** Kayıtları doğrula, geçersizi atla (Strateji B) | AC-02-1, 02-2, 02-3 | UC-02 | TC-11...TC-19, TC-21 | `validator.py` |
| **FR-03:** Yalnızca 'active' cihazları filtrele | AC-03-1 | UC-03 | TC-20 (Resmi Veri Testi) | `analyzer.py` |
| **FR-04:** threat_score >= 50 kritik cihaz işareti | AC-04-1, 04-2, 04-3 | UC-03 | TC-22, TC-23 | `analyzer.py` |
| **FR-05:** Aktif cihaz ortalamasını hesapla | AC-05-1, 05-2 | UC-03 | TC-20, TC-24, TC-42 | `analyzer.py` |
| **FR-06:** Sonuçları okunaklı formatta yazdır | AC-06-1 | UC-05 | TC-40 | `presenter.py` |
| **FR-07:** API'den ilk 5 başlığı güvenli çek | AC-07-1, 07-2, 07-3, 07-4 | UC-06 | TC-25, TC-26, TC-27, TC-28, TC-29, TC-30, TC-31 | `api_client.py` |
| **FR-08:** API düşse bile yerel analiz tamamlanır | AC-08-1 | UC-07 | TC-37, TC-39 | `main.py` |

---

## 2. Kullanım Senaryoları (Use Cases) Detaylı Listesi

* **UC-01 (Yerel Veri Yükleme - Mutlu Yol):** Kullanıcı komut satırından `main.py`'yi çalıştırır. Sistem `data/devices.json` dosyasını hatasız okur ve ham veriyi belleğe alır. *(İlgili Testler: TC-32, TC-38)*
* **UC-02 (Veri Doğrulama ve Filtreleme - İstisna Akışı):** Sistem ham verideki bozuk kayıtları (eksik alan, bool tuzağı, NaN/inf değerler) inceler. Geçersizleri Strateji B gereği atlar, `stderr` üzerinden uyarı üretir ve geçerli kayıtları korur. *(İlgili Testler: TC-11...TC-19, TC-21)*
* **UC-03 (İş Mantığı ve İstatistik Analizi):** Temizlenen veriler arasından yalnızca `active` olanlar seçilir, skoru $\ge 50$ olanlar kritik olarak işaretlenir ve ortalama tehdit skoru hesaplanır. *(İlgili Testler: TC-20, TC-22, TC-23, TC-24, TC-42)*
* **UC-04 (Hatalı Dosya Yönetimi - Alternatif Akış):** Kullanıcı var olmayan veya bozuk formatlı bir JSON dosyası yollarsa, sistem çökmez (traceback vermez), kontrollü hata basar ve işletim sistemine çıkış kodu `1` döner. *(İlgili Testler: TC-33, TC-34, TC-35, TC-36, TC-41)*
* **UC-05 (Konsol Raporlama):** Sistem; aktif cihazları, kritik cihazları, istatistikleri ve uyarıları düzenli ve renkli/okunaklı bir formatta konsola yazdırır. *(İlgili Testler: TC-40)*
* **UC-06 (Harici API Entegrasyonu):** Sistem harici JSONPlaceholder servisinden (`/posts`) ilk 5 gönderinin başlığını güvenli bir şekilde çeker. *(İlgili Testler: TC-25...TC-31)*
* **UC-07 (Hata Toleransı ve İzolasyon):** Harici API çağrısında zaman aşımı (timeout) veya bağlantı kopması olsa bile yerel analiz raporu tam olarak sunulur ve program başarıyla `0` çıkış koduyla tamamlanır. *(İlgili Testler: TC-37, TC-39)*

---

## 3. Fonksiyonel Olmayan Gereksinimler (NFR) ve Karşılıkları

| NFR ID | Gereksinim Tanımı | Mimari / Teknik Karşılık |
| :--- | :--- | :--- |
| **NFR-01** | Python 3.11+ Uyumu | Python 3.11 özellikleriyle geliştirildi ve test edildi. |
| **NFR-02** | Kod Okunabilirliği ve Temizlik | Tip ipuçları (Type Hints), saf fonksiyonlar ve Docstring standardı uygulandı. |
| **NFR-03** | Test Edilebilirlik | İş mantığı I/O ve baskı işlemlerinden izole edildi; saf fonksiyonlar yazıldı. |
| **NFR-04** | Beklenen Hatalarda Traceback Yok | Dosya yokluğu veya bozuk JSON durumlarında kontrollü hata mesajı ve çıkış kodu `1` üretilir. |
| **NFR-05** | API Zaman Aşımı (Timeout) Tanımlı | Harici isteklerde `timeout=5.0` saniye sınırı zorunlu tutuldu. |
| **NFR-06** | Minimum Bağımlılık (KISS / YAGNI) | Yalnızca `requests` ve `pytest` paketleri kullanıldı; ek framework yüklenmedi. |
| **NFR-07** | Internetsiz Koşabilen Testler | Tüm API testleri `unittest.mock` ile izole edildi; internet bağımlılığı sıfır. |
| **NFR-08** | Net Dokümantasyon | Kurulum, çalıştırma ve iş kuralları README.md içinde detaylandırıldı. |