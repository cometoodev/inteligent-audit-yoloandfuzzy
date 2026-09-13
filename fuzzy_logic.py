# fuzzy_logic.py
# Implementasi Fuzzy Mamdani menggunakan scikit-fuzzy
# Revisi: Penambahan variabel pohonpeneduh, 12 Rule Utama sesuai spesifikasi baru

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ─── 1. UNIVERSE (semesta pembicaraan) ───────────────────────────────────────
# Resolusi 0.1 agar centroid akurat
orang_universe          = np.arange(0, 10.1,  0.1)   # 0 – 10
bangkutaman_universe    = np.arange(0, 7.1,   0.1)   # 0 – 7
tempatsampah_universe   = np.arange(0, 5.1,   0.1)   # 0 – 5
pohonpeneduh_universe   = np.arange(0, 3.1,   0.1)   # 0 – 3
lampulalulintas_universe= np.arange(0, 5.1,   0.1)   # 0 – 5
urgensi_universe        = np.arange(0, 100.1, 0.1)   # 0 – 100, resolusi tinggi

# ─── 2. ANTECEDENT (variabel input) ──────────────────────────────────────────
orang           = ctrl.Antecedent(orang_universe,           'orang')
bangkutaman     = ctrl.Antecedent(bangkutaman_universe,     'bangkutaman')
tempatsampah    = ctrl.Antecedent(tempatsampah_universe,    'tempatsampah')
pohonpeneduh    = ctrl.Antecedent(pohonpeneduh_universe,    'pohonpeneduh')
lampulalulintas = ctrl.Antecedent(lampulalulintas_universe, 'lampulalulintas')

# ─── 3. CONSEQUENT (variabel output) ─────────────────────────────────────────
urgensi = ctrl.Consequent(urgensi_universe, 'urgensi', defuzzify_method='centroid')

# ─── 4. MEMBERSHIP FUNCTIONS INPUT ───────────────────────────────────────────
# --- Orang ---
# Sepi  : puncak di 0, transisi habis di 3.5
# Ramai : mulai dari 2.5, puncak di 6
orang['Sepi']  = fuzz.trimf(orang.universe, [0,   0,   3.5])
orang['Ramai'] = fuzz.trimf(orang.universe, [2.5, 6,   10])

# --- Bangku Taman ---
# Minim   : puncak 0, habis di 3
# Memadai : naik dari 3, puncak di 5, habis di 7
bangkutaman['Minim']   = fuzz.trimf(bangkutaman.universe, [0,   0, 3])
bangkutaman['Memadai'] = fuzz.trimf(bangkutaman.universe, [3,   5, 7])

# --- Tempat Sampah ---
# Minim   : ketat; ada 1 saja sudah keluar zona minim
# Memadai : irisan di 0.5, ideal di 2
tempatsampah['Minim']   = fuzz.trimf(tempatsampah.universe, [0,   0,   1])
tempatsampah['Memadai'] = fuzz.trimf(tempatsampah.universe, [0.5, 2,   5])

# --- Pohon Peneduh ---
# Minim   : puncak 0, habis di 1
# Memadai : irisan di 0.5, puncak di 1.5, habis di 3
pohonpeneduh['Minim']   = fuzz.trimf(pohonpeneduh.universe, [0,   0,   1])
pohonpeneduh['Memadai'] = fuzz.trimf(pohonpeneduh.universe, [0.5, 1.5, 3])

# --- Lampu Lalu Lintas ---
# NA  : tidak ada lampu (nilai 0)
# Ada : terdeteksi 1 saja sudah dianggap ada dan berfungsi
lampulalulintas['NA']  = fuzz.trimf(lampulalulintas.universe, [0,   0,   1])
lampulalulintas['Ada'] = fuzz.trimf(lampulalulintas.universe, [0.5, 1.5, 5])

# ─── 5. OUTPUT URGENSI ────────────────────────────────────────────────────────
# Intervensi   : skor 60–75  → kondisi kritis, perbaikan segera
# Monitoring   : skor 65–85  → perlu pengawasan rutin
# Perencanaan  : skor 80–95  → rencana pengembangan kapasitas
# Pemeliharaan : skor 90–100 → kondisi ideal, perawatan rutin
urgensi['Intervensi']   = fuzz.trimf(urgensi.universe, [60,  60,  75])
urgensi['Monitoring']   = fuzz.trimf(urgensi.universe, [65,  75,  85])
urgensi['Perencanaan']  = fuzz.trimf(urgensi.universe, [80,  85,  95])
urgensi['Pemeliharaan'] = fuzz.trimf(urgensi.universe, [90, 100, 100])

# ─── 6. RULE BASE (12 Aturan Utama - Update Final) ───────────────────────────
# Logika ini menggunakan bobot (1) untuk setiap aturan.
# Prioritas: Ketersediaan fasilitas peneduh dan tempat duduk.

rules = [
    # R1 - R6: Logika Pemeliharaan (🟢)
    ctrl.Rule(pohonpeneduh['Memadai'], urgensi['Pemeliharaan']),  # type: ignore[operator]
    ctrl.Rule(bangkutaman['Memadai'], urgensi['Pemeliharaan']),  # type: ignore[operator]
    ctrl.Rule(tempatsampah['Memadai'], urgensi['Pemeliharaan']),  # type: ignore[operator]
    ctrl.Rule(orang['Sepi'], urgensi['Pemeliharaan']),  # type: ignore[operator]
    ctrl.Rule(bangkutaman['Memadai'] & pohonpeneduh['Memadai'], urgensi['Pemeliharaan']),  # type: ignore[operator]
    ctrl.Rule(lampulalulintas['Ada'], urgensi['Pemeliharaan']),  # type: ignore[operator]

    # R7 - R8: Logika Perencanaan (⚪)
    ctrl.Rule(pohonpeneduh['Minim'], urgensi['Perencanaan']),  # type: ignore[operator]
    ctrl.Rule(bangkutaman['Minim'], urgensi['Perencanaan']),  # type: ignore[operator]

    # R9: Logika Monitoring (🟡)
    ctrl.Rule(bangkutaman['Minim'] & pohonpeneduh['Minim'], urgensi['Monitoring']),  # type: ignore[operator]

    # R10 - R11: Logika Pemeliharaan Kondisi Ramai
    ctrl.Rule(orang['Ramai'] & pohonpeneduh['Memadai'], urgensi['Pemeliharaan']),  # type: ignore[operator]
    ctrl.Rule(orang['Ramai'] & bangkutaman['Memadai'], urgensi['Pemeliharaan']),  # type: ignore[operator]

    # R12: Logika Intervensi (🟠)
    ctrl.Rule(orang['Ramai'] & bangkutaman['Minim'] & pohonpeneduh['Minim'], urgensi['Intervensi']),  # type: ignore[operator]
]

# ─── 7. CONTROL SYSTEM ───────────────────────────────────────────────────────
sistem_fuzzy = ctrl.ControlSystem(rules)

# ─── 8. FUNGSI UTAMA ─────────────────────────────────────────────────────────
def calculate_skor_fuzzy(counts_depan, counts_kanan, counts_kiri, image_count=3):
    """
    Menghitung skor dan status fuzzy Mamdani berdasarkan deteksi YOLO dari
    3 arah (Depan, Kanan, Kiri).

    Args:
        counts_depan  (dict): {'orang': int, 'bangkutaman': int, 'tempatsampah': int,
                               'pohonpeneduh': int, 'lampulalulintas': int}
        counts_kanan  (dict): sama
        counts_kiri   (dict): sama

    Returns:
        skor_akhir (float): nilai 60–100
        status     (str)  : 'Intervensi' / 'Monitoring' / 'Perencanaan' / 'Pemeliharaan'
    """
    active_directions = image_count
    if active_directions == 0:
        return 0.0, 'Intervensi'

    # Gabungkan hitungan dari 3 arah
    total_orang           = counts_depan.get('orang', 0)           + counts_kanan.get('orang', 0)           + counts_kiri.get('orang', 0)
    total_bangkutaman     = counts_depan.get('bangkutaman', 0)     + counts_kanan.get('bangkutaman', 0)     + counts_kiri.get('bangkutaman', 0)
    total_tempatsampah    = counts_depan.get('tempatsampah', 0)    + counts_kanan.get('tempatsampah', 0)    + counts_kiri.get('tempatsampah', 0)
    total_pohonpeneduh    = counts_depan.get('pohonpeneduh', 0)    + counts_kanan.get('pohonpeneduh', 0)    + counts_kiri.get('pohonpeneduh', 0)
    total_lampulalulintas = counts_depan.get('lampulalulintas', 0) + counts_kanan.get('lampulalulintas', 0) + counts_kiri.get('lampulalulintas', 0)

    # 1. Logika Pembagi Dinamis (Dynamic Counter)
    # Kalkulasi: Gunakan rumus Rata-rata = Total Objek / active_directions
    avg_orang           = total_orang / active_directions
    avg_bangkutaman     = total_bangkutaman / active_directions
    avg_tempatsampah    = total_tempatsampah / active_directions
    avg_pohonpeneduh    = total_pohonpeneduh / active_directions
    avg_lampulalulintas = total_lampulalulintas / active_directions

    # Clamp ke batas universe agar tidak out-of-range
    total_orang           = min(round(avg_orang),           10)
    total_bangkutaman     = min(round(avg_bangkutaman),     7)
    total_tempatsampah    = min(round(avg_tempatsampah),    5)
    total_pohonpeneduh    = min(round(avg_pohonpeneduh),    3)
    total_lampulalulintas = min(round(avg_lampulalulintas), 5)

    try:
        sim = ctrl.ControlSystemSimulation(sistem_fuzzy)
        sim.input['orang']           = total_orang
        sim.input['bangkutaman']     = total_bangkutaman
        sim.input['tempatsampah']    = total_tempatsampah
        sim.input['pohonpeneduh']    = total_pohonpeneduh
        sim.input['lampulalulintas'] = total_lampulalulintas
        sim.compute()
        skor_akhir = round(sim.output['urgensi'], 2)
    except Exception as e:
        # Fallback jika fuzzy gagal (misal input di batas universe ekstrem)
        print(f"[FUZZY WARNING] {e} — Menggunakan fallback scoring.")
        skor_akhir = _fallback_score(total_orang, total_bangkutaman,
                                     total_tempatsampah, total_pohonpeneduh,
                                     total_lampulalulintas)

    status = _tentukan_status(skor_akhir)
    return skor_akhir, status


def _tentukan_status(skor: float) -> str:
    """
    Terjemahkan skor numerik ke label status.
    Sesuai batas MF Output revisi final:
      Pemeliharaan : [90, 100, 100]  → skor ≥ 90
      Perencanaan  : [80,  85,  95]  → skor ≥ 80
      Monitoring   : [65,  75,  85]  → skor ≥ 65
      Intervensi   : [60,  60,  75]  → skor  < 65
    """
    if skor >= 90:
        return 'Pemeliharaan'
    elif skor >= 80:
        return 'Perencanaan'
    elif skor >= 65:
        return 'Monitoring'
    else:
        return 'Intervensi'


def _fallback_score(orang, bangku, sampah, pohon, lampu) -> float:  # type: ignore[misc]
    """Skor sederhana jika engine fuzzy gagal. Rentang: 60–100."""
    skor = 60.0
    if sampah >= 1:
        skor += 8.0
    if bangku >= 3:
        skor += 10.0
    elif bangku >= 1:
        skor += 5.0
    if pohon >= 1:       # threshold pohon sesuai MF baru (memadai mulai di 0.5)
        skor += 10.0
    if lampu >= 1:
        skor += 8.0
    if orang <= 3:       # threshold sepi sesuai MF baru (sepi habis di 3.5)
        skor += 4.0
    return min(skor, 100.0)
