from typing import List, Dict, Any, Tuple
import math
import re

def validate_device_record(record: Any, seen_ids: set) -> Tuple[bool, str]:
    if not isinstance(record, dict):
        return False, "Kayıt bir sözlük  yapısında değil."
    
    required_keys = ["id", "device_name", "status", "threat_score"]
    for key in required_keys:
        if key not in record:
            return False, f"Zorunlu alan eksik: '{key}'"
            
    dev_id = record.get("id")
    if isinstance(dev_id, int) and dev_id <= 0:
        return False, f"Geçersiz 'id' (0 veya negatif olamaz): {dev_id}"
    if not isinstance(dev_id, (int, str)):
        return False, "Geçersiz 'id' tipi."
        
    if dev_id in seen_ids:
        return False, f"Duplicate ID tespit edildi: {dev_id}"
        
    name = record.get("device_name")
    if not isinstance(name, str) or not name.strip():
        return False, f"Geçersiz veya boş 'device_name': {name!r}"
    if re.search(r"[<>]", name):
        return False, f"Zararlı karakter içeren 'device_name' reddedildi: {name!r}"
        
    status = record.get("status")
    if status not in ["active", "inactive"]:
        return False, f"Geçersiz 'status' değeri: {status!r}"
        
    score = record.get("threat_score")
    if isinstance(score, bool) or not isinstance(score, (int, float)) or math.isnan(score) or math.isinf(score):
        return False, f"'threat_score' sayısal olmalı, gelen: {score!r}"
        
    return True, ""

def validate_devices(raw_records: List[Any]) -> Tuple[List[Dict[str, Any]], List[str]]:
    valid_devices = []
    warnings = []
    seen_ids = set()
    
    for index, record in enumerate(raw_records):
        is_valid, err_msg = validate_device_record(record, seen_ids)
        if is_valid:
            valid_devices.append(record)
            seen_ids.add(record.get("id"))
        else:
            rec_id = record.get("id", "N/A") if isinstance(record, dict) else "N/A"
            warnings.append(f"Kayıt indeks {index} (id={rec_id}) reddedildi: {err_msg}")
            
    return valid_devices, warnings