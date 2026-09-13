import os
from flask import Flask
from flask_login import LoginManager

# Import dari file terpisah yang baru kita buat
from models import db, User
from routes import main

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasia-skripsi-anda-123'

# Konfigurasi Folder & Database
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mysql@localhost/SistemAuditCerdas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Sambungkan Database & Login Manager ke App
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login' # Mengarah ke route di dalam blueprint 'main'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Daftarkan semua URL dari file routes.py
app.register_blueprint(main)

# Fungsi membuat Admin awal
def create_initial_data():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')  # type: ignore[call-arg]
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print(">>> Database & Admin Siap!")

if __name__ == '__main__':
    create_initial_data()

    # ── Integrasi pyngrok untuk akses HTTPS via HP ──────────────────────────
    try:
        from pyngrok import ngrok, conf

        # Set authtoken agar sesi ngrok terautentikasi
        NGROK_AUTH_TOKEN = "35SXE9aldtLUGJs6sO5jCwR1MiK_59EaEoWT66jAzkZFmmwyW"
        conf.get_default().auth_token = NGROK_AUTH_TOKEN

        # Buka tunnel HTTP pada port 5000
        public_tunnel = ngrok.connect("5000", "http")
        public_url = public_tunnel.public_url or ""

        print("\n" + "=" * 60)
        print("  ✅  Smart Audit – Tunnel Ngrok Berhasil Dibuka!")
        print("=" * 60)
        print(f"  🌐  URL Publik  : {public_url}")
        print(f"  🔒  HTTPS URL  : {public_url.replace('http://', 'https://')}")
        print("  📱  Scan QR atau buka URL di browser HP Anda")
        print("=" * 60 + "\n")

    except ImportError:
        print("\n⚠️  [WARNING] Library 'pyngrok' tidak ditemukan.")
        print("   Jalankan: pip install pyngrok")
        print("   Aplikasi tetap berjalan secara lokal.\n")

    except Exception as e:
        print(f"\n❌  [ERROR] Ngrok gagal terhubung: {e}")
        print("   Periksa koneksi internet dan authtoken Anda.")
        print("   Aplikasi tetap berjalan secara lokal.\n")

    # Jalankan Flask dengan threaded=True agar deteksi YOLOv11
    # tidak memblokir koneksi tunnel saat diakses dari HP
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)