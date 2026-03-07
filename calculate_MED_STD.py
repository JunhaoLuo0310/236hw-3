import time
import os
import psutil
from math import sqrt
from collections import defaultdict, Counter


def get_process_memory():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024


def get_median_from_counter(counter, n):
    items = sorted(counter.items())   # (temp_in_tenths, frequency)

    if n % 2 == 1:
        target = n // 2 + 1
        running = 0
        for temp10, freq in items:
            running += freq
            if running >= target:
                return temp10 / 10.0
    else:
        left_target = n // 2
        right_target = n // 2 + 1
        running = 0
        left_value = None
        right_value = None

        for temp10, freq in items:
            running += freq
            if left_value is None and running >= left_target:
                left_value = temp10
            if right_value is None and running >= right_target:
                right_value = temp10
                break

        return (left_value + right_value) / 20.0


def calculate_median_std():
    start_time = time.time()
    start_memory = get_process_memory()

    # per-station stats
    counts = defaultdict(int)
    sums = defaultdict(int)       # store temperature * 10
    sums_sq = defaultdict(int)    # store (temperature * 10)^2
    freq_tables = defaultdict(Counter)

    with open("measurements.txt", "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            station, temp_str = line.strip().split(";")

            # convert to integer tenths, e.g. 18.3 -> 183
            temp10 = int(round(float(temp_str) * 10))

            counts[station] += 1
            sums[station] += temp10
            sums_sq[station] += temp10 * temp10
            freq_tables[station][temp10] += 1

            if line_num % 10_000_000 == 0:
                print(f"Processed {line_num:,} rows...", flush=True)

    results = {}

    for station in counts:
        n = counts[station]

        median = get_median_from_counter(freq_tables[station], n)

        mean10 = sums[station] / float(n)
        variance10 = sums_sq[station] / float(n) - mean10 * mean10
        std = sqrt(max(variance10, 0)) / 10.0

        results[station] = (median, std)

    end_time = time.time()
    end_memory = get_process_memory()

    return results, end_time - start_time, end_memory - start_memory


if __name__ == "__main__":
    results, elapsed_time, memory_delta = calculate_median_std()

    output_parts = []
    for station in sorted(results.keys()):
        median, std = results[station]
        output_parts.append(f"{station}={median:.1f}/{std:.1f}")

    output_str = "{" + ", ".join(output_parts) + "}"
    print(output_str)

    print("\n--- Performance Metrics ---")
    print(f"Time: {elapsed_time:.2f} seconds")
    print(f"Memory usage: {memory_delta:.2f} MB")