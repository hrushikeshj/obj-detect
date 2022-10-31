from click import password_option
from sqlalchemy import Column, Integer, String, Text
from database import Base
import bcrypt

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50))
    name = Column(String(50))
    password = Column(String(200))

    def __init__(self, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = bcrypt.hashpw(str(kwargs["password"]).encode('utf-8'), bcrypt.gensalt())
        super().__init__(**kwargs)

    def val(self, p):
        return bcrypt.checkpw(p.encode('utf-8'), self.password)

    def __repr__(self):
        return f'<User id: {self.id!r}, email: {self.email!r}>'
