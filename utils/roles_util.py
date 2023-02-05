from exceptions.exceptions import AccessForbiddenException

class Roles:
    CLIENT = "client"
    ARTIST = "artist"
    CONTENT_MANAGER = "content_manager"
    APP_ADMIN = "administrator_aplicatie"


class RolesUtil:
    @staticmethod
    def has_the_correct_role(user_roles, desired_role):
        for user_role in user_roles:
            if user_role == desired_role:
                return True

        raise AccessForbiddenException("You don't have the proper role for this operation!")
