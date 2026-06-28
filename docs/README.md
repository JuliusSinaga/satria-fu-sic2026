# Dokumentasi Analisis Finansial dan Proyeksi TCO

Dokumen ini memuat interpretasi data visual dari file `tco_bep_chart.png` serta ringkasan eksekutif hasil kalkulasi Total Cost of Ownership (TCO). Analisis ini digunakan sebagai landasan data (proof of concept) untuk fitur Micro-Savings dan Automated Investment pada pengembangan platform Sahabat Duwit (SAWIT).

## Interpretasi Grafik: tco_bep_chart.png

Proyeksi grafik menggunakan rentang waktu 60 bulan (5 tahun) dengan parameter operasional jarak tempuh rata-rata kendaraan sebesar 12.000 km per tahun (1.000 km per bulan).

### 1. Fase Pembelian / Capital Expenditure (Bulan ke-0)
* **Kondisi Finansial:** Honda BeAT CBS memiliki harga OTR bersih Rp 19.155.000. Polytron Fox-R memiliki harga OTR bersih Rp 15.500.000 setelah dipotong Subsidi Pemerintah sebesar Rp 7.000.000.
* **Korelasi Topik:** Data menunjukkan adanya keunggulan modal awal (Capex) sebesar Rp 3.655.000 pada varian EV. Angka ini menjadi basis visualisasi bagi pengguna platform bahwa intervensi kebijakan regulasi dapat meruntuhkan hambatan investasi awal bagi Gen Z.

### 2. Fase Operasional / Operational Expenditure (Bulan ke-7)
* **Kondisi Finansial:** Skenario operasional Polytron Fox-R mencakup biaya tetap skema sewa baterai (BaaS) sebesar Rp 200.000 per bulan.
* **Korelasi Topik:** Bulan ke-7 merupakan Titik Balik Efisiensi Operasional Mutlak. Pada titik ini, akumulasi biaya variabel bensin (Pertalite) dan pemeliharaan berkala pada motor konvensional secara resmi melampaui biaya tetap sewa baterai dan daya listrik EV. Setelah Bulan ke-7, margin penghematan EV terus melebar secara konsisten.

---

## Ringkasan Komparasi Finansial dan Nilai Investasi (5 Tahun)

| Komponen Finansial | Motor Bensin (Honda BeAT CBS) | Motor Listrik (Polytron Fox R) | Margin Penghematan Bersih |
| :--- | :---: | :---: | :---: |
| Biaya Pembelian Awal (Capex) | Rp 19.155.000 | Rp 15.500.000 | Rp 3.655.000 (EV Lebih Efisien) |
| Total TCO Akhir (60 Bulan) | Rp 32.185.000 | Rp 23.332.201 | Rp 8.852.799 (Total Akumulasi Hemat) |
| Penghematan Opex Bulanan Net | - | - | Rp 332.490 / bulan |

### Implementasi pada Fitur Aplikasi Keuangan
Memanfaatkan angka penghematan operasional net sebesar Rp 332.490 per bulan ini untuk dialihkan secara otomatis ke instrumen reksa dana. Menggunakan asumsi makroekonomi dengan Compound Annual Growth Rate (CAGR) sebesar 12,51% per tahun, konversi dana tersebut menghasilkan proyeksi sebagai berikut:

* **Total Setoran Modal Pokok (Micro-Savings):** Rp 19.949.400
* **Nilai Akhir Akumulasi Investasi (Future Value):** Rp 27.249.707
* **Pertumbuhan Nilai Murni dari Bunga Majemuk:** Rp 7.300.307

### Kesimpulan Hubungan Topik
Analisis ini membuktikan secara empiris bahwa penghematan skala mikro (micro-savings) dari efisiensi harian yang dikelola secara digital oleh platform mampu mengubah pola konsumsi pasif menjadi pertumbuhan aset produktif yang signifikan bagi Gen Z.
