# python -m pip install lxml spyne
import spyne.error
from spyne import Application, rpc, ServiceBase, Integer, Double, String, Boolean, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from repositories.role_repository import *
from repositories.user_repository import *
from models.user_and_roles import UserAndRoles
from jws_service import Jws
from exceptions.exceptions import *
from utils.roles_util import *
from spyne.error import Fault
import sys


# value = mesajul din exceptie
def global_exception_handler(exception_type, value, traceback):
    if exception_type == JwsFormatNotValidException:
        raise Fault("Client", value)
    elif exception_type == JwsExpiredException:
        raise Fault("Client", value)
    elif exception_type == JwsSignatureNotValidException:
        raise Fault("Client", value)
    elif exception_type == AccessForbiddenException:
        raise Fault("Client", value)
    elif exception_type == JwsIsBlacklistedException:
        raise Fault("Client", value)
    elif exception_type == InvalidCredentialsException:
        raise Fault("Client", value)
    elif exception_type == UserAlreadyHasRoleException:
        raise Fault("Client", value)
    else:
        sys.__excepthook__(exception_type, value, traceback)


def invalidate_jws(jws):
    blacklist_filepath = "/home/robert/Desktop/POS/Spotify/Aux/jws_blacklist.txt"
    with open(blacklist_filepath, "a") as f:
        f.write(jws)
        f.write('\n')


def authorize_jws(jws):
    Jws.check_blacklist(jws)
    decoded_jws = Jws.decode_jws(jws)
    return decoded_jws


class AuthService(ServiceBase):
    @rpc(String, String, _returns=Integer)
    def create_new_role(self, role_name, jws):
        decoded_jws = authorize_jws(jws)
        user_roles = decoded_jws.get("roles")
        if RolesUtil.has_the_correct_role(user_roles, Roles.APP_ADMIN):
            role_id = create_new_role(role_name)
            return role_id

    @rpc(String, String)
    def delete_user(self, id_of_user, jws):
        id_of_user = int(id_of_user)
        decoded_jws = authorize_jws(jws)
        user_id = int(decoded_jws.get("sub"))
        user_roles = decoded_jws.get("roles")
        if RolesUtil.has_the_correct_role(user_roles, Roles.APP_ADMIN):
            if user_id != id_of_user:
                delete_user(id_of_user)
            else:
                raise Fault("Client", "You can't delete your own admin account!")

    @rpc(String, String)
    def delete_role(self, role_name, jws):
        decoded_jws = authorize_jws(jws)
        user_roles = decoded_jws.get("roles")
        if RolesUtil.has_the_correct_role(user_roles, Roles.APP_ADMIN):
            delete_role(role_name)

    @rpc(String, _returns=Array(UserAndRoles, wrapped=False))
    def get_all_users_with_their_roles(self, jws):
        decoded_jws = authorize_jws(jws)
        user_roles = decoded_jws.get("roles")
        if RolesUtil.has_the_correct_role(user_roles, Roles.APP_ADMIN):
            users = get_users()
            users_and_roles = []
            for user in users:
                role_list = []
                for role in user.roles:
                    role_list.append(role.role_name)
                users_and_roles.append(UserAndRoles(user.user_id, user.username, role_list))
            return users_and_roles

    @rpc(String, _returns=Array(String, wrapped=False))
    def get_roles(self, jws):
        decoded_jws = authorize_jws(jws)
        user_roles = decoded_jws.get("roles")
        if RolesUtil.has_the_correct_role(user_roles, Roles.APP_ADMIN):
            roles = get_roles()
            role_list = []
            for role in roles:
                role_list.append(role.role_name)
            return role_list

    @rpc(String, String, String)
    def change_password(self, id_of_user, new_password, jws):
        id_of_user = int(id_of_user)
        decoded_jws = authorize_jws(jws)
        user_id = decoded_jws.get("sub")
        user_roles = decoded_jws.get("roles")
        if RolesUtil.has_the_correct_role(user_roles, Roles.APP_ADMIN) or id_of_user == user_id:
            change_password(id_of_user, new_password)

    @rpc(String, String, String)
    def change_username(self, id_of_user, new_username, jws):
        id_of_user = int(id_of_user)
        decoded_jws = authorize_jws(jws)
        user_id = decoded_jws.get("sub")
        user_roles = decoded_jws.get("roles")
        if RolesUtil.has_the_correct_role(user_roles, Roles.APP_ADMIN) or id_of_user == user_id:
            change_username(id_of_user, new_username)

    #####################################################################

    @rpc(String, String, _returns=Integer)
    def create_new_user(self, username, password):
        user_id = create_new_user(username, password)
        assign_roles_to_user(user_id, ["client"])
        return user_id

    @rpc(String, Array(String, wrapped=False), String)
    def assign_roles_to_user(self, user_id, roles_list, jws):
        decoded_jws = authorize_jws(jws)
        user_roles = decoded_jws.get("roles")
        if RolesUtil.has_the_correct_role(user_roles, Roles.APP_ADMIN):
            assign_roles_to_user(user_id, roles_list)

    @rpc(String, String, _returns=UserAndRoles)
    def get_user_info_and_his_roles(self, id_of_user, jws):
        id_of_user = int(id_of_user)
        decoded_jws = authorize_jws(jws)
        user_id = decoded_jws.get("sub")
        user_name = decoded_jws.get("name")
        user_roles = decoded_jws.get("roles")
        if RolesUtil.has_the_correct_role(user_roles, Roles.APP_ADMIN) or id_of_user == user_id:
            user = get_user(id_of_user)
            role_list = []
            for role in user.roles:
                role_list.append(role.role_name)
            return UserAndRoles(user.user_id, user.username, role_list)

    @rpc(String, String, _returns=String)
    def login(self, username, password):
        user = get_user_by_username(username)
        if user and user.password == password:
            roles = []
            for role in user.roles:
                roles.append(role.role_name)
            userAndRoles = UserAndRoles(user.user_id, user.username, roles)
            jws_token = Jws.create_jws(userAndRoles)
            return jws_token
        raise Fault("Client", "Invalid credentials")

    @rpc(String)
    def logout(self, jws):
        invalidate_jws(jws)


application = Application([AuthService], 'services.auth.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    sys.excepthook = global_exception_handler

    import logging
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.INFO)
    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://127.0.0.1:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
