import hashlib
from datetime import datetime, timedelta
from jose import jwt

# -------------------------------------------------
# JWT CONFIG
# -------------------------------------------------
SECRET_KEY = "CHANGE_THIS_LATER"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours


# -------------------------------------------------
# PASSWORD HELPERS (NO EXTERNAL DEPENDENCIES)
# -------------------------------------------------
def hash_password(password: str) -> str:
    """
    Hash plain password for storage (SHA-256)
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify plain password against stored hash
    """
    return hash_password(password) == hashed_password


# -------------------------------------------------
# TOKEN CREATION
# -------------------------------------------------
def create_access_token(data: dict):
    """
    Create JWT access token
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
