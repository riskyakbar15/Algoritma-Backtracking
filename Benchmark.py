import time
import random
import itertools


components = [
    "CPU Intel i7", "CPU Cooler Tower", "GPU RTX 3060", "GPU RTX 4060 Ti",
    "RAM 16GB DDR4", "SSD NVMe 1TB", "HDD 2TB", "Motherboard ATX Gaming",
    "PSU Modular", "RGB Fan Kit"
]
weights = [95, 15, 170, 220, 10, 8, 12, 70, 5, 20]
profits = [85, 20, 120, 150, 30, 25, 18, 60, 12, 22]
capacity = 500


def brute_force(weights, profits, capacity):
    n = len(weights)
    best_profit = 0
    best_weight = 0
    best_comb = []

    for r in range(1, n + 1):
        for comb in itertools.combinations(range(n), r):
            total_w = sum(weights[i] for i in comb)
            total_p = sum(profits[i] for i in comb)
            if total_w <= capacity and total_p > best_profit:
                best_profit = total_p
                best_comb = list(comb)
                best_weight = total_w

    return best_profit, best_weight, best_comb


def knapsack_dp(weights, profits, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + profits[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    w = capacity
    chosen = []
    total_weight = 0
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            idx = i - 1
            chosen.append(idx)
            total_weight += weights[idx]
            w -= weights[idx]

    chosen.reverse()
    return dp[n][capacity], chosen, total_weight


def branch_and_bound(weights, profits, capacity):
    items = []
    for index, (weight, profit) in enumerate(zip(weights, profits)):
        ratio = profit / weight
        items.append((index, weight, profit, ratio))

    items.sort(key=lambda item: (-item[3], item[1], item[0]))

    best_profit = 0
    best_weight = 0
    best_taken = []

    def bound(level, current_weight, current_profit):
        if current_weight >= capacity:
            return current_profit

        estimate = current_profit
        total_weight = current_weight

        for i in range(level, len(items)):
            _, item_weight, item_profit, _ = items[i]
            if total_weight + item_weight <= capacity:
                total_weight += item_weight
                estimate += item_profit
            else:
                remaining = capacity - total_weight
                estimate += item_profit * (remaining / item_weight)
                break

        return estimate

    def search(level, current_weight, current_profit, taken):
        nonlocal best_profit, best_weight, best_taken

        if current_weight <= capacity:
            is_better = current_profit > best_profit or (
                current_profit == best_profit and current_weight < best_weight
            )
            if is_better:
                best_profit = current_profit
                best_weight = current_weight
                best_taken = taken[:]

        if level == len(items):
            return

        if bound(level, current_weight, current_profit) <= best_profit:
            return

        original_index, item_weight, item_profit, _ = items[level]

        if current_weight + item_weight <= capacity:
            taken.append(original_index)
            search(
                level + 1,
                current_weight + item_weight,
                current_profit + item_profit,
                taken,
            )
            taken.pop()

        search(level + 1, current_weight, current_profit, taken)

    search(0, 0, 0, [])
    best_taken.sort()
    return best_profit, best_weight, best_taken


def meet_in_the_middle(weights, profits, capacity):
    n = len(weights)
    mid = n // 2
    left_indices = list(range(mid))
    right_indices = list(range(mid, n))

    def enumerate_subsets(indices):
        subsets = []
        total = 1 << len(indices)
        for mask in range(total):
            subset_weight = 0
            subset_profit = 0
            chosen = []
            for bit, index in enumerate(indices):
                if mask & (1 << bit):
                    subset_weight += weights[index]
                    subset_profit += profits[index]
                    chosen.append(index)
            if subset_weight <= capacity:
                subsets.append((subset_weight, subset_profit, chosen))
        return subsets

    left_subsets = enumerate_subsets(left_indices)
    right_subsets = enumerate_subsets(right_indices)
    right_subsets.sort(key=lambda item: (item[0], -item[1]))

    filtered_right = []
    best_profit_so_far = -1
    for subset_weight, subset_profit, subset_indices in right_subsets:
        if subset_profit > best_profit_so_far:
            filtered_right.append((subset_weight, subset_profit, subset_indices))
            best_profit_so_far = subset_profit

    right_weights = [subset[0] for subset in filtered_right]

    best_profit = 0
    best_weight = 0
    best_taken = []

    def update_best(total_weight, total_profit, chosen_indices):
        nonlocal best_profit, best_weight, best_taken
        if total_weight <= capacity:
            is_better = total_profit > best_profit or (
                total_profit == best_profit and total_weight < best_weight
            )
            if is_better:
                best_profit = total_profit
                best_weight = total_weight
                best_taken = chosen_indices[:]

    for left_weight, left_profit, left_indices_chosen in left_subsets:
        remaining_capacity = capacity - left_weight
        if remaining_capacity < 0:
            continue

        low = 0
        high = len(right_weights) - 1
        best_right_index = -1
        while low <= high:
            middle = (low + high) // 2
            if right_weights[middle] <= remaining_capacity:
                best_right_index = middle
                low = middle + 1
            else:
                high = middle - 1

        if best_right_index != -1:
            right_weight, right_profit, right_indices_chosen = filtered_right[best_right_index]
            update_best(
                left_weight + right_weight,
                left_profit + right_profit,
                left_indices_chosen + right_indices_chosen,
            )
        else:
            update_best(left_weight, left_profit, left_indices_chosen)

    best_taken.sort()
    return best_profit, best_weight, best_taken


def run_benchmark(trials=5):
    algos = [
        ("Brute Force", brute_force),
        ("Dynamic Programming", knapsack_dp),
        ("Branch and Bound", branch_and_bound),
        ("Meet-in-the-Middle", meet_in_the_middle),
    ]

    results = {}
    def normalize_result(res):
        # Normalize varied return shapes to (profit, weight, chosen_list)
        if not isinstance(res, tuple) or len(res) != 3:
            raise ValueError("Algorithm must return a 3-tuple")

        a, b, c = res
        # find the list element (chosen indices)
        chosen = None
        profit = None
        weight = None

        for x in (a, b, c):
            if isinstance(x, list):
                chosen = x

        # remaining two should be ints (profit and weight)
        ints = [x for x in (a, b, c) if not isinstance(x, list)]
        if len(ints) != 2:
            # fallback: try to coerce
            ints = [x for x in (a, b, c) if isinstance(x, (int,))]

        if chosen is None or len(ints) != 2:
            raise ValueError("Cannot normalize result from algorithm: %r" % (res,))

        # determine which int is profit (larger is profit generally) but use positions
        p, w = ints[0], ints[1]
        # profit should be >= 0 and weight <= capacity
        if w <= capacity and p >= 0:
            profit, weight = p, w
        else:
            profit, weight = w, p

        return profit, weight, chosen

    for name, func in algos:
        times = []
        last_result = None
        for _ in range(trials):
            start = time.perf_counter()
            res = func(weights, profits, capacity)
            end = time.perf_counter()
            times.append(end - start)
            last_result = res

        avg_time = sum(times) / len(times)
        try:
            profit, w, chosen = normalize_result(last_result)
        except Exception as e:
            print(f"Failed to normalize result for {name}:", e)
            profit, w, chosen = None, None, []

        results[name] = (avg_time, (profit, w, chosen))

    print("\n=== Benchmark Results (average over", trials, "runs) ===")
    for name, (t, res) in results.items():
        profit, w, chosen = res
        items_count = len(chosen) if isinstance(chosen, list) else 0
        print(f"{name}: avg time = {t:.6f}s, profit = {profit}, weight = {w}, items = {items_count}")

    # consistency check
    profits_set = set(results[name][1][0] for name in results)
    if len(profits_set) == 1:
        print("\nAll algorithms agree on optimal profit:", profits_set.pop())
    else:
        print("\nDiscrepancy detected between algorithms: profits ->",
              {name: results[name][1][0] for name in results})


if __name__ == "__main__":
    print("Running benchmark on sample case:")
    run_benchmark(trials=5)
