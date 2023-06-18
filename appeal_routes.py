from flask import jsonify, render_template, Blueprint
from models.appeal import Appeal


appeal_bp = Blueprint("appeal", __name__)


@appeal_bp.route("/appeals", methods=["GET"])
def appeals():
    appeals = Appeal.query.all()
    return render_template("appeals.html", appeals=appeals)


@appeal_bp.route("/appeals/<int:appeal_id>", methods=["GET"])
def appeal(appeal_id):
    appeal = Appeal.query.get(appeal_id)
    if appeal:
        return render_template("appeal.html", appeal=appeal)
    else:
        return jsonify({"message": "appeal not found"}), 404
