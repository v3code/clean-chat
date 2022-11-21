import bcrypt


def encrypt_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bytes.decode(bcrypt.hashpw(password.encode('utf-8'), salt))


def check_password(password: str, other_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), other_password.encode('utf-8'))
