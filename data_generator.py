"""
MovieLens 1M 스타일 합성 스트리밍 데이터 생성기
- 사용자 ID: 1 ~ 6,040
- 영화 ID:   1 ~ 3,952
- 평점:      1.0 ~ 5.0 (0.5 단위)
- 레코드 수: 1,000,000
"""

import random
from typing import Generator, Tuple


def stream_generator(
    n_records: int = 1_000_000,
    n_users: int = 6_040,
    n_movies: int = 3_952,
    seed: int = 42
) -> Generator[Tuple[int, int, float], None, None]:
    """
    스트리밍 데이터 제너레이터 (전체 데이터를 메모리에 올리지 않음)

    Yields:
        (user_id, movie_id, rating) 튜플
    """
    rng = random.Random(seed)
    ratings = [r / 2 for r in range(2, 11)]  # 1.0 ~ 5.0, 0.5 단위

    for _ in range(n_records):
        user_id = rng.randint(1, n_users)
        movie_id = rng.randint(1, n_movies)
        rating = rng.choice(ratings)
        yield user_id, movie_id, rating


def get_stream(n_records: int = 1_000_000, seed: int = 42):
    """실험용 스트림 팩토리 함수"""
    def _stream():
        return stream_generator(n_records=n_records, seed=seed)
    return _stream
