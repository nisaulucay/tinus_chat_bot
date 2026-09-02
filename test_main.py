from fastapi.testclient import TestClient
from app.main import app

# FastAPI uygulaması için test istemcisi oluştur
client = TestClient(app)

def test_read_main():
    # Kök dizine (/) istek atıldığında arayüzün HTTP 200 döndüğünü test et
    response = client.get("/")
    assert response.status_code == 200

def test_ask_endpoint():
    # /api/v1/ask adresine örnek bir soru gönderildiğinde HTTP 200 döndüğünü test et
    response = client.post(
        "/api/v1/ask",
        json={"session_id": "test-oturum-123", "query": "FEA nedir?"}
    )
    assert response.status_code == 200