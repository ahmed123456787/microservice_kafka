from use_cases.validate_token import validate_token
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):

    PUBLIC_PATHS = ["/login", "/signup", "/public","/health"]

    async def dispatch(self, request: Request, call_next):

        if request.url.path.endswith(tuple(self.PUBLIC_PATHS)):
            response = await call_next(request)
            return response
        
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        token = auth_header.split(" ")[1] if " " in auth_header else auth_header

        is_valid = await validate_token(token)
        if not is_valid:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        response = await call_next(request)
        return response
