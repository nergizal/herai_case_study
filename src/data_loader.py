import json
from typing import List, Any

def load_devices(file_path: str) -> List[Any]:
    """Belirtilen dosya yolundan JSON formatındaki cihaz verilerini okur."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            if not isinstance(data, list):
                raise ValueError("Geçersiz format: JSON kök dizini bir liste (array) olmalıdır.")
                
            return data
            
    except FileNotFoundError as e:
        # Hata zincirini (stack trace) korumak için 'from e' kullanıyoruz
        raise FileNotFoundError(f"Veri dosyası bulunamadı: {file_path}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"Geçerli bir JSON formatı değil: {file_path}") from e