from typing import List, Dict, Any, Optional
from src.validator import validate_devices

CRITICAL_THRESHOLD = 50

def filter_active_devices(devices: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [d for d in devices if d.get("status") == "active"]

def identify_critical_devices(active_devices: List[Dict[str, Any]], threshold: int = CRITICAL_THRESHOLD) -> List[Dict[str, Any]]:
    return [d for d in active_devices if isinstance(d.get("threat_score"), (int, float)) and d.get("threat_score") >= threshold]

def calculate_average_threat_score(active_devices: List[Dict[str, Any]]) -> Optional[float]:
    if not active_devices:
        return None
    valid_scores = [d.get("threat_score") for d in active_devices if isinstance(d.get("threat_score"), (int, float))]
    if not valid_scores:
        return None
    return round(sum(valid_scores) / len(valid_scores), 2)

def run_device_analysis_pipeline(raw_records: List[Any]) -> Dict[str, Any]:
    valid_devices, warnings = validate_devices(raw_records)
    active_devices = filter_active_devices(valid_devices)
    critical_devices = identify_critical_devices(active_devices)
    avg_score = calculate_average_threat_score(active_devices)
    
    return {
        "valid_devices": valid_devices,
        "valid_count": len(valid_devices),
        "active_devices": active_devices,
        "critical_devices": critical_devices,
        "avg_score": avg_score,
        "warnings": warnings
    }