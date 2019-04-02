from sqlalchemy import ForeignKey

from main import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    mail = db.Column(db.Text(), nullable=False, unique=True)
    pwdhash = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<User {0}: {1}>".format(self.id, self.name)


db.create_all()
