import pytest
from src.validator import validate_devices

VALID_RECORD = {"id": 1, "device_name": "Kamera-A", "status": "active", "threat_score": 85}

def make_record(**overrides):
    """Geçerli bir kaydın kopyasını, verilen alanlar değiştirilmiş olarak döndürür."""
    record = dict(VALID_RECORD)
    record.update(overrides)
    return record

def test_TC11_valid_records_pass_through_in_order():
    """TC-11 | FR-02 / AC-02-1: Geçerli kayıtlar değişmeden ve sırayla geçer, uyarı yok."""
    records = [make_record(id=1), make_record(id=2, status="inactive")]
    valid, warnings = validate_devices(records)
    assert valid == records
    assert warnings == []

def test_TC12_missing_field_is_skipped_with_warning():
    """TC-12 | FR-02 / AC-02-1: Alanı eksik kayıt atlanır, uyarı id'yi içerir."""
    broken = {"id": 3, "device_name": "Kamera-C", "status": "active"}
    valid, warnings = validate_devices([VALID_RECORD, broken])
    assert valid == [VALID_RECORD]
    assert len(warnings) == 1
    assert "id=3" in warnings[0]
    assert "threat_score" in warnings[0]

@pytest.mark.parametrize(
    "bad_score",
    ["85", "seksen", None, True, False, [85], float("nan"), float("inf")],
    ids=["str-sayi", "str-metin", "none", "bool-true", "bool-false", "liste", "nan", "inf"],
)
def test_TC13_invalid_score_type_is_skipped(bad_score):
    """TC-13 | FR-02 / AC-02-2: Sayı olmayan (veya bool/NaN/inf) skor atlanır."""
    valid, warnings = validate_devices([make_record(threat_score=bad_score)])
    assert valid == []
    assert len(warnings) == 1

@pytest.mark.parametrize(
    "bad_status",
    ["Active", "ACTIVE", "unknown", "", None, ["active"]],
    ids=["buyuk-A", "hepsi-buyuk", "bilinmeyen", "bos", "none", "liste"],
)
def test_TC14_invalid_status_is_skipped(bad_status):
    """TC-14 | FR-02 / AC-02-3: 'active'/'inactive' dışındaki status atlanır."""
    valid, warnings = validate_devices([make_record(status=bad_status)])
    assert valid == []
    assert len(warnings) == 1

@pytest.mark.parametrize("not_a_dict", ["metin", 42, None, [1, 2]])
def test_TC15_non_dict_record_is_skipped(not_a_dict):
    """TC-15 | FR-02: Sözlük olmayan kayıt atlanır, program çökmez."""
    valid, warnings = validate_devices([not_a_dict])
    assert valid == []
    assert len(warnings) == 1

@pytest.mark.parametrize("bad_name", ["", "   ", None, 123])
def test_TC16_invalid_device_name_is_skipped(bad_name):
    """TC-16 | FR-02: Boş veya metin olmayan device_name atlanır."""
    valid, warnings = validate_devices([make_record(device_name=bad_name)])
    assert valid == []
    assert len(warnings) == 1

def test_TC17_mixed_data_keeps_valid_and_warns_for_each_invalid():
    """TC-17 | FR-02 / AC-02-1: Karışık veride geçerliler korunur, her geçersiz için bir uyarı."""
    records = [make_record(id=1), make_record(id=2, threat_score="x"), make_record(id=3), "bozuk"]
    valid, warnings = validate_devices(records)
    assert [d["id"] for d in valid] == [1, 3]
    assert len(warnings) == 2

def test_TC18_empty_list_returns_empty_results():
    """TC-18 | FR-02: Boş liste hata değildir; boş sonuç döner."""
    assert validate_devices([]) == ([], [])

@pytest.mark.parametrize("score", [0, 50, 100, 100.5, -5, 250], ids=str)
def test_TC19_any_finite_number_is_valid_no_range_check(score):
    """TC-19 | FR-02: Karar V8-A: aralık kontrolü yok, sonlu her sayı geçerli (int ve float)."""
    valid, warnings = validate_devices([make_record(threat_score=score)])
    assert len(valid) == 1
    assert warnings == []