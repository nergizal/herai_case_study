import pytest
from unittest.mock import patch
from main import main

def test_TC37_main_success_exit_code_zero():
    """TC-37 | UC-03: Başarılı analizde çıkış kodu 0 olmalıdır (API mock'lı, internet gerekmez)."""
    with patch('main.load_devices', return_value=[]), \
         patch('main.fetch_first_five_posts', return_value=[]):
        assert main(["main.py", "dummy.json"]) == 0

def test_TC41_main_invalid_json_exit_code_one(tmp_path, capsys):
    """TC-41 | FR-01 (AC-01-3): Bozuk JSON'da traceback yok, hata stderr'e yazılır, çıkış kodu 1."""
    f = tmp_path / "bad.json"
    f.write_text("{bozuk", encoding="utf-8")
    with patch('main.fetch_first_five_posts', return_value=[]):
        assert main(["main.py", str(f)]) == 1
    assert "Kritik Hata" in capsys.readouterr().err

def test_TC38_main_file_not_found_exit_code_one():
    """TC-38 | UC-03: Dosya bulunamadığında hata basılıp çıkış kodu 1 dönmelidir."""
    assert main(["main.py", "invalid_path_12345.json"]) == 1

def test_TC39_main_api_failure_still_zero_exit_code():
    """TC-39 | FR-08: API çökse bile yerel analiz başarılıysa çıkış kodu 0 olmalıdır."""
    with patch('main.load_devices', return_value=[]), \
         patch('main.fetch_first_five_posts', side_effect=RuntimeError("API Error")):
        assert main(["main.py", "dummy.json"]) == 0

def test_TC40_presenter_output_format(capsys):
    """TC-40 | FR-06: Presenter konsol çıktısı doğru formatlanmalıdır."""
    from src.presenter import display_local_analysis
    display_local_analysis(
        active_devices=[{"id": 1, "device_name": "Test", "threat_score": 60}],
        critical_devices=[{"id": 1, "device_name": "Test", "threat_score": 60}],
        average_score=60.0
    )
    captured = capsys.readouterr()
    assert "HERAI STUDIOS - CIHAZ ANALIZ RAPORU" in captured.out
    assert "[KRİTİK]" in captured.out
    assert "60.00" in captured.out