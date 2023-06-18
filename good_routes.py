from flask import jsonify, render_template, Blueprint
from models.good import Goods


good_bp = Blueprint("good", __name__)


@good_bp.route("/goods", methods=["GET"])
def goods():
    goods = Goods.query.all()
    return render_template("goods.html", goods=goods)


@good_bp.route("/goods/<int:goods_id>", methods=["GET"])
def good(goods_id):
    goods = Goods.query.get(goods_id)
    if goods:
        return render_template("good.html", goods=goods)
    else:
        return jsonify({"message": "Goods not found"}), 404
