import pytest
from unittest.mock import patch, MagicMock
import requests
from src.api_client import fetch_first_five_posts

@patch("src.api_client.requests.get")
def test_TC25_fetch_first_five_posts_success(mock_get):
    """TC-25 | FR-07: Geçerli API yanıtından tam olarak ilk 5 başlığın alınması."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = [{"id": i, "title": f"Title {i}"} for i in range(1, 10)]
    mock_get.return_value = mock_resp

    posts = fetch_first_five_posts()
    assert len(posts) == 5
    assert posts[0]["title"] == "Title 1"
    assert posts[4]["title"] == "Title 5"

@patch("src.api_client.requests.get")
def test_TC26_timeout_error(mock_get):
    """TC-26 | FR-07 (AC-07-3): Zaman aşımının RuntimeError'a dönüştürülmesi."""
    mock_get.side_effect = requests.exceptions.Timeout("Zaman aşımı")
    with pytest.raises(RuntimeError) as exc_info:
        fetch_first_five_posts()
    assert "zaman aşımına" in str(exc_info.value)

@patch("src.api_client.requests.get")
def test_TC27_connection_or_http_error(mock_get):
    """TC-27 | FR-07 (AC-07-3): Bağlantı/HTTP hatalarının RuntimeError'a dönüştürülmesi."""
    mock_get.side_effect = requests.exceptions.ConnectionError("Bağlantı koptu")
    with pytest.raises(RuntimeError) as exc_info:
        fetch_first_five_posts()
    assert "API Bağlantı Hatası" in str(exc_info.value)

@patch("src.api_client.requests.get")
def test_TC28_non_json_response(mock_get):
    """TC-28 | FR-07 (AC-07-3): API'den JSON yerine metin/HTML geldiğinde güvenli hata."""
    mock_resp = MagicMock()
    mock_resp.json.side_effect = requests.exceptions.JSONDecodeError("Expecting value", "<html>", 0)
    mock_get.return_value = mock_resp
    with pytest.raises(RuntimeError) as exc_info:
        fetch_first_five_posts()
    assert "geçerli bir JSON değil" in str(exc_info.value)

@patch("src.api_client.requests.get")
def test_TC29_non_list_response(mock_get):
    """TC-29 | FR-07 (AC-07-3): JSON kökü liste değilse RuntimeError fırlatılması."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"error": "Not a list"}
    mock_get.return_value = mock_resp

    with pytest.raises(RuntimeError) as exc_info:
        fetch_first_five_posts()
    assert "liste (array) yapısında değil" in str(exc_info.value)

@patch("src.api_client.requests.get")
def test_TC30_empty_list_and_less_than_five(mock_get):
    """TC-30 | FR-07: API'de 5'ten az (veya sıfır) kayıt varsa güvenli çalışma."""
    mock_resp = MagicMock()
    
    # 1 kayıt senaryosu
    mock_resp.json.return_value = [{"id": 1, "title": "Only One"}]
    mock_get.return_value = mock_resp
    assert len(fetch_first_five_posts()) == 1

    # Boş liste senaryosu
    mock_resp.json.return_value = []
    assert len(fetch_first_five_posts()) == 0

@patch("src.api_client.requests.get")
def test_TC31_skip_invalid_items(mock_get):
    """TC-31 | FR-07 (AC-07-4): İlk 5 içindeki dict olmayan veya title'ı bozuk kayıtların atlanması."""
    mock_resp = MagicMock()
    # 1. Geçerli, 2. Dict değil, 3. Title yok, 4. Title boş string, 5. Geçerli
    mock_resp.json.return_value = [
        {"id": 1, "title": "Valid 1"},
        "I am a string, not a dict",
        {"id": 3, "body": "No title here"},
        {"id": 4, "title": "   "},
        {"id": 5, "title": "Valid 2"},
        {"id": 6, "title": "6th won't be checked"}
    ]
    mock_get.return_value = mock_resp

    posts = fetch_first_five_posts()
    
    # 5 kayıttan 3 tanesi bozuk olduğu için atlanır, geriye ilk 5 içindeki 2 geçerli kayıt kalır.
    assert len(posts) == 2
    assert posts[0]["title"] == "Valid 1"
    assert posts[1]["title"] == "Valid 2"