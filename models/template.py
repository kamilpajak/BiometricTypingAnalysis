# template.py

from database import db


class Template(db.Model):
    __tablename__ = "templates"
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), nullable=False)
    mean_press_press = db.Column(db.Float, nullable=False)
    std_dev_press_press = db.Column(db.Float, nullable=False)
    mean_press_release = db.Column(db.Float, nullable=False)
    std_dev_press_release = db.Column(db.Float, nullable=False)
    mean_release_press = db.Column(db.Float, nullable=False)
    std_dev_release_press = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(
        self,
        key,
        mean_press_press,
        std_dev_press_press,
        mean_press_release,
        std_dev_press_release,
        mean_release_press,
        std_dev_release_press,
        user_id,
    ):
        self.key = key
        self.mean_press_press = mean_press_press
        self.std_dev_press_press = std_dev_press_press
        self.mean_press_release = mean_press_release
        self.std_dev_press_release = std_dev_press_release
        self.mean_release_press = mean_release_press
        self.std_dev_release_press = std_dev_release_press
        self.user_id = user_id

    def __repr__(self):
        return f"<Template(key='{self.key}', user_id='{self.user_id}')>"
