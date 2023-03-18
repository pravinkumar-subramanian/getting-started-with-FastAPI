import jwt
from core.utils import OAuth2PasswordBearerCookie
from passlib.context import CryptContext
from datetime import datetime, timedelta
from core import config
import secrets


#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")
oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/api/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = secrets.token_urlsafe(30)
ALGORITHM = config.ENCRYPTION
TOKEN = config.TOKEN_NAME
ACCESS_TOKEN_EXPIRE_MINUTES = int(config.TOKEN_EXPIRY)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
