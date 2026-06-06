from src.repositories.UserRepository import UserRepository
from src.exceptions.GameExceptions import InsufficientGoldError

class ShopService:
    """모은 골드로 셀프 보상을 구매하는 상점 비즈니스 로직을 담당합니다."""

    # 상점 아이템 목록 (id: {이름, 가격})
    ITEMS = {
        "1": {"name": "소설 읽기", "price": 10},
        "2": {"name": "유튜브 30분 보기", "price": 20},
        "3": {"name": "맛있는 배달 음식", "price": 300}
    }

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_items(self) -> dict:
        """상점 아이템 목록을 반환합니다."""
        return self.ITEMS

    def buy_item(self, user_id: str, item_id: str) -> str:
        """아이템을 구매하고 골드를 차감합니다."""
        user = self.user_repo.find_user(user_id)
        if not user:
            raise ValueError("사용자를 찾을 수 없습니다.")

        item = self.ITEMS.get(item_id)
        if not item:
            raise ValueError("존재하지 않는 아이템입니다.")

        # User 모델의 spend_gold가 골드 부족 시 InsufficientGoldError를 발생시킵니다.
        user.spend_gold(item["price"])
        self.user_repo.save_user(user_id, user)
        
        return item["name"]
