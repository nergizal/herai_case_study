import time
from src.validator import validate_devices
from src.analyzer import run_device_analysis_pipeline

def test_fuzzing_and_malicious_payloads():
    malicious_data = [
        {"id": 101, "device_name": "<script>alert('xss')</script>", "status": "active", "threat_score": 50},
        {"id": -10, "device_name": "NegativeID", "status": "active", "threat_score": 30},
        {"id": 4, "device_name": "ValidDevice", "status": "active", "threat_score": 80},
        {"id": 4, "device_name": "DuplicateID", "status": "active", "threat_score": 70},
        {"id": 2, "device_name": "InvalidStatus", "status": "unknown", "threat_score": 20},
        {"id": 3, "device_name": "InvalidScoreType", "status": "active", "threat_score": "metin_skor"}
    ]
    
    valid_devices, warnings = validate_devices(malicious_data)
    assert len(valid_devices) == 1
    assert valid_devices[0]["device_name"] == "ValidDevice"
    assert len(warnings) == 5

def test_performance_stress_10k_records():
    stress_data = [
        {"id": i, "device_name": f"Device-{i}", "status": "active" if i % 2 == 0 else "inactive", "threat_score": i % 101}
        for i in range(1, 10001)
    ]
    
    start_time = time.time()
    result = run_device_analysis_pipeline(stress_data)
    duration = time.time() - start_time
    
    assert len(result["valid_devices"]) == 10000
    assert duration < 1.0