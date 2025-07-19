from flask import Flask, jsonify
from anime_scraper import search_anime
# DIUBAH: Kita import kedua fungsi dari character_scraper
from character_scraper import search_character, get_character_details 

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Unofficial MyAnimeList API",
        "endpoints": {
            "anime_search": "/anime/<name>",
            "character_search_by_name": "/character/<name>",
            "character_search_by_id": "/character/<uid>"
        },
        "author": "Daffa Aditya Pratama"
    })

@app.route('/anime/<string:query>')
def get_anime(query):
    """
    Endpoint untuk mencari anime.
    Contoh: /anime/naruto
    """
    result = search_anime(query)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result)

# DIUBAH: Logika di dalam fungsi ini diperbarui
@app.route('/character/<string:query>')
def get_character(query):
    """
    Endpoint untuk mencari karakter berdasarkan nama atau UID.
    Contoh: /character/naruto uzumaki atau /character/1
    """
    # Cek apakah query yang dimasukkan adalah angka (ID)
    if query.isdigit():
        uid = query
        # Langsung buat URL ke halaman karakter berdasarkan UID
        url = f"https://myanimelist.net/character/{uid}"
        # Panggil fungsi untuk mengambil detail langsung dari URL
        result = get_character_details(url)
    else:
        # Jika bukan angka, lakukan pencarian seperti sebelumnya
        result = search_character(query)

    if "error" in result:
        return jsonify(result), 404
    return jsonify(result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)