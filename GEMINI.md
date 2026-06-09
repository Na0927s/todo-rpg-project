# Gemini AI Assistant Guidelines for To-Do RPG

## 🎯 프로젝트 컨텍스트
- **개발자:** 컴퓨터소프트웨어공학과 3학년 나민주
- **목적:** Python 3 내장 라이브러리만을 활용한 고품질 아키텍처 기반 CLI 투두RPG 개발

## 🧱 코드 품질 지표 및 제약 사항
1. **클래스/함수 분리:** 하나의 파일에 로직을 몰아넣지 말고 명확한 레이어(Model-Repository-Service-UI)로 분리할 것.
2. **함수 길이 제약:** 모든 함수의 길이는 30줄 이하, 순환 복잡도(Cyclomatic Complexity)는 10 이하를 유지할 것.
3. **네이밍 컨벤션:** - 변수명: 약어 금지, 형태를 명확히 서술 (`user_id`, `quest_id`)
   - 함수명: 동사로 시작 (`create_quest`, `validate_input`)
   - Boolean 함수: `is_`, `has_`, `can_` 접두사 필수 (`is_levelup_condition`, `can_afford_item`)
   - 상수: 스네이크 대문자 (`MAX_HP = 100`)
4. **데이터 접근:** 데이터 파일(`todo_rpg.json`)은 Repository 레이어에서만 접근하며, 리스트 순회 O(n)가 아닌 딕셔너리 키 인덱싱을 통한 O(1) 검색을 구현할 것.
5. **예외 처리:** 예외 상황은 `src/exceptions/`에 정의된 커스텀 에러를 발생시켜 `try-except` 구조로 안전하게 제어할 것.
