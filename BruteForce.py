from itertools import combinations

components = [
    "CPU Intel i7", "CPU Cooler Tower", "GPU RTX 3060", "GPU RTX 4060 Ti",
    "RAM 16GB DDR4", "SSD NVMe 1TB", "HDD 2TB", "Motherboard ATX Gaming",
    "PSU Modular", "RGB Fan Kit"
]
weights  = [95, 15, 170, 220, 10, 8, 12, 70, 5, 20]
profits  = [85, 20, 120, 150, 30, 25, 18, 60, 12, 22]
W = 500

best_profit = 0
best_comb = []
best_weight = 0
n = len(weights)

for r in range(1, n + 1):
    for comb in combinations(range(n), r):
        total_w = sum(weights[i] for i in comb)
        total_p = sum(profits[i] for i in comb)

        if total_w <= W and total_p > best_profit:
            best_profit = total_p
            best_comb = list(comb)
            best_weight = total_w

print("=== Brute Force ===")
print("Performa maksimum:", best_profit)
print("Total daya:", best_weight, "W")
print("Item terpilih:")
for i in best_comb:
    print("-", components[i], "(", weights[i], "W,", profits[i], ")")

print("\nTotal kombinasi yang diperiksa:", 2**n)
