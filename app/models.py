from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from .__init___ import db


class Gift(db.Model):
    __tablename__ = 'gifts'

    id = Column(Integer, primary_key=True)
    image_path = Column(String)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Gift %r >' % self.id
