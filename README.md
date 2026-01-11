# Algoritma Knapsack - Pemilihan Komponen PC

Program ini menyelesaikan masalah **0/1 Knapsack Problem** untuk memilih komponen PC dengan performa maksimum dalam batasan daya **500 Watt**.

## Deskripsi Masalah

Diberikan sejumlah komponen PC dengan nilai daya (Watt) dan performa masing-masing. Tujuannya adalah memilih kombinasi komponen yang menghasilkan **performa tertinggi** tanpa melebihi kapasitas daya yang tersedia.

## Algoritma

### 1. Brute Force (`BruteForce.py`)

- Mengecek **semua kemungkinan kombinasi** komponen (2^n kombinasi)
- Memilih kombinasi dengan performa tertinggi yang tidak melebihi batas daya
- **Kompleksitas Waktu:** O(2^n)
- Cocok untuk jumlah item sedikit

### 2. Dynamic Programming (`DynamicProgramming.py`)

- Menggunakan **tabel DP** untuk menyimpan solusi subproblem
- Menghindari perhitungan berulang dengan memoization
- **Kompleksitas Waktu:** O(n × W)
- Lebih efisien untuk dataset besar

## Data Komponen

| No  | Komponen               | Daya (W) | Performa |
| --- | ---------------------- | -------- | -------- |
| 1   | CPU Intel i7           | 95       | 85       |
| 2   | CPU Cooler Tower       | 15       | 20       |
| 3   | GPU RTX 3060           | 170      | 120      |
| 4   | GPU RTX 4060 Ti        | 220      | 150      |
| 5   | RAM 16GB DDR4          | 10       | 30       |
| 6   | SSD NVMe 1TB           | 8        | 25       |
| 7   | HDD 2TB                | 12       | 18       |
| 8   | Motherboard ATX Gaming | 70       | 60       |
| 9   | PSU Modular            | 5        | 12       |
| 10  | RGB Fan Kit            | 20       | 22       |

**Kapasitas Daya Maksimum:** 500 Watt

## Cara Menjalankan

Pastikan Python sudah terinstall, lalu jalankan:

```bash
# Brute Force
python BruteForce.py

# Dynamic Programming
python DynamicProgramming.py
```

## Contoh Output

```
=== Brute Force ===
Performa maksimum: 372
Total daya: 395 W
Item terpilih:
- CPU Intel i7 ( 95 W, 85 )
- CPU Cooler Tower ( 15 W, 20 )
- GPU RTX 3060 ( 170 W, 120 )
- RAM 16GB DDR4 ( 10 W, 30 )
- SSD NVMe 1TB ( 8 W, 25 )
- HDD 2TB ( 12 W, 18 )
- Motherboard ATX Gaming ( 70 W, 60 )
- PSU Modular ( 5 W, 12 )

Total kombinasi yang diperiksa: 1024
```

## Perbandingan Algoritma

| Aspek               | Brute Force               | Dynamic Programming      |
| ------------------- | ------------------------- | ------------------------ |
| Kompleksitas Waktu  | O(2^n)                    | O(n × W)                 |
| Kompleksitas Ruang  | O(1)                      | O(n × W)                 |
| Kombinasi Diperiksa | 1024                      | -                        |
| Kelebihan           | Sederhana, mudah dipahami | Efisien untuk data besar |
| Kekurangan          | Lambat untuk n besar      | Membutuhkan memori lebih |

## Teknologi

- Python 3.x
- Library: `itertools` (untuk Brute Force)
