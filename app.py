from flask import Flask, render_template, request, jsonify
from recommender import MovieRecommender

app = Flask(__name__)
recommender = MovieRecommender("data/movies.csv")

@app.route("/")
def home():
    return render_template("index.html", genres=recommender.genres)

@app.post("/recommend")
def recommend():
    payload = request.get_json(silent=True) or {}
    query = (payload.get("query") or "").strip()
    genre = (payload.get("genre") or "").strip()
    year_from = payload.get("year_from")
    year_to = payload.get("year_to")
    min_rating = payload.get("min_rating")
    try:
        results = recommender.recommend(
            query=query,
            genre=genre,
            year_from=int(year_from) if year_from else None,
            year_to=int(year_to) if year_to else None,
            min_rating=float(min_rating) if min_rating else None,
            limit=10
        )
        return jsonify({"results": results, "count": len(results)})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

@app.route("/health")
def health():
    return jsonify({"status": "ok", "movies_loaded": len(recommender.movies)})

if __name__ == "__main__":
    # Local development server. For deployment, use a production WSGI server.
    app.run(host="0.0.0.0", port=5000, debug=True)
