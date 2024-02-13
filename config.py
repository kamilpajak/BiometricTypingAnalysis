# config.py
def configure_app(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
