components = [
    "CPU Intel i7", "CPU Cooler Tower", "GPU RTX 3060", "GPU RTX 4060 Ti",
    "RAM 16GB DDR4", "SSD NVMe 1TB", "HDD 2TB", "Motherboard ATX Gaming",
    "PSU Modular", "RGB Fan Kit"
]
weights = [95, 15, 170, 220, 10, 8, 12, 70, 5, 20]
profits = [85, 20, 120, 150, 30, 25, 18, 60, 12, 22]
capacity = 500


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


max_profit, total_weight, chosen = branch_and_bound(weights, profits, capacity)

print("=== Branch and Bound ===")
print("Performa maksimum:", max_profit)
print("Total daya:", total_weight, "W")
print("Item terpilih:")
for index in chosen:
    print("-", components[index], "(", weights[index], "W,", profits[index], ")")