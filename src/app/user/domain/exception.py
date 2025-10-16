
class UserNotFoundError(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User with username '{username}' not found.")


class UserAlreadyExistsError(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User with username '{username}' already exists.")


class InvalidUserRoleError(Exception):
    def __init__(self, role: str):
        self.role = role
        super().__init__(f"Invalid user role: '{role}'.")


class UserInactiveError(Exception):
    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User with username '{username}' is inactive.")


