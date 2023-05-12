import re
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

PASSWORD_PATTERN = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!_|\(\)\{\}@$%^&*\[\]-]).{8,}$"  # NOQA

REGISTRATION_ERROR_MESSAGES = {
    'email': 'Specified email already exists',
    'username': 'Specified username already exists',
}


def check_password(password: str):
    return re.match(PASSWORD_PATTERN, password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)
