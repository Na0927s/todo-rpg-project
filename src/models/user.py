"""
투두RPG의 사용자(캐릭터) 상태를 관리하는 도메인 모델 클래스입니다.
"""
from src.exceptions.GameExceptions import InsufficientGoldError, HeroDeadError


class User:
    """
    사용자의 레벨(Lv), 경험치(XP), 체력(HP), 골드(Gold) 스탯 구조를 정의합니다.
    """

    def __init__(self, level: int = 1, xp: int = 0, hp: int = 100, gold: int = 0):
        self.level = level
        self.xp = xp
        self.hp = hp
        self.gold = gold

    def is_dead(self) -> bool:
        """
        사용자의 체력이 0 이하인지 확인합니다.
        """
        return self.hp <= 0

    def decrease_hp(self, amount: int) -> None:
        """
        체력을 감소시킵니다. 체력이 0 이하가 되면 HeroDeadError를 발생시킵니다.
        """
        self.hp -= amount
        if self.is_dead():
            self.hp = 0
            raise HeroDeadError()

    def add_xp(self, amount: int) -> None:
        """
        경험치를 추가합니다. 레벨업 로직은 서비스 레이어에서 처리하도록 합니다.
        """
        self.xp += amount

    def spend_gold(self, amount: int) -> None:
        """
        골드를 소모합니다. 보유한 골드보다 많은 양을 소모하려 하면 예외를 발생시킵니다.
        """
        if self.gold < amount:
            raise InsufficientGoldError()
        self.gold -= amount

    def add_gold(self, amount: int) -> None:
        """
        골드를 획득합니다.
        """
        self.gold += amount
