import hashlib, binascii, random, string, crypt
from hmac import compare_digest as compare_hash


def hash_password(password):
    salt = ''.join(random.sample(string.ascii_letters, 2))
    return crypt.crypt(crypt.crypt(password, salt), salt)


def compare_password(password, cryptedpasswd):
    return compare_hash(crypt.crypt(crypt.crypt(password, cryptedpasswd), cryptedpasswd), cryptedpasswd)