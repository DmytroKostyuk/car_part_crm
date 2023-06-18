from flask import jsonify, render_template, Blueprint
from models.order import Order
from models.good import Goods


order_bp = Blueprint("order", __name__)


@order_bp.route("/orders", methods=["GET"])
def orders():
    goods = Goods.query.all()
    goods_list = [{"id": good.id, "name": good.name} for good in goods]
    orders = Order.query.all()
    return render_template("orders.html", orders=orders, goods=goods_list)


@order_bp.route("/orders/<int:order_id>", methods=["GET"])
def order(order_id):
    order = Order.query.get(order_id)
    goods = Goods.query.all()
    goods_list = [{"id": good.id, "name": good.name} for good in goods]
    if order:
        return render_template("order.html", order=order, goods=goods_list)
    else:
        return jsonify({"message": "Order not found"}), 404
