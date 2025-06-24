import redis
from app_tools.core.config import Settings

settings = Settings()

REFRESH_TOKEN_EXPIRE_MINUTES = 3600

# Initialize Redis client for token blacklist
# This client will be used to store and check blacklisted tokens
token_blacklist = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,
)


def add_token_to_blacklist(jti: str) -> None:
    """
    Add a token to the blacklist in Redis.
    """
    return token_blacklist.set(name=jti, value="", ex=REFRESH_TOKEN_EXPIRE_MINUTES)


def is_token_blacklisted(jti: str) -> bool:
    """
    Check if a token is blacklisted in Redis.
    """
    jti_tok = token_blacklist.get(jti)
    return jti_tok is not None
