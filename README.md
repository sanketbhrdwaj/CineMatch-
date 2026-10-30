# CineMatch — CPU-only Movie Recommendation Website

A responsive Flask website for laptop, tablet and mobile. It uses a content-based recommendation baseline:
- **TF-IDF** converts movie titles, genres and descriptions into sparse text vectors.
- **Cosine similarity** compares a user's natural-language request with each movie vector.
- Optional genre, year and minimum-rating filters narrow the candidate list.
- No GPU, CUDA, neural network or paid API is required.

## Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Internet connection only for installing Python packages; the app itself runs locally.

## Run in VS Code

Open this folder in VS Code, then open Terminal.

### Windows
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
If PowerShell blocks activation, use Command Prompt:
```cmd
.venv\\Scripts\\activate.bat
```

### macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

To test from a phone on the same Wi-Fi, find your laptop's local IP address and open:
`http://YOUR-LAPTOP-IP:5000`
Allow Python through the laptop firewall if prompted. Both devices must be on the same network.

## Dataset format

The included `data/movies.csv` is a small demonstration dataset. Replace it with your own larger CSV using these column names:

| Column | Required? | Description |
|---|---|---|
| title | Yes | Movie title |
| genres | Yes | Genres separated by `|` |
| overview | No | Plot summary / descriptive text |
| year | No | Release year |
| rating | No | Numeric rating |
| poster_url | No | Optional poster image URL |

The app reads the CSV and builds the TF-IDF matrix at startup. Large catalogs may require more RAM and startup time. For a million-row dataset, use a sparse matrix, avoid dense similarity matrices, cache/precompute vectors, and consider a database or indexed candidate retrieval. This starter intentionally uses a simple CPU-friendly query-to-catalog similarity calculation.

## Project structure
```text
CineMatch_CPU_Website/
├── app.py
├── recommender.py
├── requirements.txt
├── README.md
├── data/
│   └── movies.csv
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    └── js/app.js
```

## Important model notes
This is content-based retrieval, not a supervised rating-prediction model. The match percentage is cosine similarity scaled for display; it is **not** a probability that a user will like the film. The demo data is not a million-movie dataset. Add a properly licensed, cleaned catalog before public deployment.

## Deployment
For a production deployment, use a WSGI server such as Gunicorn (Linux hosting) or Waitress (Windows), set `debug=False`, configure a suitable host, and check the hosting provider's memory limits. Do not expose Flask's development server as a production server.
"# CineMatch-" 
