
class InvalidTokenError(Exception):
    pass

class NotAuthorizedException(Exception):
    def __str__(self) -> str:
        return "Not authorized"
    

class MissingTokenError(Exception):
    def __str__(self):
        return "Token is missing"