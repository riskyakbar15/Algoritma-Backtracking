components = [
    "CPU Intel i7", "CPU Cooler Tower", "GPU RTX 3060", "GPU RTX 4060 Ti",
    "RAM 16GB DDR4", "SSD NVMe 1TB", "HDD 2TB", "Motherboard ATX Gaming",
    "PSU Modular", "RGB Fan Kit"
]
weights = [95, 15, 170, 220, 10, 8, 12, 70, 5, 20]
profits = [85, 20, 120, 150, 30, 25, 18, 60, 12, 22]
capacity = 500


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


def meet_in_the_middle(weights, profits, capacity):
    n = len(weights)
    mid = n // 2
    left_indices = list(range(mid))
    right_indices = list(range(mid, n))

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


max_profit, total_weight, chosen = meet_in_the_middle(weights, profits, capacity)

print("=== Meet in the Middle ===")
print("Performa maksimum:", max_profit)
print("Total daya:", total_weight, "W")
print("Item terpilih:")
for index in chosen:
    print("-", components[index], "(", weights[index], "W,", profits[index], ")")