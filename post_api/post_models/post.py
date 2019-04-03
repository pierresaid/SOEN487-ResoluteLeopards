from main import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    url_one = db.Column(db.Text, nullable=False)
    url_two = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Post {0}: {1}>".format(self.id, self.title)


