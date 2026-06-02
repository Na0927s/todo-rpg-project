from typing import Optional
from src.models.user import User
from src.repositories.BaseRepository import BaseRepository

class UserRepository(BaseRepository):
    """
    todo_rpg.json 파일과 연동하여 사용자 데이터를 O(1) 성능으로 조회 및 저장하는 리포지토리입니다.
    """
    
    def find_user(self, user_id: str) -> Optional[User]:
        """user_id를 딕셔너리 키로 사용하여 O(1)로 사용자를 조회합니다."""
        data = self._load_data()
        users_dict = data.get("users", {})
        
        user_data = users_dict.get(user_id)
        if not user_data:
            return None
            
        return User(
            level=user_data.get("level", 1),
            xp=user_data.get("xp", 0),
            hp=user_data.get("hp", 100),
            gold=user_data.get("gold", 0)
        )

    def save_user(self, user_id: str, user: User) -> None:
        """사용자 객체를 딕셔너리에 O(1)로 업데이트 후 파일에 저장합니다."""
        data = self._load_data()
        
        if "users" not in data:
            data["users"] = {}
            
        data["users"][user_id] = {
            "level": user.level,
            "xp": user.xp,
            "hp": user.hp,
            "gold": user.gold
        }
        
        self._save_data(data)
