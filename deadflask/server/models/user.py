import bcrypt
from sqlalchemy import Column, Integer, String, Boolean

from deadflask.server.dbcore import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    password = Column(String)
    salt = Column(String)
    is_active = Column(Boolean, default=False)

    @classmethod
    def authenticate(cls, app, email, password):
        if not email or not password:
            return None

        user = app.db_session.query(cls).filter_by(email=email).one_or_none()

        if not user or not bcrypt.checkpw(password, user.password):
            return None

        return user

    @classmethod
    def create(cls, app, email, name, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password, salt)
        new = User(email=email, name=name, password=str(hashed_password), salt=str(salt))
        app.db_session.add(new)

        return new
