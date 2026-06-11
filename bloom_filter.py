"""
Bloom Filter Implementation
MovieLens 1M 스타일 합성 데이터 스트리밍 처리
"""

import hashlib
import math
import time


class BloomFilter:
    """
    확률적 집합 자료구조: 원소 포함 여부 근사 판정
    - False Negative: 없음 (있는 원소를 없다고 판정하지 않음)
    - False Positive: 비트 배열 포화도에 따라 발생 가능
    """

    def __init__(self, m: int, k: int):
        """
        Args:
            m: 비트 배열 크기
            k: 해시 함수 개수
        """
        self.m = m
        self.k = k
        self.bit_array = bytearray(math.ceil(m / 8))
        self.count = 0

    def _hashes(self, item):
        """MD5 기반 k개의 독립 해시 위치 생성"""
        positions = []
        for i in range(self.k):
            data = f"{i}:{item}".encode('utf-8')
            digest = hashlib.md5(data).hexdigest()
            pos = int(digest, 16) % self.m
            positions.append(pos)
        return positions

    def _set_bit(self, pos):
        byte_idx = pos // 8
        bit_idx = pos % 8
        self.bit_array[byte_idx] |= (1 << bit_idx)

    def _get_bit(self, pos) -> bool:
        byte_idx = pos // 8
        bit_idx = pos % 8
        return bool(self.bit_array[byte_idx] & (1 << bit_idx))

    def insert(self, item):
        """원소 삽입: k개 해시 위치를 모두 1로 설정"""
        for pos in self._hashes(item):
            self._set_bit(pos)
        self.count += 1

    def query(self, item) -> bool:
        """포함 여부 조회: k개 위치가 모두 1이면 True"""
        return all(self._get_bit(pos) for pos in self._hashes(item))

    def memory_kb(self) -> float:
        return len(self.bit_array) / 1024


class BloomFilterExperiment:

    def __init__(self, stream, n_test=1000):
        self.stream = stream
        self.n_test = n_test

    def run(self, m: int, k: int, label: str):
        bf = BloomFilter(m, k)
        ground_truth = set()

        start = time.time()
        for user_id, movie_id, rating in self.stream():
            bf.insert(user_id)
            ground_truth.add(user_id)
        elapsed = time.time() - start

        # False Positive Rate 측정
        max_id = max(ground_truth)
        test_items = range(max_id + 1, max_id + 1 + self.n_test)
        fp = sum(1 for x in test_items if bf.query(x))
        fpr = fp / self.n_test

        n_records = bf.count
        throughput = n_records / elapsed if elapsed > 0 else 0

        print(f"[Bloom Filter - {label}]")
        print(f"  m={m:,}, k={k}")
        print(f"  FPR          : {fpr:.4f}")
        print(f"  Memory       : {bf.memory_kb():.1f} KB")
        print(f"  처리 시간     : {elapsed:.2f} s")
        print(f"  처리량        : {throughput:,.0f} rec/s")
        print()

        return {
            'label': label, 'm': m, 'k': k,
            'fpr': fpr, 'memory_kb': bf.memory_kb(),
            'elapsed': elapsed, 'throughput': throughput,
        }
