from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey

from base.sql_base import Base

users_roles_relationship = Table(
    'users_roles', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('role_id', Integer, ForeignKey('roles.role_id')),
    extend_existing=True
)
