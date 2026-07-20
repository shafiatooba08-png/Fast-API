class AppException(Exception):
    """Base exception for the application."""
    pass


class LeadNotFoundError(AppException):
    def __init__(self):
        super().__init__("Lead not found")


class PropertyConflictError(AppException):
    def __init__(self):
        super().__init__("Property conflict")


class PermissionDeniedError(AppException):
    def __init__(self):
        super().__init__("Permission denied")
        
class UsernameAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__("Username already exists")
class CustomerNotFoundError(Exception):
    pass


class PropertyNotFoundError(Exception):
    pass