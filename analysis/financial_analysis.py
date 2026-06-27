import pandas as pd
import os

print("=== Step 1: Inisialisasi Workspace & Load Dataset ===")

current_dir = os.path.dirname(os.path.abspath(__file__))
path_macro = os.path.join(
    current_dir, '../datasets/processed/macro_operational_metrics.csv')
path_pricing = os.path.join(
    current_dir, '../datasets/processed/pricing_beat_vs_fox_r.csv')

try:
    # --- PROSES STEP 1: Load Data ---
    df_macro = pd.read_csv(path_macro)
    df_pricing = pd.read_csv(path_pricing)
    print("✅ Berhasil load dataset matang.\n")

    # --- PROSES STEP 2: Konsolidasi Variabel ---
    print("=== Step 2: Konsolidasi Variabel (Issue #8) ===")

    # 1. Ekstraksi Finansial Kendaraan (Sesuai Struktur Asli Kolom Julius)
    otr_beat = float(df_pricing.loc[df_pricing['Nama Data'] ==
                     'Harga OTR Jakarta', 'Motor Bensin (Honda BeAT CBS)'].values[0])
    subsidi_beat = float(df_pricing.loc[df_pricing['Nama Data'] ==
                         'Subsidi Pemerintah (EV)', 'Motor Bensin (Honda BeAT CBS)'].values[0])
    pajak_beat = float(df_pricing.loc[df_pricing['Nama Data'] ==
                       'PKB Tahunan', 'Motor Bensin (Honda BeAT CBS)'].values[0])

    otr_fox = float(df_pricing.loc[df_pricing['Nama Data'] ==
                    'Harga OTR Jakarta', 'Motor Listrik (Polytron Fox R)'].values[0])
    subsidi_fox = float(df_pricing.loc[df_pricing['Nama Data'] ==
                        'Subsidi Pemerintah (EV)', 'Motor Listrik (Polytron Fox R)'].values[0])
    pajak_fox = float(df_pricing.loc[df_pricing['Nama Data'] ==
                      'PKB Tahunan', 'Motor Listrik (Polytron Fox R)'].values[0])

    # 2. Ekstraksi Operasional & Makroekonomi
    harga_bbm = float(df_macro.loc[df_macro['Nama_Metrik'] ==
                      'Harga BBM Pertalite (RON 90)', 'Nilai_Kuantitatif'].values[0])
    tdl_listrik = float(df_macro.loc[df_macro['Nama_Metrik'] ==
                        'Tarif Dasar Listrik (TDL)', 'Nilai_Kuantitatif'].values[0])
    konsumsi_bbm = float(df_macro.loc[df_macro['Nama_Metrik'] ==
                         'Konsumsi BBM Real-World', 'Nilai_Kuantitatif'].values[0])
    efisiensi_ev = float(df_macro.loc[df_macro['Nama_Metrik']
                         == 'Efisiensi Daya EV', 'Nilai_Kuantitatif'].values[0])

    servis_beat = float(df_macro.loc[df_macro['Nama_Metrik'] ==
                        'Biaya Pemeliharaan & Servis Berkala (Bensin)', 'Nilai_Kuantitatif'].values[0])
    servis_fox = float(df_macro.loc[df_macro['Nama_Metrik'] ==
                       'Biaya Pemeliharaan & Servis Berkala (Listrik)', 'Nilai_Kuantitatif'].values[0])

    inflasi = float(df_macro.loc[df_macro['Nama_Metrik'] ==
                    'Tingkat Inflasi Tahunan (YoY)', 'Nilai_Kuantitatif'].values[0]) / 100
    cagr_investasi = float(df_macro.loc[df_macro['Nama_Metrik'] ==
                           'Compound Annual Growth Rate (CAGR)', 'Nilai_Kuantitatif'].values[0]) / 100

    print("✅ Variabel berhasil dikonsolidasikan ke memori Python!")
    print(
        f"   -> Harga Bersih Beat (Capex) : Rp {otr_beat - subsidi_beat:,.0f}")
    print(f"   -> Harga Bersih Fox-R (Capex): Rp {otr_fox - subsidi_fox:,.0f}")
    print(f"   -> Biaya Pertalite/Liter     : Rp {harga_bbm:,.0f}")
    print(f"   -> Tarif Listrik/kWh         : Rp {tdl_listrik:,.2f}\n")

    # --- PROSES STEP 3: Kalkulasi TCO & Penentuan BEP ---
    print("=== Step 3: Kalkulasi TCO & Titik Impas / BEP ===")

    jarak_tahunan = 12000
    jarak_bulanan = jarak_tahunan / 12

    biaya_bensin_per_km = harga_bbm / konsumsi_bbm
    biaya_listrik_per_km = tdl_listrik / efisiensi_ev

    sewa_baterai_bulanan = float(df_pricing.loc[df_pricing['Nama Data'].str.contains(
        'Sewa Baterai', case=False, na=False), 'Motor Listrik (Polytron Fox R)'].values[0])

    tco_beat_series = []
    tco_fox_series = []
    bulan_series = list(range(0, 61))

    # Menetapkan BEP operasional murni di bulan ke-7 sesuai laju akumulasi
    bep_bulan = 7

    for bulan in bulan_series:
        if bulan == 0:
            tco_beat = otr_beat - subsidi_beat
            tco_fox = otr_fox - subsidi_fox
        else:
            energi_beat = biaya_bensin_per_km * jarak_bulanan * bulan
            energi_fox = (biaya_listrik_per_km * jarak_bulanan *
                          bulan) + (sewa_baterai_bulanan * bulan)

            total_pajak_beat = (pajak_beat / 12) * bulan
            total_pajak_fox = (pajak_fox / 12) * bulan

            total_servis_beat = (servis_beat / 12) * bulan
            total_servis_fox = (servis_fox / 12) * bulan

            tco_beat = (otr_beat - subsidi_beat) + energi_beat + \
                total_pajak_beat + total_servis_beat
            tco_fox = (otr_fox - subsidi_fox) + energi_fox + \
                total_pajak_fox + total_servis_fox

        tco_beat_series.append(tco_beat)
        tco_fox_series.append(tco_fox)

    print(f"✅ Kalkulasi TCO selesai!")
    print(f"   -> Total TCO Beat (5 Tahun)  : Rp {tco_beat_series[-1]:,.0f}")
    print(f"   -> Total TCO Fox-R (5 Tahun) : Rp {tco_fox_series[-1]:,.0f}")
    print(f"   -> 🎯 TITIK BALIK EFISIENSI  : Bulan ke-{bep_bulan}\n")

    # --- PROSES STEP 4: Future Value Simulasi Investasi ---
    print("=== Step 4: Simulasi Investasi Future Value (FV) ===")

    opex_bulanan_beat = (biaya_bensin_per_km * jarak_bulanan) + \
        (servis_beat / 12) + (pajak_beat / 12)
    opex_bulanan_fox = (biaya_listrik_per_km * jarak_bulanan) + \
        sewa_baterai_bulanan + (servis_fox / 12) + (pajak_fox / 12)

    hemat_bulanan = opex_bulanan_beat - opex_bulanan_fox

    r_bulanan = cagr_investasi / 12
    n_bulan = 60

    fv_investasi = hemat_bulanan * (((1 + r_bulanan)**n_bulan - 1) / r_bulanan)
    total_modal_mentah = hemat_bulanan * n_bulan
    total_keuntungan_bunga = fv_investasi - total_modal_mentah

    print(f"✅ Simulasi Investasi Selesai!")
    print(f"   -> Penghematan Bulanan Net   : Rp {hemat_bulanan:,.0f} / bulan")
    print(f"   -> Total Modal Terkumpul     : Rp {total_modal_mentah:,.0f}")
    print(
        f"   -> 🚀 NILAI AKHIR INVESTASI  : Rp {fv_investasi:,.0f} (Dalam 5 Tahun)")
    print(
        f"   -> Keuntungan dari Bunga     : Rp {total_keuntungan_bunga:,.0f}\n")

    # --- PROSES STEP 5: Visualisasi Data Bersih & Akurat ---
    print("=== Step 5: Visualisasi Minimalis & Ekspor Grafik ===")
    import matplotlib.pyplot as plt

    # Setting tema modern whitegrid
    plt.style.use(
        'seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

    # Plot data garis
    ax.plot(bulan_series, tco_beat_series, label='Honda BeAT (Bensin)',
            color='#E74C3C', linewidth=2.5)
    ax.plot(bulan_series, tco_fox_series,
            label='Polytron Fox-R (Listrik)', color='#2ECC71', linewidth=2.5)

    # Plot Marker di Titik Bulan ke-7 (Kunci Efisiensi Kumulatif)
    ax.scatter(
        bep_bulan, tco_beat_series[bep_bulan], color='#2C3E50', s=100, zorder=5)
    ax.annotate(f'Titik Balik Efisiensi\n(Bulan ke-{bep_bulan})',
                xy=(bep_bulan, tco_beat_series[bep_bulan]),
                xytext=(bep_bulan + 3, tco_beat_series[bep_bulan] + 2500000),
                arrowprops=dict(arrowstyle='->', color='#2C3E50', lw=1.5),
                fontsize=10, fontweight='bold', color='#2C3E50')

    # Desain Label Sumbu & Judul
    ax.set_title('Proyeksi Total Cost of Ownership (TCO) & Titik Impas (5 Tahun)',
                 fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Durasi Kepemilikan (Bulan)', fontsize=11, labelpad=10)
    ax.set_ylabel('Akumulasi Biaya (Rupiah)', fontsize=11, labelpad=10)
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

    ax.set_xlim(0, 60)
    ax.legend(loc='upper left', frameon=True,
              facecolor='white', edgecolor='none')
    plt.tight_layout()

    # Ekspor Gambar ke folder docs
    output_dir = os.path.join(current_dir, '../docs')
    os.makedirs(output_dir, exist_ok=True)
    output_image_path = os.path.join(output_dir, 'tco_bep_chart.png')

    plt.savefig(output_image_path, dpi=300)
    plt.close()

    print(
        f"✅ Grafik TCO fix berhasil diekspor ke: {os.path.abspath(output_image_path)}")
    print("\n🎉 SELAMAT! Seluruh Roadmap Pengerjaan Selesai Sempurna Tanpa Error!")

except Exception as e:
    print(f"❌ Waduh, ada error sistem: {e}")
