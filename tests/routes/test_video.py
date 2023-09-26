import os
import shutil

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from config.settings import Settings
from models.sqlmodels import VideoIndex


class TestVideoIndex:
    @pytest.fixture(autouse=True)
    def setup(self, settings: Settings):
        self.path = settings.video_path
        self.url = "/api/v1/videos/index/"

    def test_index_file_only_one_file(self, auth_client: TestClient, db: Session):
        self._create_file("test.mp4")

        request = auth_client.get(self.url)
        get_items = db.query(VideoIndex).all()

        assert len(get_items) == 1
        assert request.status_code == status.HTTP_200_OK

    def test_index_file_multiple_files(self, auth_client: TestClient, db: Session):
        self._create_file("test.mp4")
        self._create_file("test1.mp4")
        self._create_file("test2.mp4")

        request = auth_client.get(self.url)

        get_items = db.query(VideoIndex).all()

        assert len(get_items) == 3
        assert request.status_code == status.HTTP_200_OK

    def _create_file(self, filename: str):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        with open(os.path.join(self.path, filename), "w") as f:
            f.write("FOOBAR")

    def teardown(self):
        shutil.rmtree(self.path)


class TestVideo:
    def setup(self):
        self.url = "/api/v1/videos/"

    def test_get_video(self, auth_client: TestClient, db: Session):
        request = auth_client.get(self.url)

        assert request.status_code == status.HTTP_200_OK

    def test_get_user_but_user_is_not_authenticated(
        self, client: TestClient, db: Session
    ):
        request = client.get(self.url)

        assert request.status_code == status.HTTP_401_UNAUTHORIZED
