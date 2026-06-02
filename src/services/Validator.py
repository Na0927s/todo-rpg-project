class Validator:
    """사용자 입력값을 검증하는 유틸리티 클래스입니다."""

    @staticmethod
    def validate_quest_content(content: str) -> None:
        """퀘스트 내용이 공백이 아닌지 검증합니다."""
        if not content or not content.strip():
            raise ValueError("퀘스트 내용은 공백일 수 없습니다.")

    @staticmethod
    def validate_difficulty(difficulty: str) -> None:
        """난이도 입력이 올바른지 검증합니다."""
        valid_difficulties = ["상", "중", "하"]
        if difficulty not in valid_difficulties:
            raise ValueError(f"난이도는 {', '.join(valid_difficulties)} 중 하나여야 합니다.")
