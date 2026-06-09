# 🎮 To-Do RPG (갓생 살기를 위한 일상 관리 RPG 시스템)

본 프로젝트는 일상의 할 일을 '퀘스트'로 치환하고 경험치, 레벨, 골드 요소를 도입하여 일상 관리에 몰입감을 더하는 **게이미피케이션(Gamification) 기반 시스템**입니다. 초기 CLI 버전에서 시작하여 현재 Flask 기반의 웹 대시보드 시스템으로 고도화되었습니다.


---

## 📝 프로젝트 개요
지루할 수 있는 To-Do 리스트 관리에 RPG 게임 요소를 접목하여 사용자의 동기부여를 극대화합니다. 할 일을 완료하면 보상을 얻고 레벨업을 하며, 관리하지 못한 할 일은 캐릭터의 생존을 위협하는 패널티로 작용합니다.

### 🌟 핵심 루프
1. **퀘스트 등록**: 오늘 할 일을 난이도(상/중/하)와 함께 등록합니다.
2. **수행 및 보상**: 할 일을 완료하면 난이도에 따른 **XP**와 **Gold**를 획득합니다.
3. **성장 및 소비**: 레벨업을 통해 강해지고, 모은 골드로 상점에서 **셀프 보상**을 구매합니다.
---

## ✨ 주요 기능
- **실시간 대시보드**: 캐릭터의 스탯(Level, XP, HP, Gold)을 시각적인 게이지 바와 카드 UI로 확인.
- **퀘스트 관리 시스템**: 비동기 처리(AJAX)를 통한 퀘스트 등록, 완료, 삭제 기능.
- **스마트 정렬**: 난이도순, 최신순 등 사용자가 원하는 우선순위로 퀘스트 정렬.
- **셀프 보상 상점**: 모은 골드로 '유튜브 보기', '간식 먹기' 등 실제 보상을 구매하는 상호작용.
- **반응형 웹 디자인**: Mobile-First 전략을 적용하여 스마트폰에서도 쾌적한 관리 환경 제공.
- **통합 예외 처리**: 사망 페널티(스탯 초기화) 및 유효성 검사 결과에 대한 실시간 알림 피드백.

---

## 🧱 아키텍처 및 기술적 특징
본 프로젝트는 **Clean Architecture** 원칙을 준수하여 유지보수성과 확장성을 확보했습니다.

- **Layered Architecture**: Model - Repository - Service - UI(Controller) 레이어의 엄격한 분리.
- **O(1) 검색 최적화**: JSON 데이터베이스를 딕셔너리 키 인덱싱으로 관리하여 데이터 규모와 상관없는 일정한 성능 보장.
- **의존성 주입 (DI)**: 각 서비스와 리포지토리를 생성자를 통해 연결하여 계층 간 결합도 최소화.
- **RESTful API**: 백엔드(Flask)와 프론트엔드(Vanilla JS)를 JSON 기반 비동기 API로 연결.

### 🛠️ 기술 스택
- **Backend**: Python 3.10+, Flask, Gunicorn
- **Frontend**: HTML5, CSS3 (Custom Grid/Flexbox), Vanilla JavaScript (ES6+)
- **Data**: JSON (Local DB) -> *PostgreSQL 마이그레이션 예정*
- **Deployment**: Render.com

---

## 📂 프로젝트 구조
```text
todo-rpg-project/
├── app.py               # Flask 웹 서버 진입점 (REST API 컨트롤러)
├── main.py              # (Legacy) CLI 버전 진입점
├── templates/           # UI 템플릿 (index.html)
├── src/
│   ├── models/          # 도메인 모델 (User, Quest 데이터 구조)
│   ├── repositories/    # 데이터 접근 계층 (O(1) 검색 엔진)
│   ├── services/        # 비즈니스 로직 (RpgService, ShopService, Validator)
│   └── exceptions/      # 커스텀 게임 예외 (HeroDeadError 등)
├── requirements.txt     # 파이썬 의존성 목록
├── todo_rpg.json        # 데이터 저장 파일
├── 개발일지.md           # 단계별 개발 상세 기록
├── DEVELOPMENT_LOG.md   # 요약 개발 로그
└── GEMINI.md            # 제미나이 CLI 가이드 컨텍스트
```

---

## 🚀 시작하기

### 1. 로컬 환경 설정
```bash
# 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 실행
```bash
# 웹 서버 실행 
# 서버 실행 후 브라우저에서 `http://127.0.0.1:5000`에 접속합니다.
python3 app.py
``

```bash
# 구버전 CLI 내부 실행 (선택사항)
python3 main.py
```

---

## 🚀 배포

**라이브 데모:** [https://todo-rpg.onrender.com/](https://todo-rpg.onrender.com/)

---


## 📡 API 문서

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | 메인 대시보드 페이지 렌더링 |
| `/api/status` | `GET` | 유저의 현재 스탯(Lv, XP, HP, Gold) 반환 |
| `/api/quests` | `POST` | 새로운 퀘스트 등록 (JSON: `content`, `difficulty`) |
| `/api/quests/<id>/complete` | `POST` | 특정 퀘스트 완료 처리 및 보상 지급 |
| `/api/quests/<id>` | `DELETE` | 특정 퀘스트 삭제 |

---

## 🛠️ 향후 업데이트 계획 (Roadmap)
- [ ] **DB 마이그레이션**: Render 배포 환경의 데이터 영속성을 위한 PostgreSQL 도입.
- [ ] **로컬 스토리지 및 사용자 인증 기반 마련:** 다중 사용자 지원을 위한 초기 설계 및 데이터 영속성 고도화.
- [ ] **다크 모드**: 야간 사용자를 위한 테마 전환 기능.
- [ ] **통계 페이지**: 주간/월간 퀘스트 달성률 및 성장 그래프 시각화.
- [ ] **연속 달성 스트릭**: N일 연속 완료 시 보너스 스탯 부여.
- [ ] **퀘스트 기한**: 퀘스트 완료 기한 설정.
- [ ] **HP 감소**: 퀘스트 기한 내 미완료시 HP감소.
- [ ] **HP 형태 변경**: HP 100을 하트 3개로 변경.
- [ ] **상점 목록 추가**: 상점의 목록을 사용자가 직접 설정하고 구매할 수 있도록 변경.

---