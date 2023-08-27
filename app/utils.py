from passlib.context import CryptContext

password_encryptor = CryptContext(schemes=["bcrypt"], deprecated="auto")

def encrypt(password: str):
    return password_encryptor.hash(password)

def verify(plain_password, hashed_password):
    return password_encryptor.verify(plain_password, hashed_password)