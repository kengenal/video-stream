from uuid import uuid4

import jwt
import pytest

from utils.hasher import HasherJwt, HasherPassword
from utils.hasher_exceptions import (ThisIsNotCorrectTokenException,
                                     UuidException)


class TestHashPassword:
    def setup(self):
        self.hasher = HasherPassword(salt="correct horse battery staple")

    def test_hash_password(self):
        password = "test"

        hash = self.hasher.make_secret(password)

        assert len(hash) > len(password)

    def test_verify_with_incorrect_password(self):
        random_password_hash = self.hasher.make_secret("test")
        assert self.hasher.check("test2", random_password_hash) is False

    def test_verify_with_correct_password(self):

        correct_hash = self.hasher.make_secret("test")
        assert self.hasher.check(correct_hash, "test") is True

    def test_verify_with_incorrect_hash(self):
        assert self.hasher.check("wrong hash", "test") is False


class TestHashJwt:
    def setup(self):
        self.hasher = HasherJwt(algorithm="HS256", secret="test")

    def test_create_hash(self):
        public_id = str(uuid4())
        token = self.hasher.make_secret(public_id)
        decode_token = jwt.decode(token, options={"verify_signature": False})

        assert len(token) != public_id
        assert decode_token == {"id": public_id}

    def test_create_hash_value_is_not_uuid(self):
        with pytest.raises(UuidException):
            self.hasher.make_secret("1235")

    def test_decode_token_and_get_public_id_with_correct_data(self):
        public_id = str(uuid4())
        token = self.hasher.make_secret(public_id)

        decode_token = self.hasher.make_unsecret(token)

        assert decode_token == public_id

    def test_decode_with_broken_token_should_be_raise_exception(self):
        with pytest.raises(ThisIsNotCorrectToken):
            self.hasher.make_unsecret("123")

    def test_decode_with_token_encode_with_another_secret(self):
        another_hasher = HasherJwt(algorithm="HS256", secret="hehehe")

        token = another_hasher.make_secret(str(uuid4()))

        with pytest.raises(ThisIsNotCorrectTokenException):
            self.hasher.make_unsecret(token)
