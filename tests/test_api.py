from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_upload_file():
    response = client.post("/upload/", files={"file": ("test.json", b'[{"name": "Test", "email": "test@example.com", "age": 30}]')})
    assert response.status_code == 200
    assert "id" in response.json()