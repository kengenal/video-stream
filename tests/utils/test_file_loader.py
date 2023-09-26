import os
import shutil

from utils.file_loader import VideosFileLoader


class TestVideosLoader:
    def setup(self):
        self.path = "test_glob"
        self.file_loader = VideosFileLoader(self.path)

    def test_load_video_with_existing_file_structure(self):
        self._create_file("test.mp4")

        videos = self.file_loader.get_videos()

        assert len(videos) == 1
        assert videos[0].name == "test"

    def test_load_video_two_files_in_folder_but_only_one_is_video_file(self):
        self._create_file("test.csv")
        self._create_file("test.mp4")

        videos = self.file_loader.get_videos()

        assert len(videos) == 1
        assert videos[0].name == "test"

    def test_load_video_multiple_video_files(self):
        self._create_file("test.mp4")
        self._create_file("test2.mp4")

        videos = self.file_loader.get_videos()

        assert len(videos) == 2
        assert videos[0].name == "test"
        assert videos[1].name == "test2"

    def test_load_video_multiple_files_but_one_file_is_not_a_video(self):
        self._create_file("test.mp4")
        self._create_file("test2.mp4")
        self._create_file("random_file.csv")

        videos = self.file_loader.get_videos()

        assert len(videos) == 2
        assert videos[0].name == "test"
        assert videos[1].name == "test2"

    def _create_file(self, filename: str):
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        with open(os.path.join(self.path, filename), "w") as f:
            f.write("FOOBAR")

    def teardown(self):
        shutil.rmtree(self.path)
