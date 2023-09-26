import glob
from pathlib import Path
from typing import List

from models.sqlmodels import VideoIndex


class VideosFileLoader:
    def __init__(self, path: str):
        self.path = path

    def get_videos(self) -> List[VideoIndex]:
        paths = glob.glob(f"{self.path}/**/*.mp4", recursive=True)

        return [
            VideoIndex(
                slug=self._get_slug(x),
                name=self._get_name(x),
                full_path=x,
                prefix=self._get_prefix(x),
            )
            for x in paths
        ]

    def _get_slug(self, path: str):
        return Path(path).stem.replace(" ", "-")

    def _get_name(self, path: str):
        return Path(path).stem.replace("-", " ")

    def _get_prefix(self, path: str):
        return Path(path).suffix
