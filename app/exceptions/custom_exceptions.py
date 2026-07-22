class AppException(Exception):

    def __init__(self, message: str):
        self.message = message


class AuthenticationException(AppException):
    pass


class AuthorizationException(AppException):
    pass


class ResourceNotFoundException(AppException):
    pass


class DuplicateRecordException(AppException):
    pass


class ValidationException(AppException):
    pass


class HouseOccupiedException(AppException):
    pass


class TenantAlreadyAssignedException(AppException):
    pass


class DuplicatePaymentException(AppException):
    pass