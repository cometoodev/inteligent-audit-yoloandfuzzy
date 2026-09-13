# 🏙️ Sistem Audit Cerdas – Evaluasi Kualitas Ruang Publik

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](#)
[![YOLOv11](https://img.shields.io/badge/Model-YOLOv11-00FFFF?style=flat)](#)
[![Flask](https://img.shields.io/badge/Framework-Flask-000000?style=flat&logo=flask&logoColor=white)](#)
[![Scikit--Fuzzy](https://img.shields.io/badge/Fuzzy%20Logic-Mamdani-orange?style=flat)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

Sistem berbasis kecerdasan buatan (*Artificial Intelligence*) yang mengombinasikan **Computer Vision (YOLOv11)** dan **Sistem Inferensi Fuzzy Mamdani** untuk mengotomatisasi audit serta evaluasi kelayakan fasilitas ruang publik (seperti jalur pedestrian/trotoar dan fasilitas penunjang) di Kota Kendari.

Sistem ini membantu instansi perencana dan pengawas infrastruktur dalam melakukan penilaian objektif, cepat, dan berbasis bukti visual terhadap kondisi fasilitas publik.

---

## 🎯 Alur Kerja Sistem (Pipeline)

```text
[ Input Citra Ruang Publik ]
            │
            ▼
[ Deteksi Objek via YOLOv11 ]
(Fasilitas trotoar, kerusakan, guiding block, bollard, rintangan)
            │
            ▼
[ Ekstraksi Indikator & Metrik Lingkungan ]
            │
            ▼
[ Inferensi Logika Fuzzy Mamdani ]
(Fuzzifikasi ➔ Evaluasi Basis Aturan ➔ Agregasi ➔ Defuzzifikasi Centroid)
            │
            ▼
[ Dashboard Web Flask ]
(Skor Indeks Kelayakan, Visualisasi Bounding Box, & Rekomendasi Audit)
