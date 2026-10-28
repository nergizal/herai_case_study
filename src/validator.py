"""Cihaz kayıtlarının doğrulanması (FR-02)."""
import math
from typing import Any, Dict, List, Optional, Tuple

REQUIRED_FIELDS = ("id", "device_name", "status", "threat_score")
VALID_STATUSES = frozenset({"active", "inactive"})

def find_record_problem(record: Any) -> Optional[str]:
    """Kayıt geçersizse sebebini, geçerliyse None döndürür."""
    if not isinstance(record, dict):
        return "kayıt bir nesne değil"
        
    for field in REQUIRED_FIELDS:
        if field not in record:
            return f"'{field}' alanı eksik"
            
    device_name = record["device_name"]
    if not isinstance(device_name, str) or not device_name.strip():
        return "'device_name' boş olmayan bir metin olmalı"
        
    status = record["status"]
    if not isinstance(status, str) or status not in VALID_STATUSES:
        return f"'status' geçersiz: {status!r}"
        
    score = record["threat_score"]
    
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        return f"'threat_score' sayı olmalı, gelen: {score!r}"
        
    if not math.isfinite(score):
        return f"'threat_score' sonlu bir sayı olmalı, gelen: {score!r}"
        
    return None

def _record_label(index: int, record: Any) -> str:
    if isinstance(record, dict) and "id" in record:
        return f"{index}. kayıt (id={record['id']})"
    return f"{index}. kayıt"

def validate_devices(records: List[Any]) -> Tuple[List[Dict[str, Any]], List[str]]:
    """Kayıtları doğrular, geçerli kayıtlar, uyarı mesajlarını döndürür.
    Geçersiz kayıtlar atlanır ve her biri için bir uyarı üretilir.
    Geçerli kayıtların sırası korunur.
    """
    valid_devices: List[Dict[str, Any]] = []
    warnings: List[str] = []
    
    for index, record in enumerate(records, start=1):
        problem = find_record_problem(record)
        if problem is None:
            valid_devices.append(record)
        else:
            warnings.append(f"{_record_label(index, record)} atlandı: {problem}")
            
    return valid_devices, warnings