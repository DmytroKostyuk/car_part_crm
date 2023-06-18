from database import create_app, db
from routes.appeal_api_routes import appeal_api_bp
from routes.appeal_routes import appeal_bp
from routes.good_api_routes import good_api_bp
from routes.good_routes import good_bp
from routes.index_routes import index_bp
from routes.order_api_routes import order_api_bp
from routes.order_routes import order_bp
from routes.task_api_routes import task_api_bp
from routes.task_routes import task_bp
from routes.user_api_routes import user_api_bp
from routes.user_routes import user_bp

app = create_app()

app.register_blueprint(appeal_api_bp)
app.register_blueprint(appeal_bp)
app.register_blueprint(good_api_bp)
app.register_blueprint(good_bp)
app.register_blueprint(index_bp)
app.register_blueprint(order_api_bp)
app.register_blueprint(order_bp)
app.register_blueprint(task_api_bp)
app.register_blueprint(task_bp)
app.register_blueprint(user_api_bp)
app.register_blueprint(user_bp)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
