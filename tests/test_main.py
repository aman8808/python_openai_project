from fastapi.testclient import TestClient
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app

client = TestClient(app)

def test_generate_response():
    response = client.post("/generate-response/", json={"query": "Какова погода сегодня?"})
    assert response.status_code == 200
    response_data = response.json()
    assert "query_id" in response_data
    assert "response" in response_data

def test_add_vector():
    vector_data = {
        "vector": np.random.rand(300).tolist(),
        "metadata": {"key": "value"}
    }
    response = client.post("/vectors/", json=vector_data)
    assert response.status_code == 200
    response_data = response.json()
    assert "id" in response_data
    assert response_data["id"] == 1

def test_list_vectors():
    response = client.get("/vectors/")
    assert response.status_code == 200
    response_data = response.json()
    assert "vectors" in response_data
    assert isinstance(response_data["vectors"], list)
    # Проверка структуры возвращаемых данных
    if response_data["vectors"]:
        assert isinstance(response_data["vectors"], list)
