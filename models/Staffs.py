from app import db


class StaffsModel(db.Model):
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    email = db.Column(db.String())
    phone = db.Column(db.String())

    # insert records
    def insert_records(self):
        db.session.add(self)
        db.session.commit()
        return self

    # fetch all records
    @classmethod
    def fetch_all(cls):
        return cls.query.all()
