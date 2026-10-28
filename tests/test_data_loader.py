import json
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from src.exceptions import FileFormatError, SchemaValidationError

def load_devices(file_path: str) -> List[Dict[str, Any]]:
    path = Path(file_path)
    if not path.exists():
        raise FileFormatError(f"Veri dosyası bulunamadı: {file_path}")
    
    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif suffix in [".xlsx", ".xls"]:
            df = pd.read_excel(path)
            data = df.to_dict(orient="records")
        elif suffix == ".csv":
            df = pd.read_csv(path)
            data = df.to_dict(orient="records")
        else:
            raise FileFormatError(f"Desteklenmeyen dosya formatı: {suffix}")
            
        if not isinstance(data, list):
            raise SchemaValidationError("Veri kök yapısı bir liste (array/records) formatında olmalıdır.")
        return data
    except (json.JSONDecodeError, ValueError) as e:
        raise FileFormatError(f"Geçersiz dosya içeriği veya şema hatası: {str(e)}") from e
    except Exception as e:
        if isinstance(e, DeviceAnalysisError):
            raise e
        raise FileFormatError(f"Dosya işlenirken beklenmeyen hata: {str(e)}") from e