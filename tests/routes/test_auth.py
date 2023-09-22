from unittest.mock import ANY

from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.sqlmodels import User


class TestToken:
    def setup(self):
        self.url = "/api/v1/token/"

    def test_atuh_token_with_correct_credentials(
            self,
            client: TestClient,
            db: Session
    ):
        user = self._create_user(db, "test", "test")
        request = client.post(self.url, json={
            "username": user.username,
            "password": "test"
        })
        assert request.status_code == status.HTTP_200_OK
        assert request.json() == {"token": ANY}
        assert len(request.json()["token"]) > 10

    def test_auth_with_incorrect_credentials(
            self, client: TestClient,
            db: Session
    ):
        self._create_user(db, "test", "test")

        request = client.post(self.url, json={
            "username": "test",
            "password": "random_incorrect_password"
        })

        assert request.status_code == status.HTTP_400_BAD_REQUEST

    def test_auth_with_empty_payload(self, client: TestClient, db: Session):
        self._create_user(db, "test", "test")

        request = client.post(self.url, json={})

        assert request.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def _create_user(self, db: Session, username: str, password: str) -> User:
        user = User(username=username)
        user.make_password(password=password)
        db.add(user)
        db.commit()
        return user
