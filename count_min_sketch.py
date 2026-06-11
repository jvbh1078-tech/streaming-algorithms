"""
Count-Min Sketch Implementation
MovieLens 1M 스타일 합성 데이터 스트리밍 처리
"""

import hashlib
import time


class CountMinSketch:
    """
    데이터 스트림 빈도 근사 추정 자료구조
    - 과대추정(Overestimate)은 가능하지만 과소추정(Underestimate)은 없음
    - d x w 2차원 배열, 각 행에 독립 해시 함수 적용
    """

    def __init__(self, w: int, d: int):
        """
        Args:
            w: 폭 (열 개수, 클수록 충돌 감소)
            d: 깊이 (행 개수, 클수록 오차 보정 강화)
        """
        self.w = w
        self.d = d
        self.table = [[0] * w for _ in range(d)]
        self.count = 0

    def _hashes(self, item):
        """MD5 기반 d개의 독립 해시 위치 생성"""
        positions = []
        for i in range(self.d):
            data = f"{i}:{item}".encode('utf-8')
            digest = hashlib.md5(data).hexdigest()
            pos = int(digest, 16) % self.w
            positions.append(pos)
        return positions

    def insert(self, item, delta: int = 1):
        """원소 삽입: d개 행의 해시 위치 카운터 +delta"""
        for row, col in enumerate(self._hashes(item)):
            self.table[row][col] += delta
        self.count += 1

    def query(self, item) -> int:
        """빈도 추정: d개 행의 해시 위치 중 최솟값 반환"""
        return min(self.table[row][col]
                   for row, col in enumerate(self._hashes(item)))

    def memory_kb(self) -> float:
        # 각 int ≈ 28 bytes (Python), 구조 크기 근사
        return (self.d * self.w * 4) / 1024  # 4 bytes per int (C 기준)


class CountMinSketchExperiment:

    def __init__(self, stream):
        self.stream = stream

    def run(self, w: int, d: int, label: str):
        cms = CountMinSketch(w, d)
        ground_truth = {}

        start = time.time()
        for user_id, movie_id, rating in self.stream():
            cms.insert(user_id)
            ground_truth[user_id] = ground_truth.get(user_id, 0) + 1
        elapsed = time.time() - start

        # 평균 상대오차 계산
        errors = []
        for uid, true_count in ground_truth.items():
            est = cms.query(uid)
            rel_error = abs(est - true_count) / true_count
            errors.append(rel_error)
        avg_rel_error = sum(errors) / len(errors) if errors else 0

        n_records = cms.count
        throughput = n_records / elapsed if elapsed > 0 else 0

        print(f"[Count-Min Sketch - {label}]")
        print(f"  w={w}, d={d}")
        print(f"  평균 상대오차  : {avg_rel_error:.4f}")
        print(f"  Memory       : {cms.memory_kb():.1f} KB")
        print(f"  처리 시간     : {elapsed:.2f} s")
        print(f"  처리량        : {throughput:,.0f} rec/s")
        print()

        return {
            'label': label, 'w': w, 'd': d,
            'avg_rel_error': avg_rel_error, 'memory_kb': cms.memory_kb(),
            'elapsed': elapsed, 'throughput': throughput,
        }
