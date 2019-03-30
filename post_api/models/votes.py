from models import db


class Vote(db.Model):
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Vote {0} {1}: {2}>".format(self.user_id, self.post_id, self.value)

