import jwt

from models.user_and_roles import UserAndRoles
from exceptions.exceptions import *
from jwt.exceptions import *
import time

jws_key = "robert"
jws_valid_duration_in_seconds = 60 * 60 * 1

class Jws:
    @staticmethod
    def create_jws(userAndRoles: UserAndRoles):
        userId = userAndRoles.userId
        username = userAndRoles.username
        roles = userAndRoles.roles

        payload = {
            "sub": userId,
            "name": username,
            "roles": roles,
            "exp": time.time() + jws_valid_duration_in_seconds
        }

        token = jwt.encode(payload=payload, key=jws_key, algorithm="HS256")
        return token

    @staticmethod
    def decode_jws(jws):
        try:
            decoded_jws = jwt.decode(jws, jws_key, algorithms="HS256")
            expiration_time = decoded_jws.get("exp")
            current_time = time.time()
            if expiration_time < current_time:
                raise JwsExpiredException("Jws expired!")
            return decoded_jws
        except InvalidSignatureError as ex:
            raise JwsSignatureNotValidException("Jws signature is not valid!")
        except DecodeError as ex:
            raise JwsFormatNotValidException("Jws format is not valid!")
        except ExpiredSignatureError as ex:
            raise JwsExpiredException("Jws expired!")

    @staticmethod
    def check_blacklist(jws):
        blacklist_filepath = "/home/robert/Desktop/POS/Spotify/Aux/jws_blacklist.txt"
        with open(blacklist_filepath, "r") as f:
            lines = f.readlines()
            for blacklisted_jws in lines:
                if jws == blacklisted_jws:
                    raise JwsIsBlacklistedException("Jws is blacklisted!")

        return False
