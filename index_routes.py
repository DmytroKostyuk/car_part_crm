from flask import render_template, Blueprint


index_bp = Blueprint("index", __name__)


# Render templates
@index_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")
