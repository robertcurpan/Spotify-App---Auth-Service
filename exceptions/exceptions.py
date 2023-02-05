class JwsFormatNotValidException(Exception):
    def __init__(self, message):
        super().__init__(message)


class JwsExpiredException(Exception):
    def __init__(self, message):
        super().__init__(message)


class JwsSignatureNotValidException(Exception):
    def __init__(self, message):
        super().__init__(message)


class AccessForbiddenException(Exception):
    def __init(self, message):
        super().__init__(message)


class JwsIsBlacklistedException(Exception):
    def __init(self, message):
        super().__init__(message)


class InvalidCredentialsException(Exception):
    def __init(self, message):
        super().__init__(message)


class UserAlreadyHasRoleException(Exception):
    def __init(self, message):
        super().__init__(message)