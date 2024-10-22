import json

from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_list_product():
    response = client.get("/product")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_add_product():
    response = client.post("/product", data = {'name':'test', 'price':'111', 'category':'test'})
    assert response.status_code == 200
    assert response.json() == {"message": "Product saved successfully"}

def test_show_product():
    response = client.get("/product/?name=rtrg")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_category_product():
    response = client.get("/product/category/m")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_filtering_product():
    response = client.get("/product/filtering/200&300")
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_update_product():
    response = client.put("/product/rtrg", params={'price': 111, 'category': 'test1'})
    print(response)
    assert response.status_code == 200
    assert type(response.json()) == dict

def test_delete_product():
    response = client.delete("/product/test")
    print(response)
    assert response.status_code == 200
    assert type(response.json()) == dict

