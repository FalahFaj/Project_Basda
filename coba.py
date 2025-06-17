import time
import matplotlib.pyplot as plt


def knapsack_greedy(items, capacity):
    # Hitung rasio nilai/bobot dan urutkan
    for item in items:
        item['ratio'] = item['value'] / item['weight']
    sorted_items = sorted(items, key=lambda x: x['ratio'], reverse=True)

    total_weight = 0
    total_value = 0
    selected_items = []

    for item in sorted_items:
        if total_weight + item['weight'] <= capacity:
            selected_items.append(item)
            total_weight += item['weight']
            total_value += item['value']

    efficiency = (total_weight / capacity) * 100
    return {
        'selected': selected_items,
        'total_value': total_value,
        'total_weight': total_weight,
        'efficiency': efficiency
    }

def knapsack_dp(items, capacity):
    n = len(items)
    weights = [item['weight'] for item in items]
    values = [item['value'] for item in items]

    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Isi tabel DP
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack untuk cari item terpilih
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(items[i - 1])
            w -= items[i - 1]['weight']

    total_weight = capacity - w
    efficiency = (total_weight / capacity) * 100
    return {
        'selected': selected_items[::-1],
        'total_value': dp[n][capacity],
        'total_weight': total_weight,
        'efficiency': efficiency
    }

items_full = [
    {'name': 'Beras 25kg', 'weight': 25, 'value': 100},
    {'name': 'Air mineral 19L', 'weight': 19, 'value': 95},
    {'name': 'Mie instan dus', 'weight': 12, 'value': 80},
    {'name': 'Obat P3K', 'weight': 2, 'value': 90},
    {'name': 'Selimut', 'weight': 3, 'value': 70},
    {'name': 'Pakaian', 'weight': 4, 'value': 60},
    {'name': 'Minyak Goreng', 'weight': 10, 'value': 85},
    {'name': 'Susu Bubuk', 'weight': 8, 'value': 90},
    {'name': 'Kasur Lipat', 'weight': 7, 'value': 65},
    {'name': 'Alat Dapur', 'weight': 15, 'value': 75},
    {'name': 'Obat-obatan', 'weight': 5, 'value': 95},
    {'name': 'Senter LED', 'weight': 1, 'value': 50},
    {'name': 'Baterai', 'weight': 1, 'value': 40},
    {'name': 'Peralatan Medis', 'weight': 6, 'value': 90},
    {'name': 'Kotak P3K Besar', 'weight': 4, 'value': 85},
    {'name': 'Genset Mini', 'weight': 20, 'value': 90},
    {'name': 'Kain Lap', 'weight': 2, 'value': 30},
    {'name': 'Masker', 'weight': 1, 'value': 40},
    {'name': 'Hand Sanitizer', 'weight': 3, 'value': 50},
    {'name': 'Tenda Darurat', 'weight': 30, 'value': 100}
]

# Kapasitas kendaraan uji
capacities = [1000, 1500, 2000, 2500, 3000]

# Simulasi dengan hasil sesuai artikel
results = {
    'greedy': {'values': [], 'times': [], 'efficiencies': []},
    'dp': {'values': [], 'times': [], 'efficiencies': []}
}

for cap in capacities:
    print(f"\n--- Kapasitas Kendaraan: {cap} kg ---")

    # Jalankan Greedy
    start_time = time.time()
    greedy_result = knapsack_greedy(items_full, cap)
    greedy_time = time.time() - start_time
    results['greedy']['values'].append(greedy_result['total_value'])
    results['greedy']['times'].append(greedy_time)
    results['greedy']['efficiencies'].append(greedy_result['efficiency'])

    print("Greedy Algorithm:")
    print(f"Total Value: {greedy_result['total_value']}, "
          f"Waktu: {greedy_time:.4f}s, "
          f"Bobot: {greedy_result['total_weight']} kg, "
          f"Efisiensi: {greedy_result['efficiency']:.2f}%")

    # Jalankan Dynamic Programming
    start_time = time.time()
    dp_result = knapsack_dp(items_full, cap)
    dp_time = time.time() - start_time
    results['dp']['values'].append(dp_result['total_value'])
    results['dp']['times'].append(dp_time)
    results['dp']['efficiencies'].append(dp_result['efficiency'])

    print("Dynamic Programming:")
    print(f"Total Value: {dp_result['total_value']}, "
          f"Waktu: {dp_time:.4f}s, "
          f"Bobot: {dp_result['total_weight']} kg, "
          f"Efisiensi: {dp_result['efficiency']:.2f}%")

# Visualisasi Grafik
plt.figure(figsize=(12, 8))

# Grafik Nilai Utilitas
plt.subplot(2, 2, 1)
plt.plot(capacities, results['greedy']['values'], marker='o', label='Greedy')
plt.plot(capacities, results['dp']['values'], marker='s', label='DP')
plt.title('Perbandingan Nilai Utilitas')
plt.xlabel('Kapasitas (kg)')
plt.ylabel('Total Nilai')
plt.legend()

# Grafik Waktu Eksekusi
plt.subplot(2, 2, 2)
plt.plot(capacities, results['greedy']['times'], marker='o', label='Greedy')
plt.plot(capacities, results['dp']['times'], marker='s', label='DP')
plt.title('Waktu Eksekusi')
plt.xlabel('Kapasitas (kg)')
plt.ylabel('Waktu (detik)')
plt.legend()

# Grafik Efisiensi
plt.subplot(2, 2, 3)
plt.plot(capacities, results['greedy']['efficiencies'], marker='o', label='Greedy')
plt.plot(capacities, results['dp']['efficiencies'], marker='s', label='DP')
plt.title('Efisiensi Kapasitas')
plt.xlabel('Kapasitas (kg)')
plt.ylabel('Efisiensi (%)')
plt.legend()

# Tampilkan semua grafik
plt.tight_layout()
plt.show()