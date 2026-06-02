from src.repositories.UserRepository import UserRepository
from src.repositories.QuestRepository import QuestRepository
from src.models.user import User

class RpgService:
    """투두RPG의 핵심 비즈니스 로직(퀘스트 완료, 보상, 레벨업)을 담당합니다."""

    # 난이도별 보상 설정
    REWARDS = {
        "하": {"xp": 10, "gold": 5},
        "중": {"xp": 20, "gold": 10},
        "상": {"xp": 30, "gold": 20}
    }

    def __init__(self, user_repo: UserRepository, quest_repo: QuestRepository):
        self.user_repo = user_repo
        self.quest_repo = quest_repo

    def complete_quest(self, user_id: str, quest_id: str) -> None:
        """퀘스트를 완료 처리하고 난이도에 따른 보상을 지급합니다."""
        user = self.user_repo.find_user(user_id) or User()
        quest = self.quest_repo.find_quest(quest_id)
        
        if not quest:
            raise ValueError("해당 퀘스트를 찾을 수 없습니다.")
        if quest.is_finished():
            raise ValueError("이미 완료된 퀘스트입니다.")

        quest.complete_quest()
        self.quest_repo.save_quest(quest)

        reward = self.REWARDS.get(quest.difficulty, {"xp": 0, "gold": 0})
        user.add_xp(reward["xp"])
        user.add_gold(reward["gold"])

        self._apply_levelup_if_needed(user)
        self.user_repo.save_user(user_id, user)

    def is_levelup_condition(self, user: User) -> bool:
        """레벨업 조건을 달성했는지 확인합니다."""
        required_xp = user.level * 100
        return user.xp >= required_xp

    def _apply_levelup_if_needed(self, user: User) -> None:
        """레벨업 조건을 만족하면 레벨을 올리고 경험치를 차감합니다."""
        while self.is_levelup_condition(user):
            required_xp = user.level * 100
            user.xp -= required_xp
            user.level += 1
            user.hp = 100  # 레벨업 시 체력 100으로 완전 회복
