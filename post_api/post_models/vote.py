from main import db


class Vote(db.Model):
    post_id = db.Column(db.Integer, nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    # -1 no vote, 0 la premiere image, 1 la seconde
    value = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Vote {0} {1}: {2}>".format(self.user_id, self.post_id, self.value)

