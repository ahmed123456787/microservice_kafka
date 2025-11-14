from .exceptions import MissingTokenError, InvalidTokenError
from jose import jwt, JWTError, ExpiredSignatureError
from config.settings import BaseSettings


def validate_token(token: str, settings: BaseSettings) -> bool:
    
    if token is None or token == "":
        raise MissingTokenError
    
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return True
        
    except ExpiredSignatureError:
        raise InvalidTokenError("Token has expired")
    
    except JWTError:
        raise InvalidTokenError("Invalid token")
    
    except Exception as e:
        raise InvalidTokenError(f"Token validation failed: {str(e)}")