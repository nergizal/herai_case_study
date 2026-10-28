import requests
from typing import List, Dict, Any
from src.exceptions import APICommunicationError

API_URL = "https://jsonplaceholder.typicode.com/posts"

def fetch_first_five_posts(url: str = API_URL, timeout: float = 15.0) -> List[Dict[str, Any]]:
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.Timeout as e:
        raise APICommunicationError("API isteği zaman aşımına uğradı (Timeout > 15s).") from e
    except (requests.exceptions.JSONDecodeError, ValueError) as e:
        raise APICommunicationError("API Veri Format Hatası: Yanıt geçerli bir JSON değil.") from e
    except requests.exceptions.RequestException as e:
        raise APICommunicationError(f"API Bağlantı Hatası: {str(e)}") from e
        
    if not isinstance(data, list):
        raise APICommunicationError("API Veri Format Hatası: Yanıt bir liste (array) yapısında değil.")
        
    valid_posts = []
    for item in data[:5]:
        if isinstance(item, dict):
            title = item.get("title")
            if isinstance(title, str) and title.strip():
                valid_posts.append({"id": item.get("id", "?"), "title": title.strip()})
                
    return valid_posts