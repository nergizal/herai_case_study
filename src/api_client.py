import requests
from typing import List, Dict, Any

API_URL = "https://jsonplaceholder.typicode.com/posts"

def fetch_first_five_posts(url: str = API_URL, timeout: float = 5.0) -> List[Dict[str, Any]]:
    """
    Harici REST API'den veri çeker ve geçerli ilk 5 gönderiyi döndürür.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout:
        raise RuntimeError("API isteği zaman aşımına uğradı (Timeout).")
    except (requests.exceptions.JSONDecodeError, ValueError):
        raise RuntimeError("API Veri Format Hatası: Yanıt geçerli bir JSON değil.")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API Bağlantı Hatası: {str(e)}")
        
    if not isinstance(data, list):
        raise RuntimeError("API Veri Format Hatası: API yanıtı bir liste (array) yapısında değil.")
        
    valid_posts = []
    for item in data[:5]:
        if isinstance(item, dict):
            title = item.get("title")
            if isinstance(title, str) and title.strip():
                valid_posts.append({"id": item.get("id", "?"), "title": title.strip()})
                
    return valid_posts