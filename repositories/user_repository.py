from spyne import Fault

from exceptions.exceptions import UserAlreadyHasRoleException
from models.role_orm import Role
from models.user_orm import User
from base.sql_base import Session
from models.user_and_roles import UserAndRoles


def create_new_user(username, password):
    session = Session()
    user = User(username, password)
    try:
        session.add(user)
        session.commit()
        return user.user_id
    except Exception as exc:
        print(f"Failed to add user - {exc}")


def assign_roles_to_user(user_id, roles_list):
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        roles = session.query(Role).all()
        for role_name in roles_list:
            for role in roles:
                if role_name == role.role_name:
                    if not user_has_role(user, role_name):
                        user.roles.append(role)
                        break
                    else:
                        raise UserAlreadyHasRoleException()
        session.commit()
    except UserAlreadyHasRoleException as ex:
        raise Fault("Client", "User already has that role!")


def user_has_role(user, role_name):
    for role in user.roles:
        if role.role_name == role_name:
            return True
    return False


def delete_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        session.delete(user)
        session.commit()
    except Exception as ex:
        print(f"Invalid username - {ex}")


def get_user(user_id):
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        return user
    except Exception as ex:
        print(f"Couldn't get user {user_id} - {ex}")


def get_user_by_username(username):
    session = Session()
    try:
        user = session.query(User).filter(User.username == username).first()
        return user
    except Exception as ex:
        print(f"Couldn't get user {username} - {ex}")


def get_users():
    session = Session()
    users = session.query(User).all()
    return users


def change_password(user_id, new_password):
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        user.set_new_password(new_password)
        session.commit()
    except Exception as ex:
        print(f"Couldn't change password of user - {user_id} -- {ex}")


def change_username(user_id, new_username):
    session = Session()
    try:
        user = session.query(User).filter(User.user_id == user_id).first()
        user.set_new_username(new_username)
        session.commit()
    except Exception as ex:
        print(f"Couldn't change username of user - {user_id} -- {ex}")