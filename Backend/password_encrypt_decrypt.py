import bcrypt

def password_encrypt(password):
    salt = bcrypt.gensalt(rounds=15)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def password_decrypt(password,hashed_password):
    if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
        return True
    else:
        return False