const button = document.getElementById("search-btn");
const statusBox = document.getElementById("status");
const resultsBox = document.getElementById("results");
const countBox = document.getElementById("result-count");

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
  })[ch]);
}

function movieCard(movie) {
  const poster = movie.poster_url
    ? `<img src="${escapeHtml(movie.poster_url)}" alt="${escapeHtml(movie.title)} poster" loading="lazy" onerror="this.parentElement.innerHTML='CINEMATCH'">`
    : "CINEMATCH";
  const rating = movie.rating ? `★ ${Number(movie.rating).toFixed(1)}` : "Rating unavailable";
  const year = typeof movie.year === "number" ? movie.year : movie.year;
  return `<article class="movie-card">
    <div class="poster">${poster}</div>
    <div class="movie-info">
      <h3>${escapeHtml(movie.title)}</h3>
      <div class="meta">${escapeHtml(movie.genres)} · ${escapeHtml(year)}</div>
      <p>${escapeHtml(movie.overview)}</p>
      <div class="scores"><span class="score">${escapeHtml(rating)}</span><span class="score">${Number(movie.match).toFixed(1)}% content match</span></div>
    </div>
  </article>`;
}

button.addEventListener("click", async () => {
  const payload = {
    query: document.getElementById("query").value.trim(),
    genre: document.getElementById("genre").value,
    year_from: document.getElementById("year-from").value,
    year_to: document.getElementById("year-to").value,
    min_rating: document.getElementById("rating").value
  };
  if (!payload.query && !payload.genre && !payload.year_from && !payload.year_to && !payload.min_rating) {
    statusBox.textContent = "Please describe a movie preference or choose at least one filter.";
    return;
  }
  button.disabled = true;
  button.textContent = "Finding matches...";
  statusBox.textContent = "Comparing your preferences with the movie catalog...";
  resultsBox.innerHTML = "";
  countBox.textContent = "";
  try {
    const response = await fetch("/recommend", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not get recommendations.");
    countBox.textContent = `${data.count} results`;
    if (!data.results.length) {
      statusBox.textContent = "No movies matched those filters. Try widening your search.";
    } else {
      statusBox.textContent = "Here are the closest matches in the current dataset.";
      resultsBox.innerHTML = data.results.map(movieCard).join("");
    }
  } catch (error) {
    statusBox.textContent = error.message;
  } finally {
    button.disabled = false;
    button.innerHTML = 'Find my movies <span>→</span>';
  }
});
