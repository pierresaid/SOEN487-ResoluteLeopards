from sqlalchemy import ForeignKey

from main import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<User {0}: {1}>".format(self.id, self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    # url_one = db.Column(db.Text())
    # url_two = db.Column(db.Text())

    def __repr__(self):
        return "<Post {0}: {1}>".format(self.id, self.title)


class Vote(db.Model):
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False, primary_key=True)
    post_id = db.Column(db.Integer, ForeignKey("post.id"), nullable=False, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Vote {0} {1}: {2}>".format(self.user_id, self.post_id, self.value)


db.create_all()
