from app import db


class SalesModel(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, primary_key=True)
    shed_no = db.Column(db.String())
    quantity = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    date = db.Column(db.String())

    # insert into db
    def insert_records(self):
        db.session.add(self)
        db.session.commit()
        return self

    # fetch sales
    @classmethod
    def fetch_all(cls):
        return cls.query.all()

