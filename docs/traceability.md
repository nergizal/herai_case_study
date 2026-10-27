# İzlenebilirlik Matrisi (Traceability Matrix)

| Gereksinim (FR) | Kabul Kriteri (AC) | Use Case (UC) | İlgili Test Senaryoları (TC) | Kod Modülü |
| :--- | :--- | :--- | :--- | :--- |
| **FR-01:** JSON dosyasını oku | AC-01-1, 01-2, 01-3 | UC-01, UC-03 | TC-32, TC-33, TC-34, TC-35, TC-36, TC-38, **TC-41** | `data_loader.py`, `main.py` |
| **FR-02:** Kayıtları doğrula, geçersizi atla | AC-02-1, 02-2, 02-3 | UC-01 (A1) | TC-11...TC-19, TC-21 | `validator.py` |
| **FR-03:** Yalnızca 'active' olanları al | AC-03-1 | UC-01 | TC-20 (Resmi Veri Testi) | `analyzer.py` |
| **FR-04:** threat_score >= 50 kritik | AC-04-1, 04-2, 04-3 | UC-01 | TC-22, TC-23 | `analyzer.py` |
| **FR-05:** Aktif cihaz ortalaması | AC-05-1, 05-2 | UC-01 (A2, A3) | TC-20, TC-24, **TC-42** | `analyzer.py` |
| **FR-06:** Sonuçları okunaklı yazdır | AC-06-1 | UC-01 | TC-40 | `presenter.py` |
| **FR-07:** API'den ilk 5 başlığı çek | AC-07-1, 07-2, 07-3, 07-4 | UC-02 | TC-25, TC-26, TC-27, TC-28, TC-29, TC-30, TC-31 | `api_client.py` |
| **FR-08:** API düşse de yerel analiz çalışır | AC-08-1 | UC-03 (Alt Akış) | TC-37, TC-39 | `main.py` |