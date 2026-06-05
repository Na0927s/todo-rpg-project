from flask import Flask, jsonify
from src.repositories.UserRepository import UserRepository
from src.repositories.QuestRepository import QuestRepository
from src.services.RpgService import RpgService

app = Flask(__name__)

# 데이터베이스 파일 경로
DB_PATH = "todo_rpg.json"

# Dependency Injection: Repository 및 Service 초기화
user_repo = UserRepository(DB_PATH)
quest_repo = QuestRepository(DB_PATH)
rpg_service = RpgService(user_repo, quest_repo)

@app.route('/', methods=['GET'])
def get_game_status():
    """
    현재 유저 스탯과 진행 중인 퀘스트 목록을 JSON 형태로 반환합니다.
    """
    # 기본 유저 ID (기존 todo_rpg.json의 hero_1 사용)
    user_id = "hero_1"
    
    # 유저 데이터 조회
    user = user_repo.find_user(user_id)
    user_stats = {
        "level": user.level,
        "xp": user.xp,
        "hp": user.hp,
        "gold": user.gold
    } if user else {}

    # 퀘스트 목록 조회
    all_quests = quest_repo.find_all_quests()
    quests_list = []
    for q_id, q in all_quests.items():
        quests_list.append({
            "quest_id": q.quest_id,
            "content": q.content,
            "difficulty": q.difficulty,
            "is_completed": q.is_finished()
        })

    return jsonify({
        "user_status": user_stats,
        "quests": quests_list
    })

if __name__ == '__main__':
    # Flask 서버 실행
    app.run(debug=True, port=5000)
