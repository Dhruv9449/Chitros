""" Handles password hashing and verifying"""

# Imports
from passlib.context import CryptContext


# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Creating and verifying hashed passwords

def get_password(password) -> str:
    """  Hashes password string """
    return pwd_context.hash(password)


def verify_password(input_password, hashed_password) -> str:
    """ Verifies password """
    return pwd_context.verify(input_password, hashed_password)
