from argon2 import PasswordHasher


def verify_password(plain_password, hashed_password) -> bool:
    ph = PasswordHasher()
    return ph.verify(hashed_password, plain_password)


def get_password_hash(password) -> str:
    ph = PasswordHasher()
    return ph.hash(password)
