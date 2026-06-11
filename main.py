"""
스트리밍 알고리즘 실험 메인 스크립트
Bloom Filter & Count-Min Sketch 파라미터 비교 실험
"""

from data_generator import get_stream
from bloom_filter import BloomFilterExperiment
from count_min_sketch import CountMinSketchExperiment

N_RECORDS = 1_000_000
SEED = 42


def run_bloom_filter_experiments():
    print("=" * 50)
    print("Bloom Filter 파라미터 비교 실험")
    print("=" * 50)

    stream = get_stream(N_RECORDS, SEED)
    exp = BloomFilterExperiment(stream, n_test=1000)

    configs = [
        (500_000,   3, "Small"),
        (1_000_000, 5, "Medium"),
        (2_000_000, 7, "Large"),
    ]

    results = []
    for m, k, label in configs:
        result = exp.run(m, k, label)
        results.append(result)

    return results


def run_count_min_sketch_experiments():
    print("=" * 50)
    print("Count-Min Sketch 파라미터 비교 실험")
    print("=" * 50)

    stream = get_stream(N_RECORDS, SEED)
    exp = CountMinSketchExperiment(stream)

    configs = [
        (500,  3, "Small"),
        (1000, 5, "Medium"),
        (2000, 7, "Large"),
    ]

    results = []
    for w, d, label in configs:
        result = exp.run(w, d, label)
        results.append(result)

    return results


def print_summary(bf_results, cms_results):
    print("=" * 50)
    print("결과 요약")
    print("=" * 50)

    print("\n[Bloom Filter]")
    print(f"{'설정':<10} {'m':>12} {'k':>4} {'FPR':>8} {'Memory(KB)':>12} {'처리량':>12}")
    print("-" * 60)
    for r in bf_results:
        print(f"{r['label']:<10} {r['m']:>12,} {r['k']:>4} "
              f"{r['fpr']:>8.4f} {r['memory_kb']:>12.1f} {r['throughput']:>12,.0f}")

    print("\n[Count-Min Sketch]")
    print(f"{'설정':<10} {'w':>6} {'d':>4} {'평균오차':>10} {'Memory(KB)':>12} {'처리량':>12}")
    print("-" * 60)
    for r in cms_results:
        print(f"{r['label']:<10} {r['w']:>6} {r['d']:>4} "
              f"{r['avg_rel_error']:>10.4f} {r['memory_kb']:>12.1f} {r['throughput']:>12,.0f}")


if __name__ == "__main__":
    bf_results = run_bloom_filter_experiments()
    cms_results = run_count_min_sketch_experiments()
    print_summary(bf_results, cms_results)
