from typing import Optional, Dict
from src.models.quest import Quest
from src.repositories.BaseRepository import BaseRepository

class QuestRepository(BaseRepository):
    """
    todo_rpg.json 파일과 연동하여 퀘스트 데이터를 O(1) 성능으로 조회 및 저장하는 리포지토리입니다.
    """
    
    def find_quest(self, quest_id: str) -> Optional[Quest]:
        """quest_id를 딕셔너리 키로 사용하여 O(1)로 퀘스트를 조회합니다."""
        data = self._load_data()
        quests_dict = data.get("quests", {})
        
        quest_data = quests_dict.get(quest_id)
        if not quest_data:
            return None
            
        quest = Quest(
            quest_id=quest_data["quest_id"],
            content=quest_data["content"],
            difficulty=quest_data["difficulty"]
        )
        if quest_data.get("is_completed"):
            quest.complete_quest()
            
        return quest

    def save_quest(self, quest: Quest) -> None:
        """퀘스트 객체를 딕셔너리에 O(1)로 업데이트 후 파일에 저장합니다."""
        data = self._load_data()
        
        if "quests" not in data:
            data["quests"] = {}
            
        data["quests"][quest.quest_id] = {
            "quest_id": quest.quest_id,
            "content": quest.content,
            "difficulty": quest.difficulty,
            "is_completed": quest.is_finished()
        }
        
        self._save_data(data)

    def delete_quest(self, quest_id: str) -> None:
        """quest_id를 기반으로 O(1) 성능으로 딕셔너리에서 퀘스트를 삭제합니다."""
        data = self._load_data()
        quests_dict = data.get("quests", {})
        
        if quest_id in quests_dict:
            del quests_dict[quest_id]
            self._save_data(data)

    def find_all_quests(self) -> Dict[str, Quest]:
        """모든 퀘스트를 딕셔너리 형태로 반환하여 O(1) 인덱싱 접근을 유지합니다."""
        data = self._load_data()
        quests_dict = data.get("quests", {})
        
        result = {}
        for q_id, q_data in quests_dict.items():
            quest = Quest(
                quest_id=q_data["quest_id"],
                content=q_data["content"],
                difficulty=q_data["difficulty"]
            )
            if q_data.get("is_completed"):
                quest.complete_quest()
            result[q_id] = quest
            
        return result
