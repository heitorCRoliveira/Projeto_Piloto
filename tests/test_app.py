import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from main import app  # noqa: E402

client = app.test_client()


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json() == {"status": "ok"}


def test_list_products():
    r = client.get("/products")
    assert r.status_code == 200
    assert len(r.get_json()) == 3


def test_get_product():
    r = client.get("/products/1")
    assert r.status_code == 200
    assert r.get_json()["name"] == "Notebook"


def test_product_not_found():
    r = client.get("/products/999")
    assert r.status_code == 404
