import json
from pathlib import Path
from typing import List, Dict, Any
from src.exceptions import FileFormatError

def load_devices(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileFormatError(f"Veri dosyası bulunamadı: {file_path}")
    
    suffix = path.suffix.lower()
    if suffix != ".json":
        raise FileFormatError(f"Desteklenmeyen dosya formatı: {suffix}. Yalnızca .json desteklenmektedir.")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not isinstance(data, list):
            raise FileFormatError("Veri kök yapısı bir liste (array) formatında olmalıdır.")
        return data
        
    except (json.JSONDecodeError, ValueError) as e:
        raise FileFormatError(f"Geçersiz JSON formatı veya bozuk dosya içeriği: {str(e)}") from e
    except Exception as e:
        if isinstance(e, FileFormatError):
            raise e
        raise FileFormatError(f"Dosya okunurken beklenmeyen hata: {str(e)}") from e