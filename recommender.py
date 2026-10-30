import csv
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class MovieRecommender:
    """CPU-only content-based recommender using TF-IDF and cosine similarity."""

    def __init__(self, csv_path):
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Movie dataset not found: {csv_path}")
        self.movies = self._load_movies(csv_path)
        if not self.movies:
            raise ValueError("The movie dataset is empty.")
        self.genres = sorted({
            genre.strip()
            for movie in self.movies
            for genre in movie["genres"].split("|")
            if genre.strip() and genre.strip().lower() != "unknown"
        })
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=100000,
            sublinear_tf=True
        )
        corpus = [self._movie_text(movie) for movie in self.movies]
        self.movie_matrix = self.vectorizer.fit_transform(corpus)

    @staticmethod
    def _load_movies(path):
        movies = []
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            required = {"title", "genres"}
            if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
                raise ValueError("CSV must contain at least 'title' and 'genres' columns.")
            for row in reader:
                title = (row.get("title") or "").strip()
                if not title:
                    continue
                try:
                    year = int(row.get("year") or 0)
                except ValueError:
                    year = 0
                try:
                    rating = float(row.get("rating") or 0)
                except ValueError:
                    rating = 0.0
                movies.append({
                    "title": title,
                    "genres": (row.get("genres") or "Unknown").replace(",", "|"),
                    "overview": (row.get("overview") or "").strip(),
                    "year": year,
                    "rating": rating,
                    "poster_url": (row.get("poster_url") or "").strip()
                })
        return movies

    @staticmethod
    def _movie_text(movie):
        return " ".join([
            movie["title"],
            movie["genres"].replace("|", " "),
            movie["overview"]
        ])

    def recommend(self, query="", genre="", year_from=None, year_to=None,
                  min_rating=None, limit=10):
        if not query and not genre and not year_from and not year_to and min_rating is None:
            raise ValueError("Enter a movie preference or choose at least one filter.")

        # Query text is compared with movie metadata. Genre filter is also added
        # to the query so it contributes to relevance when natural-language text exists.
        query_parts = [query]
        if genre:
            query_parts.append(genre)
        query_text = " ".join(query_parts).strip()

        if query_text:
            query_vector = self.vectorizer.transform([query_text])
            scores = cosine_similarity(query_vector, self.movie_matrix).ravel()
        else:
            scores = [0.0] * len(self.movies)

        candidates = []
        for idx, movie in enumerate(self.movies):
            if genre and genre.lower() not in movie["genres"].lower().replace("|", " "):
                continue
            if year_from and (not movie["year"] or movie["year"] < year_from):
                continue
            if year_to and (not movie["year"] or movie["year"] > year_to):
                continue
            if min_rating is not None and movie["rating"] < min_rating:
                continue

            candidates.append((idx, float(scores[idx])))

        candidates.sort(key=lambda item: (item[1], self.movies[item[0]]["rating"]), reverse=True)
        output = []
        for idx, score in candidates[:limit]:
            movie = self.movies[idx]
            output.append({
                "title": movie["title"],
                "genres": movie["genres"].replace("|", ", "),
                "overview": movie["overview"] or "No description is available in the current dataset.",
                "year": movie["year"] or "Year unavailable",
                "rating": movie["rating"] if movie["rating"] else None,
                "match": round(score * 100, 1),
                "poster_url": movie["poster_url"]
            })
        return output
