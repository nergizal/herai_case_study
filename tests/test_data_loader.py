import pytest
import json
from src.data_loader import load_devices

def test_TC32_load_devices_success(tmp_path):
    f = tmp_path / "valid.json"
    f.write_text('[{"id": 1, "status": "active"}]', encoding="utf-8")
    data = load_devices(str(f))
    assert isinstance(data, list)

def test_TC33_load_devices_not_found():
    with pytest.raises(FileNotFoundError):
        load_devices("non_existing.json")

def test_TC34_load_devices_invalid_json(tmp_path):
    """TC-34 | FR-01: Bozuk JSON dosyasında ValueError fırlatılır."""
    f = tmp_path / "invalid.json"
    f.write_text('{bozuk_json', encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        load_devices(str(f))
    assert "Geçerli bir JSON formatı değil" in str(exc.value)

def test_TC35_load_devices_not_a_list(tmp_path):
    """TC-35 | FR-01: JSON kökü liste değilse ValueError fırlatılır."""
    f = tmp_path / "dict.json"
    f.write_text('{"id": 1}', encoding="utf-8")
    with pytest.raises(ValueError) as exc:
        load_devices(str(f))
    assert "kök dizini bir liste" in str(exc.value)
    
def test_TC36_load_devices_empty_file(tmp_path):
    """TC-36 | FR-01: Boş dosyada JSON ayrıştırma hatası yönetilir."""
    f = tmp_path / "empty.json"
    f.write_text('', encoding="utf-8")
    with pytest.raises(ValueError):
        load_devices(str(f))