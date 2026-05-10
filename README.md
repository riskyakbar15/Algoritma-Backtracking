<!-- Professional README for Algoritma-Backtracking -->

# Algoritma Knapsack (0/1) — Pemilihan Komponen PC

Dokumentasi ini menjelaskan empat implementasi untuk menyelesaikan masalah 0/1 Knapsack (pemilihan komponen PC berdasarkan daya dan performa): satu pendekatan eksahustif (`BruteForce.py`), satu implementasi efisien berbasis Dynamic Programming (`DynamicProgramming.py`), satu pendekatan Branch and Bound (`BranchAndBound.py`), dan satu pendekatan Meet-in-the-Middle (`MeetInTheMiddle.py`).

**Status:** Demo / bahan pembelajaran.

## Cepat Mulai

Prasyarat:

- Python 3.8 atau lebih baru

Menjalankan contoh:

```bash
python BruteForce.py
python DynamicProgramming.py
python BranchAndBound.py
python MeetInTheMiddle.py
```

## Struktur Proyek

- `BruteForce.py` — pemeriksaan semua kombinasi menggunakan `itertools.combinations` (eksahustif)
- `DynamicProgramming.py` — implementasi 0/1 Knapsack klasik menggunakan tabel DP
- `BranchAndBound.py` — pencarian dengan pruning menggunakan batas atas berbasis fractional knapsack
- `MeetInTheMiddle.py` — enumerasi dua bagian subset lalu digabungkan dengan pencarian biner
- `README.md` — dokumentasi ini

## Implementasi Aktual

Berikut penjelasan fungsi dan keluaran masing-masing skrip sesuai kode di repositori:

- `BruteForce.py`
  - Pendekatan: eksplorasi semua subset kombinasi komponen untuk menemukan kombinasi optimal.
  - Cara kerja: iterasi semua kombinasi ukuran 1..n, hitung total daya dan performa, pilih kombinasi terbaik yang tidak melebihi kapasitas `W`.
  - Output yang dicetak: `Performa maksimum`, `Total daya`, daftar item terpilih, dan `Total kombinasi yang diperiksa` (ditampilkan sebagai `2**n`).
  - Kompleksitas: waktu O(2^n). Ini bukan implementasi backtracking dengan pruning — semua subset diperiksa.

- `DynamicProgramming.py`
  - Pendekatan: 0/1 Knapsack klasik menggunakan tabel DP ukuran (n+1) × (W+1).
  - Fungsi kunci: `knapsack_dp(weights, profits, W)` mengembalikan `(max_profit, chosen_indices, total_weight)`.
  - Cara kerja: bangun tabel DP, kemudian rekonstruksi item terpilih dari tabel untuk mendapatkan indeks item yang dipilih.
  - Output yang dicetak: `Performa maksimum`, `Total daya`, dan daftar item terpilih.
  - Kompleksitas: waktu O(n × W), ruang O(n × W). Cocok ketika bobot dan kapasitas berupa bilangan bulat moderat.

- `BranchAndBound.py`
  - Pendekatan: depth-first search dengan pruning berdasarkan batas atas dari fractional knapsack.
  - Cara kerja: item diurutkan berdasarkan rasio performa per daya, lalu cabang yang tidak mungkin mengalahkan solusi terbaik saat ini dipangkas.
  - Output yang dicetak: `Performa maksimum`, `Total daya`, dan daftar item terpilih.
  - Kompleksitas: tetap eksponensial pada kasus terburuk, tetapi biasanya jauh lebih cepat daripada brute force karena pruning.

- `MeetInTheMiddle.py`
  - Pendekatan: membagi item menjadi dua bagian, enumerasi semua subset tiap bagian, lalu menggabungkan hasil terbaik dengan pencarian biner.
  - Cara kerja: subset dari bagian kanan diringkas menjadi daftar subset dominan, kemudian tiap subset bagian kiri dipasangkan dengan subset kanan terbaik yang masih muat.
  - Output yang dicetak: `Performa maksimum`, `Total daya`, dan daftar item terpilih.
  - Kompleksitas: sekitar O(2^(n/2) log 2^(n/2)), efektif untuk jumlah item menengah.

## Contoh Keluaran

Format keluaran yang akan muncul saat menjalankan skrip (nyata dari implementasi):

`BruteForce.py` (contoh):

```contoh bf
=== Brute Force ===
Performa maksimum: 422
Total daya: 455 W
Item terpilih:
- CPU Intel i7 ( 95 W, 85 )
- CPU Cooler Tower ( 15 W, 20 )
...

Total kombinasi yang diperiksa: 1024
```

`DynamicProgramming.py` (contoh):

```contoh dp
=== Dynamic Programming ===
Performa maksimum: 422
Total daya: 455 W
Item terpilih:
- CPU Intel i7 ( 95 W, 85 )
- GPU RTX 4060 Ti ( 220 W, 150 )
...
```

`BranchAndBound.py` (contoh):

```contoh bnb
=== Branch and Bound ===
Performa maksimum: 422
Total daya: 455 W
Item terpilih:
- CPU Intel i7 ( 95 W, 85 )
- CPU Cooler Tower ( 15 W, 20 )
...
```

`MeetInTheMiddle.py` (contoh):

```contoh mitm
=== Meet in the Middle ===
Performa maksimum: 422
Total daya: 455 W
Item terpilih:
- CPU Intel i7 ( 95 W, 85 )
- CPU Cooler Tower ( 15 W, 20 )
...
```

## Catatan & Rekomendasi

- Jika tujuan Anda adalah mempelajari backtracking dengan pruning (branch-and-bound), `BruteForce.py` dapat diadaptasi menjadi versi backtracking yang memangkas cabang saat akumulasi daya melebihi batas.
- Untuk eksperimen dengan kapasitas besar, gunakan `DynamicProgramming.py` jika bobot dapat diperlakukan sebagai integer; jika kapasitas terlalu besar untuk DP, pertimbangkan pendekatan greedy (heuristik) atau algoritma approximate/branch-and-bound.

## Perbandingan Kompleksitas

| Algoritma           | Waktu                      | Ruang              | Catatan                                              |
| ------------------- | -------------------------- | ------------------ | ---------------------------------------------------- |
| Brute Force         | O(2^n)                     | O(1)               | Memeriksa semua subset secara penuh                  |
| Dynamic Programming | O(n × W)                   | O(n × W)           | Cocok untuk kapasitas integer moderat                |
| Branch and Bound    | O(2^n) pada kasus terburuk | O(n) sampai O(2^n) | Biasanya lebih cepat dari brute force karena pruning |
| Meet-in-the-Middle  | O(2^(n/2) log 2^(n/2))     | O(2^(n/2))         | Efektif untuk jumlah item menengah                   |

Ringkasnya: brute force paling mudah dipahami, DP paling stabil untuk kapasitas integer, branch and bound lebih efisien saat pruning efektif, dan meet-in-the-middle berguna saat jumlah item menengah tetapi brute force terlalu mahal.

## Kontribusi

Kontribusi diterima melalui Pull Request. Langkah singkat:

1. Fork repositori
2. Buat branch deskriptif (`feat/`, `fix/`)
3. Tambahkan perubahan dan tes minimal
4. Buka Pull Request

Ikuti gaya Python (PEP 8) dan tambahkan dokumentasi untuk perubahan besar.

## Kontak

GitHub — [riskyakbar15/Deteksi-Kata-Terlarang](https://github.com/riskyakbar15/Deteksi-Kata-Terlarang)

---
