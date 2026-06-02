"""
게임 내 특수 상황(골드 부족, 체력 고갈 등)을 안전하게 제어하기 위한 커스텀 예외 모음입니다.
"""

class InsufficientGoldError(Exception):
    """
    아이템 구매나 이벤트 등에서 골드가 부족할 경우 발생하는 예외입니다.
    """
    def __init__(self, message: str = "골드가 부족하여 해당 작업을 수행할 수 없습니다."):
        self.message = message
        super().__init__(self.message)


class HeroDeadError(Exception):
    """
    퀘스트 실패나 데미지를 입어 체력(HP)이 0 이하가 되었을 때 발생하는 예외입니다.
    """
    def __init__(self, message: str = "체력이 0이 되어 캐릭터가 쓰러졌습니다."):
        self.message = message
        super().__init__(self.message)
