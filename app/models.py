from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.__init___ import db


class Gift(db.Model):
    __tablename__ = 'gifts'

    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Gift %r >' % self.id
