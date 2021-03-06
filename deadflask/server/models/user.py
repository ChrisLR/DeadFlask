import bcrypt
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from deadflask.server.dbcore import Base
from deadflask.server.app import app


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=False)
    characters = relationship('Character')

    @classmethod
    def authenticate(cls, email, password):
        if not email or not password:
            return None

        user = app.db_query(User).filter_by(email=email).one_or_none()
        encoded_password = password.encode('utf-8')
        encoded_db_password = user.password.encode('utf-8')
        if not user or not bcrypt.checkpw(encoded_password, encoded_db_password):
            return None

        return user

    @classmethod
    def create(cls, email, password):
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        decoded_password = hashed_password.decode('utf8')
        new = User(email=email, password=str(decoded_password))
        app.db_session.add(new)

        return new
