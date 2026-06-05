from flask import Flask, render_template, redirect, url_for, flash
from src.repositories.UserRepository import UserRepository
from src.repositories.QuestRepository import QuestRepository
from src.services.RpgService import RpgService

app = Flask(__name__)
app.secret_key = "todo_rpg_secret_key" # 플래시 메시지 등을 위해 필요

# 데이터베이스 파일 경로
DB_PATH = "todo_rpg.json"

# Dependency Injection: Repository 및 Service 초기화
user_repo = UserRepository(DB_PATH)
quest_repo = QuestRepository(DB_PATH)
rpg_service = RpgService(user_repo, quest_repo)

@app.route('/')
def index():
    """
    현재 유저 스탯과 진행 중인 퀘스트 목록을 대시보드 형태로 출력합니다.
    """
    user_id = "hero_1" # 기본 유저 ID
    
    # 유저 데이터 조회
    user = user_repo.find_user(user_id)
    user_stats = {
        "level": user.level if user else 1,
        "xp": user.xp if user else 0,
        "hp": user.hp if user else 100,
        "gold": user.gold if user else 0
    }

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

    return render_template('index.html', user_status=user_stats, quests=quests_list)

@app.route('/complete/<quest_id>')
def complete_quest(quest_id):
    """
    특정 퀘스트를 완료 처리합니다.
    """
    user_id = "hero_1"
    try:
        rpg_service.complete_quest(user_id, quest_id)
    except Exception as e:
        print(f"Error completing quest: {e}")
    
    return redirect(url_for('index'))

@app.route('/delete/<quest_id>')
def delete_quest(quest_id):
    """
    특정 퀘스트를 삭제합니다.
    """
    try:
        quest_repo.delete_quest(quest_id)
    except Exception as e:
        print(f"Error deleting quest: {e}")
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Flask 서버 실행
    app.run(debug=True, port=5000)
