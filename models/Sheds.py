from app import db
from models.Vaccines import VaccinesModel


class ShedsModel(db.Model):
    __tablename__ = 'sheds'
    id = db.Column(db.Integer, primary_key=True)
    shed_no = db.Column(db.String())
    swine_name = db.Column(db.String())
    quantity = db.Column(db.Integer)

    system_user_id = db.Column(db.Integer, db.ForeignKey('system_users.id'))

    # pseudocolumn for vaccines
    vaccines = db.relationship(VaccinesModel, backref='shed')

    # insert into db
    def insert_records(self):
        db.session.add(self)
        db.session.commit()
        return self

    # fetch sheds
    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    # fetch by id
    @classmethod
    def fetch_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    # fetch by shed_no
    @classmethod
    def fetch_by_shed_no(cls, shed_no):
        return cls.query.filter_by(shed_no=shed_no).first()

    # check shed no
    @classmethod
    def check_shed(cls, shed_no):
        record = cls.query.filter_by(shed_no=shed_no).first()
        return record

    # update shed information
    @classmethod
    def update_by_id(cls, id, shed_no=None, swine_name=None, quantity=None):
        record = cls.query.filter_by(id=id).first()
        if shed_no:
            record.shed_no = shed_no
        if swine_name:
            record.swine_name = swine_name
        if quantity:
            record.quantity = quantity

        db.session.commit()
        return True

    # delete shed
    @classmethod
    def delete_by_id(cls, id):
        record = cls.query.filter_by(id=id)
        record.delete()
        db.session.commit()
        return True