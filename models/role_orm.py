from sqlalchemy import Column, String, Integer
from base.sql_base import Base
from sqlalchemy.orm import relationship
from models.users_roles_orm import users_roles_relationship


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    role_name = Column(String, unique=True, nullable=False)

    def __init__(self, role_name):
        self.role_name = role_name
