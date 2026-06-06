import uuid
from flask import Flask, render_template, request, jsonify
from src.repositories.UserRepository import UserRepository
from src.repositories.QuestRepository import QuestRepository
from src.services.RpgService import RpgService
from src.services.ShopService import ShopService
from src.services.Validator import Validator
from src.models.quest import Quest
from src.exceptions.GameExceptions import HeroDeadError, InsufficientGoldError

app = Flask(__name__)
app.secret_key = "todo_rpg_secret_key"

# 데이터베이스 파일 경로
DB_PATH = "todo_rpg.json"

# Dependency Injection
user_repo = UserRepository(DB_PATH)
quest_repo = QuestRepository(DB_PATH)
rpg_service = RpgService(user_repo, quest_repo)
shop_service = ShopService(user_repo)

@app.route('/')
def index():
    user_id = "hero_1"
    user = user_repo.find_user(user_id)
    user_stats = {
        "level": user.level if user else 1,
        "xp": user.xp if user else 0,
        "hp": user.hp if user else 100,
        "gold": user.gold if user else 0
    }
    
    all_quests = quest_repo.find_all_quests()
    active_quests = []
    completed_quests = []
    
    for q in all_quests.values():
        quest_data = {
            "quest_id": q.quest_id,
            "content": q.content,
            "difficulty": q.difficulty,
            "is_completed": q.is_finished()
        }
        if quest_data["is_completed"]:
            completed_quests.append(quest_data)
        else:
            active_quests.append(quest_data)
            
    return render_template('index.html', 
                           user_status=user_stats, 
                           active_quests=active_quests, 
                           completed_quests=completed_quests,
                           shop_items=shop_service.get_items())

@app.route('/api/status')
def get_status():
    user_id = "hero_1"
    user = user_repo.find_user(user_id)
    return jsonify({
        "level": user.level if user else 1,
        "xp": user.xp if user else 0,
        "hp": user.hp if user else 100,
        "gold": user.gold if user else 0
    })

@app.route('/api/shop/buy', methods=['POST'])
def buy_item():
    user_id = "hero_1"
    data = request.json
    item_id = data.get('item_id')
    
    try:
        item_name = shop_service.buy_item(user_id, item_id)
        return jsonify({"message": f"'{item_name}' 구매 완료! 즐거운 시간 되세요."})
    except InsufficientGoldError as e:
        return jsonify({"error": str(e)}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/quests', methods=['POST'])
def create_quest():
    data = request.json
    content = data.get('content', '')
    difficulty = data.get('difficulty', '중')
    
    try:
        Validator.validate_quest_content(content)
        Validator.validate_difficulty(difficulty)
        
        new_quest = Quest(
            quest_id=str(uuid.uuid4())[:8],
            content=content,
            difficulty=difficulty
        )
        quest_repo.save_quest(new_quest)
        return jsonify({"message": "퀘스트가 등록되었습니다.", "quest": {
            "quest_id": new_quest.quest_id,
            "content": new_quest.content,
            "difficulty": new_quest.difficulty,
            "is_completed": False
        }}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/quests/<quest_id>/complete', methods=['POST'])
def complete_quest(quest_id):
    user_id = "hero_1"
    try:
        rpg_service.complete_quest(user_id, quest_id)
        return jsonify({"message": "퀘스트 완료! 보상이 지급되었습니다."})
    except HeroDeadError:
        return jsonify({"error": "캐릭터가 사망했습니다! HP를 회복하세요."}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/quests/<quest_id>', methods=['DELETE'])
def delete_quest(quest_id):
    try:
        quest_repo.delete_quest(quest_id)
        return jsonify({"message": "퀘스트가 삭제되었습니다."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
