from flask import request, jsonify, Blueprint
from database import db
from models.good import Goods


good_api_bp = Blueprint("good_api", __name__)


# Create a Goods
@good_api_bp.route("/api/goods", methods=["POST"])
def create_goods():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")
    if name is None or price is None or quantity is None:
        return jsonify({"message": "Name, price, and quantity are required"}), 400
    goods = Goods(name=name, price=price, quantity=quantity)
    db.session.add(goods)
    db.session.commit()
    return jsonify({"message": "Goods created successfully", "goods_id": goods.id})


# Read all Goods
@good_api_bp.route("/api/goods", methods=["GET"])
def get_goods():
    goods = Goods.query.all()
    return jsonify([{"id": g.id, "name": g.name, "price": g.price, "quantity": g.quantity} for g in goods])


# Read a specific Goods
@good_api_bp.route("/api/goods/<int:goods_id>", methods=["GET"])
def get_good(goods_id):
    goods = Goods.query.get(goods_id)
    if goods:
        return jsonify({"id": goods.id, "name": goods.name, "price": goods.price, "quantity": goods.quantity})
    else:
        return jsonify({"message": "Goods not found"}), 404


# Update a Goods
@good_api_bp.route("/api/goods/<int:goods_id>", methods=["PUT"])
def update_good(goods_id):
    goods = Goods.query.get(goods_id)
    if goods:
        data = request.get_json()
        name = data.get("name")
        price = data.get("price")
        quantity = data.get("quantity")
        if name is None or price is None or quantity is None:
            return jsonify({"message": "Name, price, and quantity are required"}), 400
        goods.name = name
        goods.price = price
        goods.quantity = quantity
        db.session.commit()
        return jsonify({"message": "Goods updated successfully"})
    else:
        return jsonify({"message": "Goods not found"}), 404


# Delete a Goods
@good_api_bp.route("/api/goods/<int:goods_id>", methods=["DELETE"])
def delete_good(goods_id):
    goods = Goods.query.get(goods_id)
    if goods:
        db.session.delete(goods)
        db.session.commit()
        return jsonify({"message": "Goods deleted successfully"})
    else:
        return jsonify({"message": "Goods not found"}), 404
