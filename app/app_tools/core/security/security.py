import os
import jwt
import logging
import uuid

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from jwt import PyJWTError
from passlib.context import CryptContext

from app_tools.core.config import Settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
settings = Settings()


def hash_password(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a password against a hashed password.

    Args:
        plain_password (str): The plain password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return password_context.verify(plain_password, hashed_password)


def password_meets_criteria(password: str) -> bool:
    """
    Checks if a password meets the specified criteria.

    Args:
        password (str): The password to check.

    Returns:
        bool: True if the password meets the criteria, False otherwise.
    """
    return len(password) >= 7 and\
        any(char.isdigit() for char in password) and\
        any(char.islower() for char in password) and\
        any(char.isupper() for char in password)


def generate_token(
    data: dict, token_type: str = "access", expires: timedelta = None
) -> str:
    """
    Generates a JWT token.

    Args:
        data (dict): The data to encode in the token.
        secret_key (str): The secret key to sign the token.
        algorithm (str): The algorithm to use for signing the token.

    Returns:
        str: The generated JWT token.
    """
    payload = data.copy()
    expiration = datetime.utcnow() + expires if expires else datetime.utcnow() + timedelta(hours=1)
    payload["exp"] = expiration
    payload.update({"type": token_type})  # Type of the token (e.g., "access", "refresh", "jti")
    payload.update({"jti": str(uuid.uuid4())})  # Unique identifier for the token
    
    return jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str, token_type:str = "access") -> dict:
    """
    Decodes a JWT token.

    Args:
        token (str): The JWT token to decode.
        secret_key (str): The secret key to verify the token.
        algorithms (list): The algorithms to use for verifying the token.

    Returns:
        dict: The decoded data from the token.
    """
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token type. Expected {token_type}, got {payload.get('type')}",
                headers={"WWW-Authenticate": "Bearer"}
            )

        # If the user ID is present in the payload
        user_id = payload.get("id")
        user_email = payload.get("email")

        if user_id is None or user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload. Missing user ID or email",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return payload

    except PyJWTError as e:
        logging.exception(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired or is invalid",
            headers={"WWW-Authenticate": "Bearer"}
        )
