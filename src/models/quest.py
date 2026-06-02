"""
투두RPG의 퀘스트(할 일) 데이터를 관리하는 도메인 모델 클래스입니다.
"""

class Quest:
    """
    퀘스트ID, 내용, 난이도(상/중/하), 완료 여부 데이터 구조를 정의합니다.
    """

    def __init__(self, quest_id: str, content: str, difficulty: str):
        self.quest_id = quest_id
        self.content = content
        self.difficulty = difficulty
        self.is_completed = False

    def is_finished(self) -> bool:
        """
        퀘스트가 완료되었는지 확인합니다.
        """
        return self.is_completed

    def complete_quest(self) -> None:
        """
        퀘스트의 상태를 완료(True)로 변경합니다.
        """
        self.is_completed = True

    def update_content(self, new_content: str) -> None:
        """
        퀘스트의 내용을 수정합니다.
        """
        self.content = new_content

    def update_difficulty(self, new_difficulty: str) -> None:
        """
        퀘스트의 난이도를 수정합니다.
        """
        self.difficulty = new_difficulty
