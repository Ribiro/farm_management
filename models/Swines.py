from app import db


class SwinesModel(db.Model):
    __tablename__ = 'swines'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    quantity = db.Column(db.Integer)
    date = db.Column(db.String())
    shed_id = db.Column(db.Integer, db.ForeignKey('sheds.id'))