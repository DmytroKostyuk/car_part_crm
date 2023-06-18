from flask import request, jsonify, Blueprint
from database import db
from models.order import Order, OrderItem
from models.good import Goods


order_api_bp = Blueprint("oreder_api", __name__)


# Create an Order
@order_api_bp.route("/api/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    if user_id is None:
        return jsonify({"message": "User ID is required"}), 400
    order = Order(user_id=user_id, status="Pending")
    db.session.add(order)
    for item in data["items"]:
        goods_id = item.get("goods_id")
        quantity = item.get("quantity")
        if goods_id is None or quantity is None:
            return jsonify({"message": "Goods ID and quantity are required for each item"}), 400
        goods = Goods.query.get(goods_id)
        if goods is None:
            return jsonify({"message": f"Goods with ID {goods_id} not found"}), 404
        order_item = OrderItem(order=order, goods_id=goods_id, quantity=quantity)
        db.session.add(order_item)
    db.session.commit()
    return jsonify({"message": "Order created successfully", "order_id": order.id})


# Read all Orders
@order_api_bp.route("/api/orders", methods=["GET"])
def get_orders():
    orders = Order.query.all()
    return jsonify([{"id": o.id, "status": o.status, "user_id": o.user_id} for o in orders])


# Read a specific Order
@order_api_bp.route("/api/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order:
        order_data = {
            "id": order.id,
            "status": order.status,
            "user_id": order.user_id,
            "items": [{"goods_id": item.goods_id, "quantity": item.quantity} for item in order.items],
        }
        return jsonify(order_data)
    else:
        return jsonify({"message": "Order not found"}), 404


# Update an Order
@order_api_bp.route("/api/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    order = Order.query.get(order_id)
    if order:
        data = request.get_json()
        status = data.get("status")
        if status is None:
            return jsonify({"message": "Status is required"}), 400
        order.status = status
        db.session.commit()
        return jsonify({"message": "Order updated successfully"})
    else:
        return jsonify({"message": "Order not found"}), 404


# Delete an Order
@order_api_bp.route("/api/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        OrderItem.query.filter_by(order_id=order_id).delete()

        db.session.delete(order)
        db.session.commit()
        return jsonify({"message": "Order and associated items deleted successfully"})
    else:
        return jsonify({"message": "Order not found"}), 404
