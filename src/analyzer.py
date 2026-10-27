from typing import List, Dict, Any, Optional
from src.validator import validate_devices

CRITICAL_THRESHOLD = 50

def filter_active_devices(devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Yalnızca durumu 'active' olan cihazları filtreler."""
    return [device for device in devices if device["status"] == "active"]

def identify_critical_devices(active_devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Aktif cihazlar arasından threat_score >= CRITICAL_THRESHOLD olanları seçer."""
    return [device for device in active_devices if device["threat_score"] >= CRITICAL_THRESHOLD]

def calculate_average_threat_score(active_devices: List[Dict[str, Any]]) -> Optional[float]:
    """Aktif cihazların ortalama tehdit skorunu hesaplar; aktif cihaz yoksa None."""
    if not active_devices:
        return None
    total_score = sum(device["threat_score"] for device in active_devices)
    return total_score / len(active_devices)

def run_device_analysis_pipeline(raw_devices: List[Any]) -> Dict[str, Any]:
    """Hem CLI hem de olası dış katmanların çağıracağı ana analiz boru hattı."""
    valid_devices, warnings = validate_devices(raw_devices)
    active_devices = filter_active_devices(valid_devices)
    critical_devices = identify_critical_devices(active_devices)
    avg_score = calculate_average_threat_score(active_devices)

    return {
        "raw_count": len(raw_devices),
        "valid_count": len(valid_devices),
        "active_devices": active_devices,
        "critical_devices": critical_devices,
        "avg_score": avg_score,
        "warnings": warnings,
    }