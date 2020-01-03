from app import db


class FeedsModel(db.Model):
    __tablename__ = 'feeds'
    id = db.Column(db.Integer, primary_key=True)
    feed_name = db.Column(db.String())
    unit_price = db.Column(db.String())
    quantity = db.Column(db.Integer())
    total = db.Column(db.String())
    date = db.Column(db.String())

    # insert records
    def insert_records(self):
        db.session.add(self)
        db.session.commit()
        return self

    # fetch all records
    @classmethod
    def fetch_all(cls):
        return cls.query.all()