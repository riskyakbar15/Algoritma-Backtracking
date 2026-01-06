def knapsack_dp(weights, profits, W):
    n = len(weights)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + profits[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    w = W
    chosen = []
    total_weight = 0
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            idx = i - 1
            chosen.append(idx)
            total_weight += weights[idx]
            w -= weights[idx]

    chosen.reverse()
    return dp[n][W], chosen, total_weight


components = [
    "CPU Intel i7", "CPU Cooler Tower", "GPU RTX 3060", "GPU RTX 4060 Ti",
    "RAM 16GB DDR4", "SSD NVMe 1TB", "HDD 2TB", "Motherboard ATX Gaming",
    "PSU Modular", "RGB Fan Kit"
]
weights  = [95, 15, 170, 220, 10, 8, 12, 70, 5, 20]
profits  = [85, 20, 120, 150, 30, 25, 18, 60, 12, 22]
W = 500

max_profit, chosen, total_w = knapsack_dp(weights, profits, W)

print("=== Dynamic Programming ===")
print("Performa maksimum:", max_profit)
print("Total daya:", total_w, "W")
print("Item terpilih:")
for i in chosen:
    print("-", components[i], "(", weights[i], "W,", profits[i], ")")
