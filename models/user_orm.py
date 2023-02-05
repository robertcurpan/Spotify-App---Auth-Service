from sqlalchemy import Column, String, Integer
from base.sql_base import Base
from sqlalchemy.orm import relationship
from models.users_roles_orm import users_roles_relationship


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    roles = relationship("Role", secondary=users_roles_relationship)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def set_new_password(self, new_password):
        self.password = new_password

    def set_new_username(self, new_username):
        self.username = new_username
