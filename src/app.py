from flask import Flask, request, jsonify
import db

### Order Service ###

app = Flask(__name__)


@app.route("/health")
def health():
    try:
        conn = db.get_db_connection()
        conn.close()
        return {"status": "healthy"}, 200
    except Exception as e:
        return {"error": str(e)}, 503


@app.route("/orders", methods=["GET", "POST"])
def index():
    # get all orders
    if request.method == "GET":
        query = "SELECT * FROM orders;"
        try:
            result = db.read_from_db(query)
            keys = ["id", "product_id", "quantity", "total_price"]
            return jsonify([dict(zip(keys, row)) for row in result]), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    # create orders
    else:
        product_id = request.json["product_id"]
        quantity = request.json["quantity"]
        total_price = request.json["total_price"]

        query = "INSERT INTO orders (product_id, quantity, total_price, status) VALUES (%s, %s, %s, %s)"
        params = (product_id, quantity, total_price, "Order Received")
        try:
            db.write_to_db(query, params)
            return jsonify({"message": "Your order was successfully logged!"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route("/orders/<int:id>", methods=["GET"])
def read_singleton(id):
    query = "SELECT * FROM orders WHERE id = %s;"
    params = (id,)
    try:
        result = db.read_from_db(query, params)
        keys = ["id", "item", "quantity", "price"]
        return jsonify([dict(zip(keys, row)) for row in result]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# consider implementing delete function later


@app.route("/orders/<int:id>", methods=["PUT"])
def update_status(id):
    status = request.json["status"]

    # schema: id, product_id, quantity, total_price, status
    query = "UPDATE orders SET status = %s WHERE id = %s"
    params = (status, id)
    try:
        db.write_to_db(query, params)
        return jsonify(
            {"message": f"Status for order {id} was updated successfully!"}
        ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
