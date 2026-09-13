import os
import cv2
import numpy as np
from datetime import datetime
from werkzeug.utils import secure_filename
from ultralytics import YOLO

# Load model YOLOv11 Custom Model
model_yolo = YOLO('best.pt')

# Ekstensi gambar yang diizinkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'tiff', 'tif', 'jfif', 'pjpeg', 'pjp'}

def allowed_file(filename):
    """Cek ekstensi file gambar. Fix: rsplit mengembalikan list, harus ambil [1]."""
    if '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()   # BUG FIX: tambah [1]
    return ext in ALLOWED_EXTENSIONS

def read_image_robust(path):
    """
    Baca gambar secara robust menggunakan numpy buffer.
    Mengatasi path dengan karakter non-ASCII dan semua ukuran gambar.
    Mengembalikan numpy array BGR atau None jika gagal.
    """
    try:
        # Metode 1: cv2.imread standar
        img = cv2.imread(path)
        if img is not None:
            return img
        
        # Metode 2: Baca via numpy buffer (untuk path non-ASCII / file terlindungi)
        with open(path, 'rb') as f:
            buf = np.frombuffer(f.read(), dtype=np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        return img  # bisa None jika format tidak didukung
    except Exception as e:
        print(f"[read_image_robust] Gagal baca gambar '{path}': {e}")
        return None

def process_image(file_input, arah, upload_folder, is_path=False):
    """
    Memproses gambar dengan model YOLOv11 best.pt.
    - Mendukung semua ekstensi gambar umum
    - Mendukung semua ukuran (kecil / besar / portrait / landscape)
    - Menggunakan try/except agar jika gagal tidak merusak flow
    """
    time_str = datetime.now().strftime("%H%M%S%f")
    empty_counts = {
        'orang': 0,
        'bangkutaman': 0,
        'tempatsampah': 0,
        'pohonpeneduh': 0,
        'lampulalulintas': 0
    }

    try:
        # ── 1. Penanganan Sumber File ──────────────────────────────────────────
        if is_path:
            # Audit Massal: path lokal dari ZIP
            if not os.path.exists(file_input):
                print(f"[process_image] File tidak ditemukan: {file_input}")
                return None, empty_counts
            original_path = file_input
            filename = os.path.basename(original_path)
        else:
            # Audit Satuan: upload via Flask form
            if not file_input or not hasattr(file_input, 'filename') or file_input.filename == '':
                print(f"[process_image] Tidak ada file yang diunggah untuk arah: {arah}")
                return None, empty_counts

            filename = secure_filename(file_input.filename)

            # Jika nama file kosong setelah secure_filename (karakter spesial semua)
            if not filename:
                filename = f"upload_{arah}_{time_str}.jpg"

            # Jika tidak ada ekstensi dikenal, tetap coba proses (YOLO bisa baca bytes)
            original_path = os.path.join(upload_folder, f"raw_{arah}_{time_str}_{filename}")
            file_input.save(original_path)

        # ── 2. Verifikasi file bisa dibaca sebagai gambar ──────────────────────
        # Baca ulang untuk validasi (bukan wajib, tapi memberi pesan error yang jelas)
        img_check = read_image_robust(original_path)
        if img_check is None:
            print(f"[process_image] File bukan gambar valid atau rusak: {original_path}")
            # Jangan return None — biarkan YOLO coba sendiri (kadang YOLO bisa baca PIL)
            # Jika YOLO juga gagal, akan tertangkap di except di bawah

        # ── 3. Proses Deteksi YOLO ────────────────────────────────────────────
        # YOLO secara otomatis:
        #   - Me-resize gambar ke ukuran input model (misal 640x640)
        #   - Menangani aspect ratio (letterboxing)
        #   - Mendukung semua resolusi gambar (kecil / besar)
        results = model_yolo(
            original_path,
            conf=0.50,     # confidence threshold
            verbose=False  # matikan log ke konsol setiap inferensi
        )

        if not results or len(results) == 0:
            print(f"[process_image] YOLO tidak menghasilkan output untuk: {original_path}")
            return None, empty_counts

        result = results[0]

        # ── 4. Visualisasi Hasil (Bounding Boxes) ─────────────────────────────
        res_plotted = result.plot()
        out_filename = f"deteksi_{arah}_{time_str}_{filename}"
        out_path = os.path.join(upload_folder, out_filename)
        
        
        # Simpan hasil deteksi menggunakan imencode agar aman untuk semua path
        _, buf = cv2.imencode('.jpg', res_plotted)
        with open(out_path, 'wb') as f:
            f.write(buf.tobytes())

        # ── 5. Hitung 4 Objek sesuai Custom Map best.pt ───────────────────────
        counts = {
            'orang': 0,
            'bangkutaman': 0,
            'tempatsampah': 0,
            'pohonpeneduh': 0,
            'lampulalulintas': 0
        }

        for box in result.boxes:
            cls_id = int(box.cls)
            # Mapping class ID sesuai data.yaml training best.pt:
            # 0: bangkutaman | 1: lampulalulintas | 2: orang | 3: pohonpeneduh | 4: tempatsampah
            if cls_id == 0:
                counts['bangkutaman'] += 1
            elif cls_id == 1:
                counts['lampulalulintas'] += 1
            elif cls_id == 2:
                counts['orang'] += 1
            elif cls_id == 3:
                counts['pohonpeneduh'] += 1
            elif cls_id == 4:
                counts['tempatsampah'] += 1

        print(f"[process_image] {arah.upper()} selesai → {counts}")
        return out_filename, counts

    except Exception as e:
        print(f"[process_image] ERROR pada arah {arah}: {e}")
        import traceback
        traceback.print_exc()
        return None, empty_counts