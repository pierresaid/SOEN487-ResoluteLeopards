from main import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utc import UtcDateTime

db = SQLAlchemy(app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    mail = db.Column(db.Text(), nullable=False, unique=True)
    pwdhash = db.Column(db.Text(), nullable=False)
    refresh_token = db.relationship('RefreshToken', backref='user', lazy=True, uselist=False)

    def __repr__(self):
        return "<User {0}: {1}>".format(self.id, self.name)


class RefreshToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    jti = db.Column(db.Text, nullable=False)
    exp = db.Column(UtcDateTime(), nullable=False)
    revoked = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<RefreshToken {0} for {1} (expires {})>".format(self.jti, self.user, self.exp)


db.create_all()