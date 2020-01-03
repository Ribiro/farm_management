from app import db


class VaccinesModel(db.Model):
    __tablename__ = 'vaccines'
    id = db.Column(db.Integer, primary_key=True)
    vaccine_name = db.Column(db.String())
    date_administered = db.Column(db.String())
    next_date = db.Column(db.String())
    cost = db.Column(db.String)
    shed_id = db.Column(db.Integer, db.ForeignKey('sheds.id'))

    # insert records
    def insert_records(self):
        db.session.add(self)
        db.session.commit()
        return self