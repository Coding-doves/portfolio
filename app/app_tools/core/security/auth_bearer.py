from fastapi import Request, status, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials

from app_tools.core.security import security
from app_tools.core.db import redis


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        cred = await super().__call__(request)

        if cred is None or not cred.credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization header")

        token = cred.credentials
        
        token_data = security.decode_token(token, token_type="refresh")
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )
                
        # Check if the token is blacklisted
        if redis.is_token_blacklisted(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    'error': "Token has been blacklisted",
                    'reason': "User logged out or token revoked",
                    'resolution': "Please login again"
                }
            )

        self.verify_token_data(token_data=token_data)
            
        return token_data

    
    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError('Please overide this method in child classes')


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get('refresh'):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a access token"
            )


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if not token_data.get('refresh'):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token"
            )
