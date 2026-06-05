import os
import time
import uuid
import sys
from typing import Dict, Optional

from src.repositories.UserRepository import UserRepository
from src.repositories.QuestRepository import QuestRepository
from src.services.RpgService import RpgService
from src.services.ShopService import ShopService
from src.services.Validator import Validator
from src.exceptions.GameExceptions import InsufficientGoldError, HeroDeadError
from src.models.user import User
from src.models.quest import Quest

# 고정 설정값
USER_ID = "hero_1"
DATA_FILE = "todo_rpg.json"

def clear_screen() -> None:
    """터미널 화면을 깨끗하게 비웁니다."""
    os.system("clear")

def draw_gauge(current: int, maximum: int, length: int = 10) -> str:
    """HP 또는 XP의 가시성 높은 게이지 바를 생성합니다."""
    if maximum <= 0:
        return "□" * length
    filled_ratio = min(current / maximum, 1.0)
    filled_length = int(filled_ratio * length)
    return "■" * filled_length + "□" * (length - filled_length)

def render_status(user: User) -> None:
    """유저의 레벨, HP, XP, 골드 상태창을 대시보드 형태로 출력합니다."""
    max_xp = user.level * 100
    hp_bar = draw_gauge(user.hp, 100)
    xp_bar = draw_gauge(user.xp, max_xp)

    print("=" * 50)
    print(f" 🛡️  Lv.{user.level} 용사 상태창 | 💰 {user.gold} Gold")
    print(f" HP: [{hp_bar}] {user.hp}/100")
    print(f" XP: [{xp_bar}] {user.xp}/{max_xp}")
    print("=" * 50)

def render_quests(quest_repo: QuestRepository) -> None:
    """현재 등록된 퀘스트 목록을 출력합니다."""
    quests = quest_repo.find_all_quests()
    print("\n📜 [일일 퀘스트 목록]")
    if not quests:
        print("  등록된 퀘스트가 없습니다. 새로운 할 일을 추가해보세요!")
    else:
        for idx, (q_id, quest) in enumerate(quests.items(), 1):
            status = "✅ 완료" if quest.is_finished() else "⏳ 진행중"
            print(f"  {idx}. [{status}] ({quest.difficulty}) {quest.content} [ID: {q_id[:6]}]")
    print("-" * 50)

def handle_add_quest(quest_repo: QuestRepository) -> None:
    """새로운 퀘스트를 안전하게 입력받아 등록합니다."""
    try:
        content = input("➕ 퀘스트 내용을 입력하세요: ").strip()
        Validator.validate_quest_content(content)
        difficulty = input("🔥 난이도(상/중/하): ").strip()
        Validator.validate_difficulty(difficulty)
        
        quest_id = str(uuid.uuid4())[:8]
        quest_repo.save_quest(Quest(quest_id, content, difficulty))
        print("🎉 퀘스트가 성공적으로 등록되었습니다!")
    except (ValueError, Exception) as e:
        print(f"❌ 입력 오류: {e}")
    time.sleep(1)

def handle_complete_quest(rpg_service: RpgService, quest_repo: QuestRepository) -> None:
    """ID 앞자리를 통해 퀘스트를 완료 처리하고 보상을 지급합니다."""
    try:
        prefix = input("✅ 완료할 퀘스트 ID 앞자리를 입력하세요: ").strip()
        quests = quest_repo.find_all_quests()
        target_id = next((q_id for q_id in quests if q_id.startswith(prefix)), None)
        
        if not target_id:
            raise ValueError("일치하는 퀘스트 ID를 찾을 수 없습니다.")
            
        rpg_service.complete_quest(USER_ID, target_id)
        print("🎊 퀘스트 완료! 경험치와 골드를 획득했습니다.")
    except (ValueError, Exception) as e:
        print(f"❌ 오류: {e}")
    time.sleep(1)

def handle_delete_quest(quest_repo: QuestRepository) -> None:
    """ID 앞자리를 통해 퀘스트를 목록에서 삭제합니다."""
    try:
        prefix = input("🗑️ 삭제할 퀘스트 ID 앞자리를 입력하세요: ").strip()
        quests = quest_repo.find_all_quests()
        target_id = next((q_id for q_id in quests if q_id.startswith(prefix)), None)
        
        if not target_id:
            raise ValueError("일치하는 퀘스트 ID를 찾을 수 없습니다.")
            
        quest_repo.delete_quest(target_id)
        print("🗑️ 퀘스트가 삭제되었습니다.")
    except (ValueError, Exception) as e:
        print(f"❌ 오류: {e}")
    time.sleep(1)

def handle_shop(shop_service: ShopService) -> None:
    """상점에서 셀프 보상 아이템을 구매합니다."""
    clear_screen()
    print("🏪 [셀프 보상 상점]\n" + "=" * 50)
    items = shop_service.get_items()
    for i_id, info in items.items():
        print(f"  [{i_id}] {info['name']} - 💰 {info['price']} Gold")
    
    try:
        choice = input("\n🎁 구매할 아이템 번호(0: 돌아가기): ").strip()
        if choice == '0':
            return
        item_name = shop_service.buy_item(USER_ID, choice)
        print(f"✨ '{item_name}' 구매 완료! 고생한 자신에게 상을 주세요.")
    except (InsufficientGoldError, ValueError, Exception) as e:
        print(f"❌ 상점 이용 오류: {e}")
    time.sleep(1.5)

def run_menu_action(choice: str, svcs: dict) -> bool:
    """사용자의 메뉴 선택에 따른 핸들러를 실행합니다."""
    if choice == '1':
        handle_add_quest(svcs['q_repo'])
    elif choice == '2':
        handle_complete_quest(svcs['rpg_svc'], svcs['q_repo'])
    elif choice == '3':
        handle_delete_quest(svcs['q_repo'])
    elif choice == '4':
        handle_shop(svcs['shop_svc'])
    elif choice == '5':
        print("게임을 종료합니다. 갓생을 응원합니다!")
        return False
    else:
        print("❌ 잘못된 메뉴 선택입니다. 1~5 사이의 숫자를 입력하세요.")
        time.sleep(1)
    return True

def main() -> None:
    """투두RPG의 메인 진입점 및 무한 루프 제어"""
    u_repo, q_repo = UserRepository(DATA_FILE), QuestRepository(DATA_FILE)
    svcs = {
        'q_repo': q_repo,
        'rpg_svc': RpgService(u_repo, q_repo),
        'shop_svc': ShopService(u_repo)
    }

    while True:
        try:
            user = u_repo.find_user(USER_ID) or User()
            if not u_repo.find_user(USER_ID):
                u_repo.save_user(USER_ID, user)
            
            clear_screen()
            render_status(user)
            render_quests(q_repo)
            print("1. 추가 | 2. 완료 | 3. 삭제 | 4. 상점 | 5. 종료")
            
            menu_input = input("\n메뉴 선택: ").strip()
            if not run_menu_action(menu_input, svcs):
                break
        except HeroDeadError as e:
            print(f"\n💀 GAME OVER: {e}\n체력이 모두 소진되었습니다. 다시 힘내보아요!")
            break
        except KeyboardInterrupt:
            print("\n👋 프로그램을 종료합니다."); sys.exit(0)
        except Exception as e:
            print(f"⚠️ 시스템 오류 발생: {e}"); time.sleep(1.5)

if __name__ == "__main__":
    main()
