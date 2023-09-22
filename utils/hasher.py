from uuid import UUID

import jwt
from argon2 import PasswordHasher

from utils.hasher_exceptions import (ThisIsNotCorrectTokenException,
                                     TokenExpireException, UuidException)


class HasherPassword:
    def __init__(self, salt: str):
        self.salt = salt
        self.password_hasher = PasswordHasher()

    def make_secret(self, password: str) -> str:
        password_hash = self.password_hasher.hash(
            bytes(password, encoding="utf-8"),
            salt=bytes(self.salt.encode("utf-8")))
        return password_hash

    def check(self, hash: str, password: str) -> bool:
        password_hash = self.make_secret(password)
        if password_hash == hash:
            return True
        return False


class HasherJwt:
    def __init__(self, algorithm: str, secret: str, expire=None):
        self.algorithm = algorithm
        self.secret = secret
        self.expire = None

    def make_secret(self, public_id: UUID) -> str:
        try:
            UUID(public_id, version=4)
        except ValueError:
            raise UuidException()

        create_jwt = jwt.encode({
            "id": public_id
        }, self.secret, algorithm=self.algorithm)
        return create_jwt

    def make_unsecret(self, token: str) -> str:
        try:
            decode_token = jwt.decode(
                token,
                self.secret,
                algorithms=self.algorithm,
                options={"verify_signature": True}
            )
            return decode_token.get("id")
        except (
                jwt.exceptions.InvalidTokenError,
                jwt.exceptions.DecodeError
        ):
            raise ThisIsNotCorrectTokenException(token)
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpireException()
