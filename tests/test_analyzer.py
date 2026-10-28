import pytest
from src.analyzer import (
    filter_active_devices,
    identify_critical_devices,
    calculate_average_threat_score,
    run_device_analysis_pipeline
)

def test_TC20_case_study_official_sample_data():
    """TC-20 | FR-05: Case Study'nin resmi örnek verisinde tam olarak 73.33 ortalamasını doğrulayan test."""
    official_data = [
        {"id": 1, "device_name": "Kamera-A", "status": "active", "threat_score": 85},
        {"id": 2, "device_name": "Kamera-B", "status": "inactive", "threat_score": 20},
        {"id": 3, "device_name": "Kamera-C", "status": "active", "threat_score": 45},
        {"id": 4, "device_name": "Kamera-D", "status": "active", "threat_score": 90}
    ]
    res = run_device_analysis_pipeline(official_data)
    assert len(res["warnings"]) == 0
    assert len(res["active_devices"]) == 3
    assert len(res["critical_devices"]) == 2
    assert res["avg_score"] == pytest.approx(73.3333, rel=1e-3)

@pytest.mark.parametrize(
    "bad_record",
    [
        {"id": 2, "device_name": "Cam", "status": "active"}, 
        {"id": 2, "device_name": "Cam", "status": "active", "threat_score": None}, 
        {"id": 2, "device_name": "Cam", "status": "active", "threat_score": True}, 
        {"id": 2, "device_name": "Cam", "status": "active", "threat_score": "seksen"}, 
        {"id": 2, "device_name": "Cam", "status": "active", "threat_score": float("nan")}, 
        {"id": 2, "device_name": "Cam"},
        {"id": 2, "device_name": "Cam", "status": "Active", "threat_score": 90}, 
    ],
    ids=["eksik-skor", "null-skor", "bool-skor", "metin-skor", "nan-skor", "eksik-status", "buyuk-harf-status"]
)
def test_TC21_pipeline_resilience_to_bad_data(bad_record):
    """TC-21 | FR-02: Pipeline seviyesinde bozuk verilerin çökmeye yol açmadığı ve uyarı ürettiği doğrulanır."""
    valid_record = {"id": 1, "device_name": "Valid-Cam", "status": "active", "threat_score": 80}
    raw_data = [valid_record, bad_record]
    
    res = run_device_analysis_pipeline(raw_data)
    
    assert res["valid_count"] == 1
    assert len(res["warnings"]) == 1
    assert res["avg_score"] == 80.0

def test_TC22_passive_high_score_not_critical():
    """TC-22 | FR-04: Pasif cihazın skoru yüksek olsa dahi kritik olmamalıdır."""
    data = [{"id": 1, "device_name": "Cam", "status": "inactive", "threat_score": 99}]
    res = run_device_analysis_pipeline(data)
    assert len(res["critical_devices"]) == 0

def test_TC23_critical_devices_boundary():
    """TC-23 | FR-04 & FR-05: Sınır değer 50 kritik, 49 normal kabul edilmeli, ortalama 49.5 olmalı."""
    data = [
        {"id": 1, "device_name": "Cam1", "status": "active", "threat_score": 50},
        {"id": 2, "device_name": "Cam2", "status": "active", "threat_score": 49}
    ]
    res = run_device_analysis_pipeline(data)
    assert len(res["critical_devices"]) == 1
    assert res["critical_devices"][0]["id"] == 1
    assert res["avg_score"] == 49.5

def test_TC24_average_empty_list():
    """TC-24 | FR-05: Aktif cihaz yoksa ortalama None dönmeli, ZeroDivisionError olmamalı."""
    res = run_device_analysis_pipeline([])
    assert res["avg_score"] is None

def test_TC42_all_devices_inactive_no_average():
    """TC-42 | FR-05 (AC-05-2): Cihazlar var ama hiçbiri aktif değilse ortalama None, kritik yok."""
    data = [{"id": 1, "device_name": "Cam", "status": "inactive", "threat_score": 90}]
    res = run_device_analysis_pipeline(data)
    assert res["valid_count"] == 1
    assert res["active_devices"] == []
    assert res["critical_devices"] == []
    assert res["avg_score"] is None