import json
import os

class BaseRepository:
    """
    JSON 파일 입출력을 담당하는 기본 리포지토리 클래스입니다.
    이 클래스를 상속받아 User와 Quest 각각의 리포지토리를 구현합니다.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._initialize_file()

    def _initialize_file(self) -> None:
        """파일이 없을 경우 초기 구조를 생성합니다."""
        if not os.path.exists(self.file_path):
            self._save_data({"users": {}, "quests": {}})

    def _load_data(self) -> dict:
        """파일에서 전체 데이터를 불러옵니다."""
        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _save_data(self, data: dict) -> None:
        """전체 데이터를 파일에 저장합니다."""
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
