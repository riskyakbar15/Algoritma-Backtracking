def prompt_int(message, minimum=None):
    while True:
        raw_value = input(message).strip()
        try:
            value = int(raw_value)
            if minimum is not None and value < minimum:
                print(f"Masukkan angka minimal {minimum}.")
                continue
            return value
        except ValueError:
            print("Masukkan bilangan bulat yang valid.")


def prompt_item(index):
    print(f"\nKomponen ke-{index + 1}")
    name = input("Nama komponen: ").strip()
    while not name:
        print("Nama komponen tidak boleh kosong.")
        name = input("Nama komponen: ").strip()

    weight = prompt_int("Daya / bobot: ", minimum=0)
    profit = prompt_int("Performa / nilai: ", minimum=0)
    return name, weight, profit


def knapsack_dp(weights, profits, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for current_capacity in range(capacity + 1):
            if weights[i - 1] <= current_capacity:
                dp[i][current_capacity] = max(
                    dp[i - 1][current_capacity],
                    dp[i - 1][current_capacity - weights[i - 1]] + profits[i - 1],
                )
            else:
                dp[i][current_capacity] = dp[i - 1][current_capacity]

    chosen = []
    total_weight = 0
    current_capacity = capacity

    for i in range(n, 0, -1):
        if dp[i][current_capacity] != dp[i - 1][current_capacity]:
            chosen.append(i - 1)
            total_weight += weights[i - 1]
            current_capacity -= weights[i - 1]

    chosen.reverse()
    return dp[n][capacity], chosen, total_weight


def main():
    print("=== Input User Knapsack 0/1 ===")
    print("Masukkan data komponen PC Anda sendiri.")

    component_count = prompt_int("Jumlah komponen: ", minimum=1)
    capacity = prompt_int("Kapasitas daya maksimum: ", minimum=0)

    components = []
    weights = []
    profits = []

    for index in range(component_count):
        name, weight, profit = prompt_item(index)
        components.append(name)
        weights.append(weight)
        profits.append(profit)

    max_profit, chosen, total_weight = knapsack_dp(weights, profits, capacity)

    print("\n=== Hasil Optimal ===")
    print("Performa maksimum:", max_profit)
    print("Total daya:", total_weight, "W")
    print("Item terpilih:")

    if not chosen:
        print("- Tidak ada item yang dipilih")
    else:
        for index in chosen:
            print("-", components[index], "(", weights[index], "W,", profits[index], ")")


if __name__ == "__main__":
    main()