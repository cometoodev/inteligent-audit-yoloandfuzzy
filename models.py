# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Inisialisasi DB kosong di sini
db = SQLAlchemy()

class User(UserMixin, db.Model):
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    audits = db.relationship('Audit', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Audit(db.Model):
    def __init__(self, **kwargs):
        super(Audit, self).__init__(**kwargs)
        
    id = db.Column(db.Integer, primary_key=True)
    lokasi = db.Column(db.String(150), nullable=False)
    lat = db.Column(db.String(50))
    long = db.Column(db.String(50))
    skor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    tanggal = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Menyimpan nama file gambar hasil deteksi per arah
    img_depan = db.Column(db.String(255))
    img_kanan = db.Column(db.String(255))
    img_kiri  = db.Column(db.String(255))

    # Menyimpan jumlah deteksi per kelas per arah (Depan)
    d_orang  = db.Column(db.Integer, default=0)
    d_bangku = db.Column(db.Integer, default=0)
    d_sampah = db.Column(db.Integer, default=0)
    d_pohon  = db.Column(db.Integer, default=0)
    d_lampu  = db.Column(db.Integer, default=0)
    # Kanan
    k_orang  = db.Column(db.Integer, default=0)
    k_bangku = db.Column(db.Integer, default=0)
    k_sampah = db.Column(db.Integer, default=0)
    k_pohon  = db.Column(db.Integer, default=0)
    k_lampu  = db.Column(db.Integer, default=0)
    # Kiri
    ki_orang  = db.Column(db.Integer, default=0)
    ki_bangku = db.Column(db.Integer, default=0)
    ki_sampah = db.Column(db.Integer, default=0)
    ki_pohon  = db.Column(db.Integer, default=0)
    ki_lampu  = db.Column(db.Integer, default=0)