from flask import Flask, jsonify, request, render_template_string, abort
import os

app = Flask(__name__)

# --- Sample Movies Catalog ---
CATALOG = [
    {"id": 1, "title": "Stranger Strings", "year": 2023, "rating": 8.7, "genre": "Sci-Fi"},
    {"id": 2, "title": "The Cloudfather", "year": 1972, "rating": 9.2, "genre": "Crime"},
    {"id": 3, "title": "Docker Things", "year": 2016, "rating": 8.8, "genre": "Thriller"},
    {"id": 4, "title": "Pipelines", "year": 2024, "rating": 8.1, "genre": "Drama"},
    {"id": 5, "title": "Kube Wars", "year": 2022, "rating": 8.4, "genre": "Action"},
]

# --- HTML Template ---
INDEX_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Mini Netflix</title>
  <style>
    body { font-family: Arial, sans-serif; background:#111; color:#eee; margin:0; }
    header { background:#141414; padding:15px; color:#e50914; font-weight:bold; }
    .grid { display:grid; grid-template-columns: repeat(auto-fill, minmax(200px,1fr)); gap:15px; padding:20px; }
    .card { background:#1f1f1f; padding:15px; border-radius:10px; }
    .title { font-size:18px; margin-bottom:5px; }
    .meta { font-size:14px; opacity:0.8; }
    a { display:inline-block; margin-top:10px; padding:6px 10px; background:#e50914; color:#fff; text-decoration:none; border-radius:6px; }
  </style>
</head>
<body>
  <header>MINI NETFLIX</header>
  <main>
    <div class="grid">
      {% for movie in movies %}
        <div class="card">
          <div class="title">{{ movie.title }}</div>
          <div class="meta">{{ movie.genre }} • {{ movie.year }} • ⭐ {{ movie.rating }}</div>
          <a href="/watch/{{ movie.id }}">Watch</a>
        </div>
      {% endfor %}
    </div>
  </main>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML, movies=CATALOG)

@app.route("/catalog")
def catalog():
    q = request.args.get("q", "").lower()
    results = [m for m in CATALOG if q in m["title"].lower() or q in m["genre"].lower()] if q else CATALOG
    return jsonify(results)

@app.route("/watch/<int:movie_id>")
def watch(movie_id):
    movie = next((m for m in CATALOG if m["id"] == movie_id), None)
    if not movie:
        abort(404)
    return jsonify({"message": f"Streaming '{movie['title']}' now!", "movie": movie})

@app.route("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
