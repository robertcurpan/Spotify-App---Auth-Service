from models.role_orm import Role
from base.sql_base import Session


def create_new_role(role_name):
    session = Session()
    try:
        role = Role(role_name)
        session.add(role)
        session.commit()
        return role.role_id
    except Exception as ex:
        print(f"Failed to add new role - {ex}")


def delete_role(role_name):
    session = Session()
    try:
        role = session.query(Role).filter(Role.role_name == role_name).first()
        session.delete(role)
        session.commit()
    except Exception as ex:
        print(f"Invalid role_name - {ex}")


def get_roles():
    session = Session()
    roles = session.query(Role).all()
    return roles
