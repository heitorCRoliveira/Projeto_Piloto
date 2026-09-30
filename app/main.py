from flask import Flask, jsonify

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Notebook", "price": 4500.00},
    {"id": 2, "name": "Mouse", "price": 89.90},
    {"id": 3, "name": "Teclado", "price": 199.90},
]


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.get("/products")
def list_products():
    return jsonify(PRODUCTS)


@app.get("/products/<int:product_id>")
def get_product(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return jsonify(product)
    return jsonify(error="produto não encontrado"), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
