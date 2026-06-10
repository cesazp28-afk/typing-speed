from flask import Flask, render_template, jsonify, request
import random
import json
import os

# ── Inisialisasi Flask ────────────────────────────────────────────────────────
# __name__ → Flask pakai nama file ini sebagai titik referensi folder
app = Flask(__name__)

# ── Data Kata ─────────────────────────────────────────────────────────────────
WORDS = {
    "easy": [
        "yang", "dan", "di", "ke", "dari", "untuk", "dengan", "pada",
        "adalah", "tidak", "akan", "sudah", "karena", "jika", "agar",
        "dalam", "sebagai", "saat", "lebih", "bisa", "harus", "masih",
        "saya", "kamu", "dia", "mereka", "kami", "kita", "orang",
        "rumah", "sekolah", "makan", "minum", "belajar", "kerja",
        "jalan", "mobil", "motor", "teman", "keluarga", "buku",
        "uang", "waktu", "hari", "bulan", "tahun", "pagi", "malam"
    ],
    "medium": [
        "politik", "demokrasi", "pemilu", "pilkada", "parlemen",
        "anggaran", "efisiensi", "kabinet", "menteri", "presiden",
        "wakil", "rakyat", "aspirasi", "kebijakan", "regulasi",
        "konstitusi", "legislatif", "eksekutif", "yudikatif", "daerah",
        "provinsi", "kabupaten", "kota", "gubernur", "bupati",
        "walikota", "dpr", "dprd", "apbn", "apbd",
        "pajak", "subsidi", "investasi", "ekonomi", "fiskal",
        "birokrasi", "pegawai", "pppk", "asn", "pelayanan",
        "publik", "transparansi", "akuntabilitas", "reformasi", "program",
        "koperasi", "pendidikan", "kesehatan", "infrastruktur", "energi"
    ],
    "hard": [
        "mbg", "gizi", "gratis", "dapur", "anggaran", "efisiensi",
        "rupiah", "dolar", "kurs", "inflasi", "defisit", "utang",
        "ekonomi", "investor", "pasar", "saham", "ihsg", "fiskal",
        "pertamax", "pertalite", "bbm", "subsidi", "energi", "minyak",
        "harga", "naik", "turun", "mahal", "hemat", "daya",
        "beli", "rakyat", "buruh", "petani", "nelayan", "usaha",
        "kerja", "pangan", "beras", "impor", "ekspor", "produksi",
        "kabinet", "menteri", "presiden", "kebijakan", "program",
        "evaluasi", "korupsi", "transparansi", "pengawasan", "publik"
    ]
}

# ── File leaderboard ──────────────────────────────────────────────────────────
# Simpan di folder yang sama dengan app.py
LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), "leaderboard.json")

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return {"easy": [], "medium": [], "hard": []}

def save_leaderboard(data):
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Routes ────────────────────────────────────────────────────────────────────

# GET /
# Tampilkan halaman utama (index.html dari folder templates/)
@app.route("/")
def index():
    return render_template("index.html")


# GET /api/words?level=easy
# Kirim 15 kata acak sesuai level dalam format JSON
@app.route("/api/words")
def get_words():
    # request.args → query string dari URL (?level=easy)
    level = request.args.get("level", "medium")

    # Guard: kalau level tidak valid, default ke medium
    if level not in WORDS:
        level = "medium"

    word_pool = WORDS[level]
    chosen    = random.sample(word_pool, min(15, len(word_pool)))
    text      = " ".join(chosen)

    # jsonify() → konversi dict Python ke response JSON
    return jsonify({"text": text, "level": level})


# POST /api/score
# Terima skor dari browser, simpan ke leaderboard
@app.route("/api/score", methods=["POST"])
def save_score():
    # request.get_json() → parse body request sebagai JSON
    data     = request.get_json()
    name     = data.get("name", "Anonymous")
    wpm      = data.get("wpm", 0)
    accuracy = data.get("accuracy", 0)
    level    = data.get("level", "medium")

    if level not in ["easy", "medium", "hard"]:
        return jsonify({"error": "Level tidak valid"}), 400

    board = load_leaderboard()
    board[level].append({"name": name, "wpm": wpm, "accuracy": accuracy})
    board[level].sort(key=lambda x: x["wpm"], reverse=True)
    board[level] = board[level][:5]
    save_leaderboard(board)

    return jsonify({"message": "Skor disimpan!", "board": board[level]})


# GET /api/leaderboard
# Kirim semua data leaderboard sebagai JSON
@app.route("/api/leaderboard")
def get_leaderboard():
    return jsonify(load_leaderboard())


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # debug=True → auto-reload kalau ada perubahan kode (jangan pakai di production)
    # host="0.0.0.0" → bisa diakses dari HP lain di jaringan yang sama
    app.run(debug=True, host="0.0.0.0", port=5000)

