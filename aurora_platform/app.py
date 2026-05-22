import streamlit as st
import requests
import pandas as pd
import pickle
import os
import time
import re
from pathlib import Path

# ─── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Aurora — Entertainment Discovery",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS — Light, editorial, world-class ─────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    background: #F9F7F4 !important;
    color: #1A1714 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Aurora Header ── */
.aurora-nav {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 56px;
    background: rgba(249, 247, 244, 0.95);
    border-bottom: 1px solid rgba(26, 23, 20, 0.08);
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(12px);
}

.aurora-logo {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    font-weight: 600;
    color: #1A1714;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.aurora-logo span {
    color: #C9773A;
}

.nav-tagline {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    color: #8C8680;
    text-transform: uppercase;
}

/* ── Tab Switcher ── */
.tab-switcher {
    display: flex;
    background: #EFEDE8;
    border-radius: 100px;
    padding: 4px;
    gap: 2px;
}

.tab-btn {
    padding: 8px 24px;
    border-radius: 100px;
    border: none;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    color: #8C8680;
    background: transparent;
}

.tab-btn.active {
    background: #1A1714;
    color: #F9F7F4;
}

/* ── Hero Section ── */
.hero-section {
    padding: 72px 56px 48px;
    max-width: 1400px;
    margin: 0 auto;
}

.hero-overline {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #C9773A;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(42px, 5vw, 68px);
    font-weight: 600;
    line-height: 1.1;
    color: #1A1714;
    letter-spacing: -2px;
    margin-bottom: 20px;
}

.hero-title em {
    font-style: italic;
    color: #C9773A;
}

.hero-subtitle {
    font-size: 17px;
    color: #6B6560;
    font-weight: 300;
    line-height: 1.7;
    max-width: 540px;
    margin-bottom: 48px;
}

/* ── Search Container ── */
.search-wrap {
    background: #FFFFFF;
    border: 1px solid rgba(26, 23, 20, 0.12);
    border-radius: 16px;
    padding: 24px 28px;
    max-width: 720px;
    box-shadow: 0 4px 32px rgba(26, 23, 20, 0.06);
    margin-bottom: 56px;
}

.search-label {
    font-size: 11px;
    letter-spacing: 2px;
    color: #8C8680;
    text-transform: uppercase;
    font-family: 'DM Mono', monospace;
    margin-bottom: 12px;
}

/* ── Selectbox & Buttons overrides ── */
.stSelectbox > div > div {
    background: #F4F2EE !important;
    border: 1px solid rgba(26,23,20,0.1) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    color: #1A1714 !important;
    transition: border-color 0.2s !important;
}

.stSelectbox > div > div:hover {
    border-color: rgba(26,23,20,0.25) !important;
}

.stButton > button {
    background: #1A1714 !important;
    color: #F9F7F4 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    padding: 12px 32px !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background: #2D2925 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(26,23,20,0.2) !important;
}

/* ── Section Divider ── */
.section-header {
    padding: 0 56px;
    max-width: 1400px;
    margin: 0 auto 32px;
    display: flex;
    align-items: center;
    gap: 16px;
}

.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #C9773A;
    text-transform: uppercase;
}

.section-line {
    flex: 1;
    height: 1px;
    background: rgba(26,23,20,0.08);
}

/* ── Recommendation Grid ── */
.recs-grid {
    padding: 0 56px 72px;
    max-width: 1400px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 20px;
}

/* ── Card ── */
.rec-card {
    background: #FFFFFF;
    border: 1px solid rgba(26,23,20,0.07);
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.3s ease;
    cursor: default;
    position: relative;
}

.rec-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 40px rgba(26,23,20,0.1);
    border-color: rgba(26,23,20,0.15);
}

.card-image-wrap {
    position: relative;
    width: 100%;
    padding-top: 100%;
    overflow: hidden;
    background: #EFEDE8;
}

.card-image-wrap img {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    object-fit: cover;
    transition: transform 0.4s ease;
}

.rec-card:hover .card-image-wrap img {
    transform: scale(1.05);
}

.card-rank {
    position: absolute;
    top: 10px; left: 10px;
    background: rgba(249,247,244,0.95);
    border-radius: 6px;
    padding: 3px 8px;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: #8C8680;
    letter-spacing: 1px;
    backdrop-filter: blur(4px);
}

.card-body {
    padding: 16px;
}

.card-title {
    font-family: 'Playfair Display', serif;
    font-size: 15px;
    font-weight: 600;
    color: #1A1714;
    line-height: 1.3;
    margin-bottom: 6px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.card-meta {
    font-size: 12px;
    color: #8C8680;
    font-weight: 300;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.card-tag {
    display: inline-block;
    margin-top: 10px;
    padding: 3px 10px;
    border-radius: 100px;
    font-size: 10px;
    letter-spacing: 1px;
    font-family: 'DM Mono', monospace;
    text-transform: uppercase;
}

.tag-music {
    background: #FFF0E4;
    color: #C9773A;
}

.tag-movie {
    background: #E8EFF9;
    color: #3A70C9;
}

/* ── Placeholder card ── */
.card-placeholder {
    background: #F4F2EE;
    border-radius: 16px;
    padding: 40px 20px;
    text-align: center;
    border: 1.5px dashed rgba(26,23,20,0.1);
}

.placeholder-icon {
    font-size: 32px;
    margin-bottom: 12px;
    opacity: 0.3;
}

.placeholder-text {
    font-size: 13px;
    color: #8C8680;
    font-weight: 300;
}

/* ── Stats Bar ── */
.stats-bar {
    padding: 24px 56px;
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    gap: 48px;
    border-top: 1px solid rgba(26,23,20,0.07);
    border-bottom: 1px solid rgba(26,23,20,0.07);
    margin-bottom: 56px;
    background: #FDFCFA;
}

.stat-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 600;
    color: #1A1714;
    letter-spacing: -1px;
}

.stat-desc {
    font-size: 12px;
    color: #8C8680;
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px;
}

/* ── Spinner ── */
.stSpinner > div {
    border-color: #C9773A transparent transparent transparent !important;
}

/* ── Alert / Info ── */
.stAlert {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Loading state ── */
.loading-wrap {
    text-align: center;
    padding: 48px;
}

.loading-text {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 2px;
    color: #8C8680;
    text-transform: uppercase;
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.4; }
    50% { opacity: 1; }
}

/* ── Footer ── */
.aurora-footer {
    padding: 32px 56px;
    border-top: 1px solid rgba(26,23,20,0.07);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.footer-logo {
    font-family: 'Playfair Display', serif;
    font-size: 16px;
    color: #8C8680;
}

.footer-note {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: #B8B3AE;
    letter-spacing: 1px;
}

/* ── Responsive ── */
@media (max-width: 1100px) {
    .recs-grid { grid-template-columns: repeat(3, 1fr); }
    .aurora-nav, .hero-section, .recs-grid, .stats-bar { padding-left: 28px; padding-right: 28px; }
}

@media (max-width: 700px) {
    .recs-grid { grid-template-columns: repeat(2, 1fr); }
    .hero-title { font-size: 36px; }
}

/* Mode toggle */
.mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px;
}

.mode-music { background: #FFF0E4; color: #C9773A; }
.mode-movie { background: #E8EFF9; color: #3A70C9; }

/* Fix multiselect area */
div[data-baseweb="select"] span {
    font-family: 'DM Sans', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


# ─── iTunes API ─────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False, ttl=3600)
def get_itunes_artwork(song_name: str, artist_name: str) -> str:
    """Fetch album art from iTunes Search API (free, no auth). Results cached 1hr."""
    try:
        query = f"{song_name} {artist_name}"
        url = "https://itunes.apple.com/search"
        params = {"term": query, "media": "music", "limit": 1, "entity": "song"}
        r = requests.get(url, params=params, timeout=6)
        data = r.json()
        if data.get("resultCount", 0) > 0:
            art = data["results"][0].get("artworkUrl100", "")
            return art.replace("100x100bb", "600x600bb") if art else _default_music_img()
        return _default_music_img()
    except Exception:
        return _default_music_img()


@st.cache_data(show_spinner=False, ttl=3600)
def get_itunes_movie_artwork(movie_name: str) -> tuple[str, str]:
    """
    Fetch movie poster using a multi-strategy chain:
      1. iTunes Search API  (free, no key)
      2. poster.pics API    (free, no key, wide coverage)
      3. SVG data-URI fallback (always works, no external request)
    """
    director = ""

    # ── Strategy 1: iTunes ────────────────────────────────────────────────────
    try:
        r = requests.get(
            "https://itunes.apple.com/search",
            params={"term": movie_name, "media": "movie", "entity": "movie", "limit": 3},
            timeout=6,
        )
        data = r.json()
        if data.get("resultCount", 0) > 0:
            for item in data["results"]:
                raw = item.get("artworkUrl100", "") or item.get("artworkUrl60", "")
                if raw:
                    # Replace ANY size token (e.g. 100x100bb, 227x227bb) with high-res
                    art = re.sub(r"\d+x\d+bb", "600x900bb", raw)
                    director = item.get("artistName", "")
                    return art, director
    except Exception:
        pass

    # ── Strategy 2: poster.pics (open movie poster API, no key needed) ────────
    try:
        slug = requests.utils.quote(movie_name)
        r2 = requests.get(
            f"https://poster.pics/api/search?query={slug}&limit=1",
            timeout=5,
        )
        if r2.status_code == 200:
            d2 = r2.json()
            results = d2.get("results") or d2.get("data") or []
            if results:
                poster_url = results[0].get("poster") or results[0].get("image") or ""
                if poster_url:
                    return poster_url, director
    except Exception:
        pass

    # ── Strategy 3: OMDb (requires free API key — only used if key present) ──
    omdb_key = os.environ.get("OMDB_API_KEY", "")
    if omdb_key:
        try:
            r3 = requests.get(
                "http://www.omdbapi.com/",
                params={"t": movie_name, "apikey": omdb_key},
                timeout=5,
            )
            d3 = r3.json()
            poster = d3.get("Poster", "")
            if poster and poster != "N/A":
                director = d3.get("Director", director)
                return poster, director
        except Exception:
            pass

    # ── Fallback: inline SVG data-URI (always works, no network) ─────────────
    return _default_movie_img(), director


def _default_music_img() -> str:
    # Inline SVG — no external request, always renders
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400" viewBox="0 0 400 400">'
        '<rect width="400" height="400" fill="#EFEDE8"/>'
        '<text x="200" y="195" font-family="serif" font-size="64" fill="#C9B8A8" '
        'text-anchor="middle" dominant-baseline="middle">♪</text>'
        '<text x="200" y="265" font-family="sans-serif" font-size="13" fill="#B8B0A8" '
        'text-anchor="middle">No artwork found</text>'
        '</svg>'
    )
    import base64
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def _default_movie_img() -> str:
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="560" viewBox="0 0 400 560">'
        '<rect width="400" height="560" fill="#EFEDE8"/>'
        '<rect x="60" y="100" width="280" height="200" rx="8" fill="#E0DCD6"/>'
        '<circle cx="200" cy="200" r="48" fill="#D4CFC9"/>'
        '<polygon points="185,175 185,225 230,200" fill="#B8B0A8"/>'
        '<text x="200" y="360" font-family="sans-serif" font-size="13" fill="#B8B0A8" '
        'text-anchor="middle">Poster unavailable</text>'
        '</svg>'
    )
    import base64
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


# ─── Data Loading ────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def load_music_data():
    music_pkl = Path("df.pkl")
    sim_pkl   = Path("similarity.pkl")
    if not music_pkl.exists() or not sim_pkl.exists():
        return None, None
    music      = pickle.load(open(music_pkl, "rb"))
    similarity = pickle.load(open(sim_pkl, "rb"))
    return music, similarity


@st.cache_resource(show_spinner=False)
def load_movie_data():
    import difflib
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    movies_csv = Path("movies.csv")
    if not movies_csv.exists():
        return None, None, None

    df = pd.read_csv(movies_csv)
    selected_features = ["genres", "keywords", "tagline", "cast", "director"]
    for f in selected_features:
        df[f] = df[f].fillna("")
    combined = (
        df["genres"] + " " + df["keywords"] + " " +
        df["tagline"] + " " + df["cast"] + " " + df["director"]
    )
    vec     = TfidfVectorizer()
    matrix  = vec.fit_transform(combined)
    sim     = cosine_similarity(matrix)
    return df, sim, difflib


# ─── Recommendation Logic ────────────────────────────────────────────────────────

def recommend_music(song: str, music, similarity) -> list[dict]:
    idx       = music[music["song"] == song].index[0]
    distances = sorted(list(enumerate(similarity[idx])), reverse=True, key=lambda x: x[1])
    results   = []
    for i in distances[1:6]:
        row    = music.iloc[i[0]]
        artist = row.get("artist", "")
        art    = get_itunes_artwork(row["song"], artist)
        results.append({
            "title":  row["song"],
            "meta":   artist,
            "image":  art,
            "type":   "music",
        })
    return results


def recommend_movies(movie: str, df, sim, difflib) -> list[dict]:
    titles     = df["title"].tolist()
    close      = difflib.get_close_matches(movie, titles)
    if not close:
        return []
    match      = close[0]
    movie_idx  = df[df["title"] == match]["index"].values[0]
    scores     = sorted(list(enumerate(sim[movie_idx])), key=lambda x: x[1], reverse=True)
    results    = []
    for s in scores[1:6]:
        row         = df[df.index == s[0]]
        if row.empty:
            continue
        title       = row["title"].values[0]
        art, direct = get_itunes_movie_artwork(title)  # cached
        results.append({
            "title": title,
            "meta":  direct,
            "image": art,
            "type":  "movie",
        })
    return results


# ─── UI Components ───────────────────────────────────────────────────────────────

def render_nav(active_mode: str):
    st.markdown(f"""
    <div class="aurora-nav">
        <div class="aurora-logo">✦ Aurora<span>.</span></div>
        <div class="nav-tagline">Entertainment Discovery Platform</div>
        <div class="mode-badge {'mode-music' if active_mode == 'music' else 'mode-movie'}">
            {'♪ Music Mode' if active_mode == 'music' else '◉ Film Mode'}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_hero(mode: str):
    if mode == "music":
        title   = "Discover your next <em>favourite</em> song."
        sub     = "Our AI analyses lyrical DNA, genre markers, and mood vectors to surface music you'll genuinely love — not just what's popular."
        over    = "✦ Music Intelligence"
    else:
        title   = "Find films that <em>move</em> you."
        sub     = "Genre, cast, keywords, tone — our engine maps the hidden connective tissue between films to recommend your next obsession."
        over    = "◉ Cinematic Discovery"
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-overline">{over}</div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{sub}</p>
    </div>
    """, unsafe_allow_html=True)


def render_card(item: dict, rank: int):
    tag_cls = "tag-music" if item["type"] == "music" else "tag-movie"
    tag_lbl = "Music" if item["type"] == "music" else "Film"
    meta    = item["meta"] if item["meta"] else "—"
    st.markdown(f"""
    <div class="rec-card">
        <div class="card-image-wrap">
            <img src="{item['image']}" alt="{item['title']}" loading="lazy" />
            <div class="card-rank">0{rank}</div>
        </div>
        <div class="card-body">
            <div class="card-title" title="{item['title']}">{item['title']}</div>
            <div class="card-meta">{meta}</div>
            <span class="card-tag {tag_cls}">{tag_lbl}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_results_header(label: str):
    st.markdown(f"""
    <div class="section-header">
        <span class="section-label">{label}</span>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)


def render_stats(music, movies):
    music_count = len(music) if music is not None else 0
    movie_count = len(movies) if movies is not None else 0
    st.markdown(f"""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number">{music_count:,}</div>
            <div class="stat-desc">Songs indexed</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">{movie_count:,}</div>
            <div class="stat-desc">Films catalogued</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">5</div>
            <div class="stat-desc">Recommendations per query</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">iTunes</div>
            <div class="stat-desc">Artwork source</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="aurora-footer">
        <div class="footer-logo">✦ Aurora</div>
        <div class="footer-note">Powered by TF-IDF · Cosine Similarity · iTunes API</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Main App ────────────────────────────────────────────────────────────────────

def main():
    # Mode toggle via sidebar state (mapped to radio in session)
    if "mode" not in st.session_state:
        st.session_state.mode = "music"
    if "results" not in st.session_state:
        st.session_state.results = []
    if "query" not in st.session_state:
        st.session_state.query = ""

    # Load data
    music_df, music_sim   = load_music_data()
    movie_df, movie_sim, difflib_mod = load_movie_data()

    # ── Nav ──
    render_nav(st.session_state.mode)

    # ── Mode Switcher ──
    st.markdown("<div style='padding: 20px 56px 0; max-width:1400px; margin:0 auto;'>", unsafe_allow_html=True)
    col_toggle, col_spacer = st.columns([3, 7])
    with col_toggle:
        mode = st.radio(
            "Mode",
            options=["🎵 Music", "🎬 Films"],
            horizontal=True,
            label_visibility="collapsed",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    new_mode = "music" if "Music" in mode else "movie"
    if new_mode != st.session_state.mode:
        st.session_state.mode = new_mode
        st.session_state.results = []
        st.session_state.query = ""
        st.rerun()

    active = st.session_state.mode

    # ── Hero ──
    render_hero(active)

    # ── Stats Bar ──
    render_stats(music_df, movie_df)

    # ── Search Area ──
    st.markdown("<div style='padding: 0 56px; max-width:1400px; margin:0 auto;'>", unsafe_allow_html=True)

    if active == "music":
        if music_df is None:
            st.warning("⚠ Place `df.pkl` and `similarity.pkl` in the project root, then restart.")
        else:
            st.markdown('<div class="search-label">Choose a song you love</div>', unsafe_allow_html=True)
            song_list = music_df["song"].values.tolist()
            selected = st.selectbox("Song", song_list, label_visibility="collapsed")
            if st.button("✦ Discover Similar Songs", use_container_width=False):
                with st.spinner("Analysing sonic fingerprints…"):
                    st.session_state.results = recommend_music(selected, music_df, music_sim)
                    st.session_state.query   = selected
    else:
        if movie_df is None:
            st.warning("⚠ Place `movies.csv` in the project root, then restart.")
        else:
            st.markdown('<div class="search-label">Enter a film you admire</div>', unsafe_allow_html=True)
            movie_input = st.text_input("Movie", placeholder="e.g. Interstellar", label_visibility="collapsed")
            if st.button("◉ Discover Similar Films", use_container_width=False):
                if movie_input.strip():
                    with st.spinner("Mapping cinematic connections…"):
                        st.session_state.results = recommend_movies(
                            movie_input.strip(), movie_df, movie_sim, difflib_mod
                        )
                        st.session_state.query   = movie_input.strip()
                else:
                    st.info("Please enter a film title to begin.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Results ──
    if st.session_state.results:
        label = f"✦ Because you like '{st.session_state.query}'"
        render_results_header(label)
        st.markdown('<div class="recs-grid">', unsafe_allow_html=True)
        cols = st.columns(5, gap="small")
        for i, item in enumerate(st.session_state.results):
            with cols[i]:
                render_card(item, i + 1)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="padding: 0 56px 64px; max-width: 1400px; margin: 0 auto;">
            <div style="display:grid; grid-template-columns: repeat(5,1fr); gap: 20px;">
                <div class="card-placeholder"><div class="placeholder-icon">✦</div><div class="placeholder-text">Awaiting your selection</div></div>
                <div class="card-placeholder"><div class="placeholder-icon">✦</div><div class="placeholder-text">Awaiting your selection</div></div>
                <div class="card-placeholder"><div class="placeholder-icon">✦</div><div class="placeholder-text">Awaiting your selection</div></div>
                <div class="card-placeholder"><div class="placeholder-icon">✦</div><div class="placeholder-text">Awaiting your selection</div></div>
                <div class="card-placeholder"><div class="placeholder-icon">✦</div><div class="placeholder-text">Awaiting your selection</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Footer ──
    render_footer()


if __name__ == "__main__":
    main()
