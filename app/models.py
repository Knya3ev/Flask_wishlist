from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app.__init___ import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    images_path = Column(String, default=None)
    email = Column(String(60), index=True, unique=True)
    username = Column(String(60), index=True, unique=True)
    first_name = Column(String(60), index=True)
    last_name = Column(String(60), index=True)
    password_hash = Column(String(128))
    gift_id = relationship('Gift')
    is_admin = Column(Boolean, default=False)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {} id: {}>'.format(self.username, self.id)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Gift(db.Model):
    __tablename__ = 'gifts'

    id = Column(Integer, primary_key=True)
    image_path = Column(String, default=None)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Gift %r >' % self.id
