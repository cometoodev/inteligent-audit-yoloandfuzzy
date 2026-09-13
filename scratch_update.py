import re

file_path = r'd:\Materi Kuliah\TUGAS AKHIR\1. Sistem\SistemAuditCerdas\templates\analysis.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add JS Dictionary & Helper
js_helper = """
    <script>
      const objectTranslationMap = {
          'orang': 'Pedestrian',
          'bangkutaman': 'Park Bench',
          'tempatsampah': 'Trash Bin',
          'pohonpeneduh': 'Shade Tree',
          'lampulalulintas': 'Street Light / Traffic Light'
      };

      function toEnglishLabel(label) {
          if (!label) return 'Unknown';
          let clean = label.toString().toLowerCase().trim();
          return objectTranslationMap[clean] || label;
      }
    </script>
"""
# Insert after <script id="mapData" ...> or at the end of head. Let's insert it right before <!-- ── DRAW BOUNDING BOXES ── -->
content = content.replace('// ── DRAW BOUNDING BOXES ──', js_helper.replace('<script>', '').replace('</script>', '') + '\n      // ── DRAW BOUNDING BOXES ──')

# 2. Update Bounding Box Label
content = content.replace("var label = cl + ' ' + Math.round((det.confidence || 0) * 100) + '%';",
                          "var label = toEnglishLabel(cl) + ' ' + Math.round((det.confidence || 0) * 100) + '%';")

# 3. Translate UI Labels
replacements = {
    "Tampak Depan": "Front View",
    "Tampak Kanan": "Right View",
    "Tampak Kiri": "Left View",
    "Orang": "Pedestrians",
    "Bangku Taman": "Park Benches",
    "Tempat Sampah": "Trash Bins",
    "Pohon Peneduh": "Shade Trees",
    "Lampu Lalu Lintas": "Street / Traffic Lights",
    "Arah Gabungan": "Combined View",
    "Depan": "Front",
    "Kanan": "Right",
    "Kiri": "Left"
}

# We need to be careful with "Depan", "Kanan", "Kiri" not to break keys in JSON or variable names.
# Better to replace specific occurrences.

# Chart labels
content = content.replace("labels: ['Orang', 'Bangku Taman', 'Tempat Sampah', 'Pohon Peneduh', 'Lampu Lalu Lintas']",
                          "labels: ['Pedestrians', 'Park Benches', 'Trash Bins', 'Shade Trees', 'Street / Traffic Lights']")

content = content.replace("label: 'Depan',", "label: 'Front View',")
content = content.replace("label: 'Kanan',", "label: 'Right View',")
content = content.replace("label: 'Kiri',", "label: 'Left View',")

# UI text
content = content.replace(">Tampak Depan<", ">Front View<")
content = content.replace(">Tampak Kanan<", ">Right View<")
content = content.replace(">Tampak Kiri<", ">Left View<")

content = content.replace(">Arah Gabungan<", ">Combined View<")
content = content.replace("Arahkan kamera ke depan objek &amp; jepret", "Point the camera to the front of the object & capture")

# Status Urgensi (LOS) translations in Jinja conditionals
content = content.replace("🟢 {{ result.status }}", "🟢 Routine Maintenance (LOS A)")
content = content.replace("🟡 {{ result.status }}", "🟡 Active Monitoring (LOS C/D)")
content = content.replace("⚪ {{ result.status }}", "⚪ Development Planning (LOS B)")
content = content.replace("🟠 {{ result.status }}", "🟠 Urgent Intervention (LOS E/F)")

# Also replace in the kamusFuzzy JS object just in case it's displayed, but user asked to completely replace the onclick function for the modal.

# Let's replace the whole onclick function for cardStatusUrgensi
old_onclick = '''document.getElementById('cardStatusUrgensi').onclick = function() {
                var rawChartData = document.getElementById('chartData');
                var parsedData = rawChartData ? JSON.parse(rawChartData.textContent) : null;
                var data = {
                    detail_deteksi: parsedData || {
                        depan: {}, kanan: {}, kiri: {}
                    },
                    status_fuzzy: statusFuzzyAsli
                };'''

new_onclick = '''document.getElementById('cardStatusUrgensi').onclick = function() {
                var rawChartData = document.getElementById('chartData');
                var parsedData = rawChartData ? JSON.parse(rawChartData.textContent) : null;
                var data = {
                    detail_deteksi: parsedData || {
                        depan: {}, kanan: {}, kiri: {}
                    },
                    status_fuzzy: statusFuzzyAsli
                };

                // 1. Ekstraksi Data Murni Per Arah Langsung dari Response Backend YOLOv11
                let d_orang   = parseInt(data.detail_deteksi.depan.orang || 0);
                let d_bangku  = parseInt(data.detail_deteksi.depan.bangkutaman || 0);
                let d_sampah  = parseInt(data.detail_deteksi.depan.tempatsampah || 0);
                let d_pohon   = parseInt(data.detail_deteksi.depan.pohonpeneduh || 0);
                let d_lampu   = parseInt(data.detail_deteksi.depan.lampulalulintas || 0);

                let k_orang   = parseInt(data.detail_deteksi.kanan.orang || 0);
                let k_bangku  = parseInt(data.detail_deteksi.kanan.bangkutaman || 0);
                let k_sampah  = parseInt(data.detail_deteksi.kanan.tempatsampah || 0);
                let k_pohon   = parseInt(data.detail_deteksi.kanan.pohonpeneduh || 0);
                let k_lampu   = parseInt(data.detail_deteksi.kanan.lampulalulintas || 0);

                let kr_orang  = parseInt(data.detail_deteksi.kiri.orang || 0);
                let kr_bangku = parseInt(data.detail_deteksi.kiri.bangkutaman || 0);
                let kr_sampah = parseInt(data.detail_deteksi.kiri.tempatsampah || 0);
                let kr_pohon  = parseInt(data.detail_deteksi.kiri.pohonpeneduh || 0);
                let kr_lampu  = parseInt(data.detail_deteksi.kiri.lampulalulintas || 0);

                let statusAsli = data.status_fuzzy; 

                let directionAnalysis = [];
                let upgradeRecommendations = [];
                let maintenanceProcedures = [];

                // ==========================================
                // SECTOR 1: FRONT VIEW ANALYSIS
                // ==========================================
                let frontText = [];
                frontText.push(d_orang <= 2 ? `pedestrian activity is low (${d_orang} persons, Low MF [0, 0, 3.5])` : `pedestrian activity is high (${d_orang} persons, High MF [2.5, 6, 10])`);
                
                if (d_bangku >= 3) {
                    frontText.push(`park bench availability is adequate (${d_bangku} units, Adequate MF [3, 5, 7])`);
                } else {
                    frontText.push(`park bench availability is sub-optimal (${d_bangku} units, Minim MF [0, 0, 3])`);
                    upgradeRecommendations.push(`Installation of additional pedestrian park benches in the Front View zone`);
                }

                if (d_sampah >= 1) {
                    frontText.push(`sanitation facilities are adequate (${d_sampah} units, Adequate MF [0.5, 2, 5])`);
                } else {
                    frontText.push(`sanitation facilities are sub-optimal (${d_sampah} units, Minim MF [0, 0, 1])`);
                    upgradeRecommendations.push(`Provision of new segregated waste bins in the Front View zone`);
                }
                directionAnalysis.push(`<b>📍 Front View:</b> ${frontText.join(', ')}`);

                // ==========================================
                // SECTOR 2: RIGHT VIEW ANALYSIS
                // ==========================================
                let rightText = [];
                rightText.push(k_orang <= 2 ? `pedestrian activity is low (${k_orang} persons, Low MF [0, 0, 3.5])` : `pedestrian activity is high (${k_orang} persons, High MF [2.5, 6, 10])`);
                
                if (k_pohon >= 1) {
                    rightText.push(`shade tree canopy is adequate (${k_pohon} trees, Adequate MF [0.5, 1.5, 3])`);
                } else {
                    rightText.push(`shade tree canopy is sub-optimal (${k_pohon} trees, Minim MF [0, 0, 1])`);
                    upgradeRecommendations.push(`Planting of deep-rooted shade trees along the Right sidewalk corridor`);
                }

                if (k_bangku >= 3) {
                    rightText.push(`park bench availability is adequate (${k_bangku} units, Adequate MF [3, 5, 7])`);
                } else {
                    rightText.push(`park bench availability is sub-optimal (${k_bangku} units, Minim MF [0, 0, 3])`);
                    upgradeRecommendations.push(`Installation of additional pedestrian park benches in the Right View zone`);
                }
                directionAnalysis.push(`<b>📍 Right View:</b> ${rightText.join(', ')}`);

                // ==========================================
                // SECTOR 3: LEFT VIEW ANALYSIS
                // ==========================================
                let leftText = [];
                leftText.push(kr_orang <= 2 ? `pedestrian activity is low (${kr_orang} persons, Low MF [0, 0, 3.5])` : `pedestrian activity is high (${kr_orang} persons, High MF [2.5, 6, 10])`);
                
                if (kr_pohon >= 1) {
                    leftText.push(`shade tree canopy is adequate (${kr_pohon} trees, Adequate MF [0.5, 1.5, 3])`);
                } else {
                    leftText.push(`shade tree canopy is sub-optimal (${kr_pohon} trees, Minim MF [0, 0, 1])`);
                    upgradeRecommendations.push(`Planting of deep-rooted shade trees along the Left sidewalk corridor`);
                }

                if (kr_lampu >= 1) {
                    leftText.push(`street lighting is available (${kr_lampu} units, Available MF [0.5, 1.5, 5])`);
                } else {
                    leftText.push(`street lighting is below ideal threshold (${kr_lampu} units, Unavailable MF [0, 0, 1])`);
                    upgradeRecommendations.push(`Installation or repair of street lighting luminaires in the Left crossing zone`);
                }
                directionAnalysis.push(`<b>📍 Left View:</b> ${leftText.join(', ')}`);

                // ==========================================
                // GLOBAL MAINTENANCE PROCEDURES (EXISTING ASSETS)
                // ==========================================
                let totalBangku = d_bangku + k_bangku + kr_bangku;
                let totalSampah = d_sampah + k_sampah + kr_sampah;
                let totalPohon  = d_pohon + k_pohon + kr_pohon;
                let totalLampu  = d_lampu + k_lampu + kr_lampu;

                if (totalBangku > 0) maintenanceProcedures.push("Park Bench Stewardship: Regular inspection for metal corrosion, anti-termite wood coating, and structural bolt tightening.");
                if (totalSampah > 0) maintenanceProcedures.push("Sanitation Maintenance: Scheduled daily waste container emptying and periodic bin washing for corridor hygiene.");
                if (totalPohon > 0)  maintenanceProcedures.push("Urban Canopy Management: Periodic branch pruning to prevent obstruction of street lights/signage and soil fertilization.");
                if (totalLampu > 0)  maintenanceProcedures.push("Electrical Fixture Calibration: Cleaning of protective lamp covers and stability check of electrical circuitry.");

                // ==========================================
                // CONTEXTUAL SPATIAL NOTES (DICTIONARY IN ENGLISH)
                // ==========================================
                const englishContextNotes = {
                    'Pemeliharaan': '💡 <b>Field Context Notes (LOS A):</b> The absence of certain street furniture items in specific camera angles does not indicate a deficit, but rather functional spatial adjustments, such as maintaining clear zones at pedestrian crossings (zebra cross) or keeping tactile paving unblocked.',
                    
                    'Perencanaan': '💡 <b>Field Context Notes (LOS B):</b> Recommendations for installing new park benches MUST exclude active vehicle access points (driveways/building entrance gates) for traffic safety. Additionally, waste bins do not need to be placed at every spot, but should be spaced at ideal 20-meter intervals at key pedestrian gathering points.',
                    
                    'Monitoring': '💡 <b>Field Context Notes (LOS C/D):</b> Monitoring and facility placement are prioritized at intersections or sharp corners prone to side friction conflicts (e.g., illegal parking or street vendor encroachment). Keeping corners or fire hydrants clear of street furniture is mandatory to preserve sight distance (clear zone).',
                    
                    'Intervensi': '💡 <b>Field Context Notes (LOS E/F):</b> Major emergency infrastructure improvements must be preceded by a sidewalk geometric audit. Adding new facilities MUST NOT reduce the effective minimum pedestrian clear width (at least 1.5 meters) and must account for existing utility poles (e.g., PLN power poles, internet provider poles, or billboards) to prevent dual obstructions.'
                };

                // Category Determination for Modal Styling & Notes
                let statusCategory = 'Pemeliharaan';
                let statusDisplayEN = 'Routine Maintenance (LOS A)';

                if (statusAsli.includes('Perencanaan')) {
                    statusCategory = 'Perencanaan';
                    statusDisplayEN = 'Development Planning (LOS B)';
                } else if (statusAsli.includes('Monitoring')) {
                    statusCategory = 'Monitoring';
                    statusDisplayEN = 'Active Monitoring (LOS C/D)';
                } else if (statusAsli.includes('Intervensi')) {
                    statusCategory = 'Intervensi';
                    statusDisplayEN = 'Urgent Intervention (LOS E/F)';
                }

                // Modal Header Styling Map
                const styleMap = {
                    'Pemeliharaan': { header: 'linear-gradient(135deg, #198754, #2ec4b6)', border: '#198754' },
                    'Perencanaan': { header: 'linear-gradient(135deg, #0d6efd, #00b4d8)', border: '#0d6efd' },
                    'Monitoring': { header: 'linear-gradient(135deg, #f59e0b, #ffb703)', border: '#f59e0b' },
                    'Intervensi': { header: 'linear-gradient(135deg, #dc3545, #ff4d6d)', border: '#dc3545' }
                };

                // Constructing English HTML Output
                let htmlAnalysis = "<b>Multi-Angle Spatial Analysis (YOLOv11 Detection Output):</b><br><br>" + directionAnalysis.join('<br><br>');
                
                let htmlRecommendation = "<b>Tactical Policy Recommendations (Ref: SE PUPR No. 02/SE/M/2018):</b><br><br>";
                
                if (upgradeRecommendations.length > 0) {
                    htmlRecommendation += `<b>📋 [INFRASTRUCTURE UPGRADE STRATEGY]:</b><br>` + upgradeRecommendations.map((action, i) => `${i+1}. ${action}`).join('<br>') + `<br><br>`;
                }
                if (maintenanceProcedures.length > 0) {
                    htmlRecommendation += `<b>⚙️ [ROUTINE ASSET MAINTENANCE PROCEDURES]:</b><br>` + maintenanceProcedures.map((proc, i) => `${i+1}. ${proc}`).join('<br>');
                }

                // Append English Context Note Box
                htmlRecommendation += `<br><br><div class="p-3 bg-white border border-light shadow-sm" style="border-radius: 12px; font-style: normal; color: #495057; border-left: 4px solid #6c757d !important;">${englishContextNotes[statusCategory]}</div>`;

                // Render Data into Bootstrap Modal Elements
                document.getElementById('modalStatusTitle').innerText = `Spatial Audit & Evaluation: ${statusDisplayEN}`;
                document.getElementById('modalHeaderColor').style.background = styleMap[statusCategory].header;
                document.getElementById('txtModalAnalisis').innerHTML = htmlAnalysis;
                document.getElementById('txtModalRekomendasi').innerHTML = htmlRecommendation;
                document.getElementById('modalBorderRekomendasi').style.borderLeftColor = styleMap[statusCategory].border;
                
                // Trigger Modal Bootstrap
                var myModal = new bootstrap.Modal(document.getElementById('modalRekomendasiDosen'));
                myModal.show();
            };
'''

# Use regex to find and replace the whole block of document.getElementById('cardStatusUrgensi').onclick = function() { ... };
# We can find the start index of old_onclick, and find the end of the block.
import re
start_idx = content.find("document.getElementById('cardStatusUrgensi').onclick = function() {")
if start_idx != -1:
    end_idx = content.find("        // Panggil Modal Bootstrap", start_idx)
    end_idx = content.find("};", end_idx) + 2
    
    if end_idx > start_idx + 10:
        content = content[:start_idx] + new_onclick + content[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Update complete")
