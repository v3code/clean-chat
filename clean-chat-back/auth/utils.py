import bcrypt


def encrypt_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bytes.decode(bcrypt.hashpw(password.encode('utf-8'), salt))