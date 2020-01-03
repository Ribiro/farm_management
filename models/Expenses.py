from app import db


class ExpensesModel(db.Model):
    __tablename__ ='expenses'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    amount = db.Column(db.String())
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