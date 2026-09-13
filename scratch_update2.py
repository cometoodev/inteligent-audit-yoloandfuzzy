import re

file_path = r'd:\Materi Kuliah\TUGAS AKHIR\1. Sistem\SistemAuditCerdas\templates\analysis.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Dictionary of remaining UI texts to replace
replacements = {
    ">Orang / Pejalan Kaki<": ">Pedestrians<",
    ">Bangku Taman<": ">Park Benches<",
    ">Tempat Sampah<": ">Trash Bins<",
    ">Pohon Peneduh<": ">Shade Trees<",
    ">Lampu Lalu Lintas<": ">Street / Traffic Lights<",
    # Catch any remaining instances just in case
    ">Orang<": ">Pedestrians<"
}

for old_text, new_text in replacements.items():
    content = content.replace(old_text, new_text)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Update 2 complete")
