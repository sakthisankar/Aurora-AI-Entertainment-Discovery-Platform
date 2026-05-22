import pandas as pd
import nltk
import pickle
from pathlib import Path
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ── Download NLTK data if needed ─────────────────────────────────────────────
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)

# ── Load Dataset ─────────────────────────────────────────────────────────────
CSV_PATH = Path("spotify_millsongdata.csv")

if not CSV_PATH.exists():
    raise FileNotFoundError(
        f"\n  ✗ Could not find '{CSV_PATH}'.\n"
        "  Download the Spotify Million Song dataset and place it in the project root.\n"
        "  Dataset source: https://www.kaggle.com/datasets/notshrirang/spotify-million-song-dataset\n"
    )

print("▸ Loading dataset…")
df = pd.read_csv("spotify_millsongdata.csv")
print(f"  Found {len(df):,} songs. Sampling 5,000 for performance.")

df = df.sample(5000, random_state=42).reset_index(drop=True)

# Keep only essential columns
if "text" not in df.columns:
    raise ValueError("Dataset must have a 'text' column containing song lyrics.")
if "song" not in df.columns:
    raise ValueError("Dataset must have a 'song' column with song titles.")
if "artist" not in df.columns:
    df["artist"] = "Unknown Artist"

# ── Text Preprocessing ───────────────────────────────────────────────────────
print("▸ Preprocessing lyrics…")
df["text"] = (
    df["text"]
    .astype(str)
    .str.lower()
    .str.replace(r"[^a-z\s]", " ", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

stemmer = PorterStemmer()

def tokenize_and_stem(text: str) -> str:
    tokens  = nltk.word_tokenize(text)
    stemmed = [stemmer.stem(w) for w in tokens if len(w) > 2]
    return " ".join(stemmed)

df["text"] = df["text"].apply(tokenize_and_stem)
print("  Stemming complete.")

# ── TF-IDF Vectorisation ─────────────────────────────────────────────────────
print("▸ Building TF-IDF matrix…")
tfidf  = TfidfVectorizer(analyzer="word", stop_words="english", max_features=10_000)
matrix = tfidf.fit_transform(df["text"])
print(f"  Matrix shape: {matrix.shape}")

# ── Cosine Similarity ────────────────────────────────────────────────────────
print("▸ Computing cosine similarity…")
similarity = cosine_similarity(matrix)
print(f"  Similarity matrix: {similarity.shape}")

# ── Persist ──────────────────────────────────────────────────────────────────
print("▸ Saving model artefacts…")
pickle.dump(df,         open("df.pkl",         "wb"), protocol=4)
pickle.dump(similarity, open("similarity.pkl", "wb"), protocol=4)

print("\n  ✓ df.pkl          saved")
print("  ✓ similarity.pkl  saved")
print("\nReady — run 'streamlit run app.py' to launch Aurora.\n")
