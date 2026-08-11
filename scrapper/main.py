import yt_dlp
import json
import os
import time
import re
from datetime import datetime

# ──────────────────────────────────────────────────────────────
# 1. CATEGORIES (search‑based)
# ──────────────────────────────────────────────────────────────

CATEGORIES = {
    "hindi": "full movie hindi",
    "marathi": "full movie marathi",
    "english": "full movie english",
    "tamil": "full movie tamil",
    "telugu": "full movie telugu",
    "kannada": "full movie kannada",
    "bengali": "full movie bengali",          
    "hollywood": "hollywood full movie",      
    "other": "full movie",                    
    "cartoons": "cartoon full movie for kids",
    "cartoons_auto": "hindi cartoon full episodes",
    "comedy": "hindi comedy videos",
    "taarak_mehta": "taarak mehta ka ooltah chashmah",
    "yam_hain_hum": "yam hain hum",
}

# ──────────────────────────────────────────────────────────────
# 2. CARTOON SUB‑CATEGORIES (subfolders)
# ──────────────────────────────────────────────────────────────

CARTOON_CATEGORIES = {
    "cartoons/oggy_and_the_cockroaches": "oggy and the cockroaches hindi full episodes",
    "cartoons/bandbudh_aur_budbak": "bandbudh aur budbak hindi full episodes",
    "cartoons/chhota_bheem": "chhota bheem hindi full episodes",
    "cartoons/motu_patlu": "motu patlu hindi full episodes",
    "cartoons/gattu_battu": "gattu battu hindi full episodes",
    "cartoons/doraemon": "doraemon hindi full episodes",
    "cartoons/ninja_hattori": "ninja hattori hindi full episodes",
    "cartoons/chacha_bhatija": "chacha bhatija hindi full episodes",
    "cartoons/shinchan": "shinchan hindi full episodes",
    "cartoons/pokemon": "pokemon hindi full episodes",
    "cartoons/roll_no_21": "roll no 21 hindi full episodes",
    "cartoons/little_singham": "little singham hindi full episodes",
    "cartoons/shiva": "shiva cartoon hindi full episodes",
    "cartoons/rudra": "rudra boom chik chik boom hindi full episodes",
    "cartoons/vir_the_robot_boy": "vir the robot boy hindi full episodes",
    "cartoons/pakdam_pakdai": "pakdam pakdai hindi full episodes",
    "cartoons/mighty_raju": "mighty raju hindi full episodes",
    "cartoons/honey_bunny_ka_jholmaal": "honey bunny ka jholmaal hindi full episodes",
    "cartoons/guru_aur_bhole": "guru aur bhole hindi full episodes",
    "cartoons/eena_meena_deeka": "eena meena deeka hindi full episodes",
    "cartoons/inspector_chingum": "inspector chingum hindi full episodes",
    "cartoons/fukrey_boyzzz": "fukrey boyzzz hindi full episodes",
    "cartoons/golmaal_jr": "golmaal jr hindi full episodes",
    "cartoons/masha_and_the_bear": "masha and the bear hindi full episodes",
    "cartoons/peppa_pig": "peppa pig hindi full episodes",
    "cartoons/tom_and_jerry": "tom and jerry hindi full episodes",
    "cartoons/ben_10": "ben 10 hindi full episodes",
    "cartoons/mr_bean": "mr bean cartoon hindi full episodes",
    "cartoons/zig_and_sharko": "zig and sharko hindi full episodes",
    "cartoons/bapu": "bapu cartoon hindi full episodes",
    "cartoons/tik_tak_tail": "tik tak tail hindi full episodes",
    "cartoons/keymon_ache": "keymon ache hindi full episodes",
    "cartoons/super_bheem": "super bheem hindi full episodes"
}

# ──────────────────────────────────────────────────────────────
# 3. ANIME CHANNELS (direct scraping)
# ──────────────────────────────────────────────────────────────

ANIME_CHANNELS = {
    "anime/muse_india": "https://www.youtube.com/@MuseIndiaChannel/videos",
    "anime/anione_in": "https://www.youtube.com/@AniOneIN/videos",
    "anime/muse_asia": "https://www.youtube.com/@MuseAsia/videos",
    "anime/anione_asia": "https://www.youtube.com/@AniOneAsia/videos",
    "anime/gundaminfo": "https://www.youtube.com/@GundamInfo/videos",
    "anime/animelog": "https://www.youtube.com/@AnimeLogGlobal/videos"
}

# ──────────────────────────────────────────────────────────────
# 4. MOVIE CHANNELS (direct scraping) - each key can hold a list
# ──────────────────────────────────────────────────────────────

MOVIE_CHANNELS = {
    "bengali": [
        "https://www.youtube.com/@BengaliMoviesAngelDigital/videos",
        "https://www.youtube.com/channel/UCBdN0UL0aN2S6tvm41J50wQ",  # Uttam Kumar Movies
        "https://www.youtube.com/@svf/videos",                       # SVF
        "https://www.youtube.com/@Surinderfilms/videos",             # Surinder Films
        "https://www.youtube.com/@EskayMovies/videos"                # Eskay Movies
    ],
    "hollywood": [
        "https://www.youtube.com/channel/UCGBzBkV-MinlBvHBzZawfLQ",  # Movie Central
        "https://www.youtube.com/channel/UCE6OXVqLfsLvnlu5l0CkMsA",  # Best Hollywood Movies
        "https://www.youtube.com/channel/UCrKhoJu5EeWXBK5jpEj6uvw",  # Hollywood Movies
        "https://www.youtube.com/@Popcornflix/videos",               # Popcornflix
        "https://www.youtube.com/@SciFiCentral/videos"               # Sci-Fi Central
    ],
}

# ──────────────────────────────────────────────────────────────
# 5. MERGE ALL SEARCH CATEGORIES
# ──────────────────────────────────────────────────────────────

ALL_CATEGORIES = {**CATEGORIES, **CARTOON_CATEGORIES}

# ──────────────────────────────────────────────────────────────
# 6. CONFIGURATION
# ──────────────────────────────────────────────────────────────

RESULTS_PER_CATEGORY = 20          # for search‑based categories
OUTPUT_DIR = "movies"

# ──────────────────────────────────────────────────────────────
# 7. HELPER: EXTRACT CARTOON NAME FROM TITLE
# ──────────────────────────────────────────────────────────────

def extract_cartoon_name_and_category(title):
    """Extract cartoon name from video title."""
    delimiters = r'[|\-:]'
    parts = re.split(delimiters, title)
    
    if parts:
        name = parts[0].strip()
        name = re.sub(r'(?i)\b(hindi|full episode|cartoon|episodes|kids|in hindi|new episode|latest)\b', '', name).strip()
        name = re.sub(r'^[^a-zA-Z0-9]+', '', name)
        name = re.sub(r'[^a-zA-Z0-9]+$', '', name)
        name = name.strip()
        
        if 2 < len(name) < 40:
            sanitized = re.sub(r'[^a-zA-Z0-9]+', '_', name.lower()).strip('_')
            return name, f"cartoons/{sanitized}"
            
    return "Various Cartoons", "cartoons/various_cartoons"

# ──────────────────────────────────────────────────────────────
# 8. CHANNEL SCRAPER (reusable)
# ──────────────────────────────────────────────────────────────

def scrape_channel_videos(channel_url, category, max_results=30):
    """
    Fetch recent videos from a YouTube channel URL.
    Returns a list of video dicts with the same structure as search results.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
    }
    videos = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(channel_url, download=False)
            if 'entries' in info:
                for video in info['entries'][:max_results]:
                    if not video:
                        continue
                    duration = video.get('duration', 0)
                    # Skip very short clips (shorts / trailers) – adjust as needed
                    if duration and duration < 300:   # 5 minutes minimum for episodes/movies
                        continue
                    videos.append({
                        "id": video.get('id'),
                        "title": video.get('title'),
                        "url": video.get('url'),
                        "duration": duration,
                        "view_count": video.get('view_count'),
                        "uploader": video.get('uploader'),
                        "category": category,
                        "thumbnail": video.get('thumbnails', [{}])[-1].get('url', '') if video.get('thumbnails') else None,
                        "channel": video.get('uploader'),   # extra field, optional
                    })
                    time.sleep(0.5)  # be gentle
        except Exception as e:
            print(f"Error scraping channel {category} ({channel_url}): {e}")
    return videos

# ──────────────────────────────────────────────────────────────
# 9. MAIN SCRAPER (search + channels)
# ──────────────────────────────────────────────────────────────

def scrape_movies():
    """Scrape movies from YouTube and return them grouped by category."""
    all_movies = []

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # ── A. Search‑based categories ──
        for category, query in ALL_CATEGORIES.items():
            # Skip anime categories because we handle them via channel scraping
            if category.startswith("anime/"):
                continue

            print(f"Searching for {category}...")
            search_query = f"ytsearch{RESULTS_PER_CATEGORY}:{query}"

            try:
                result = ydl.extract_info(search_query, download=False)
                if 'entries' in result:
                    for video in result['entries']:
                        if not video:
                            continue

                        duration = video.get('duration', 0)
                        # Determine minimum duration based on category type
                        short_categories = ["cartoons", "comedy", "taarak_mehta", "yam_hain_hum"]
                        is_short = category in short_categories or category.startswith("cartoons/")
                        min_duration = 600 if is_short else 2400   # 10 min vs 40 min
                        if duration and duration < min_duration:
                            continue

                        movie_data = {
                            "id": video.get('id'),
                            "title": video.get('title'),
                            "url": video.get('url'),
                            "duration": duration,
                            "view_count": video.get('view_count'),
                            "uploader": video.get('uploader'),
                            "category": category,
                            "thumbnail": video.get('thumbnails', [{}])[-1].get('url', '') if video.get('thumbnails') else None
                        }

                        if movie_data['id'] and movie_data['title']:
                            # Auto‑detect cartoon name if category is cartoons_auto
                            if category == "cartoons_auto":
                                detected_name, new_category = extract_cartoon_name_and_category(movie_data['title'])
                                movie_data['category'] = new_category
                                movie_data['show_name'] = detected_name

                            all_movies.append(movie_data)
                            print(f"[{time.strftime('%X')}] Added movie: {movie_data['title']}")
                            time.sleep(1)   # delay between search results

            except Exception as e:
                print(f"Error scraping category {category}: {e}")

        # ── B. Anime channels ──
        for category, channel_url in ANIME_CHANNELS.items():
            print(f"Fetching videos from {category}...")
            videos = scrape_channel_videos(channel_url, category, max_results=30)
            all_movies.extend(videos)
            print(f"  Added {len(videos)} videos from {category}")

        # ── C. Movie channels (now each category can have multiple URLs) ──
        for category, channel_urls in MOVIE_CHANNELS.items():
            # Ensure we always iterate over a list
            if not isinstance(channel_urls, list):
                channel_urls = [channel_urls]
            for url in channel_urls:
                print(f"Fetching movies from {category} channel: {url}...")
                videos = scrape_channel_videos(url, category, max_results=30)
                all_movies.extend(videos)
                print(f"  Added {len(videos)} movies from {category} channel")

    # Remove duplicates based on video ID
    unique_movies = {movie['id']: movie for movie in all_movies}.values()
    return list(unique_movies)

# ──────────────────────────────────────────────────────────────
# 10. LOAD / SAVE HELPERS
# ──────────────────────────────────────────────────────────────

def load_existing(filepath):
    """Load existing movies from a JSON file."""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                movies = existing_data.get('episodes', existing_data.get('movies', []))
                print(f"  Loaded {len(movies)} existing movies from {filepath}")
                return movies
        except Exception as e:
            print(f"  Could not read existing file {filepath}: {e}")
    return []

def save_json(movies_list, filepath, show_name=None, is_cartoon=False):
    """Save a list of movies to a JSON file with metadata."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if is_cartoon:
        output = {
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "show_name": show_name or "Unknown Cartoon",
            "language": "Hindi",
            "category": "cartoons",
            "description": f"Auto-generated category for {show_name or 'videos'}.",
            "total_episodes": len(movies_list),
            "episodes": movies_list
        }
    else:
        output = {
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "total_movies": len(movies_list),
            "movies": movies_list
        }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    print(f"  Saved {len(movies_list)} items to {filepath}")

# ──────────────────────────────────────────────────────────────
# 11. SAVE ALL (per‑category + combined)
# ──────────────────────────────────────────────────────────────

def save_all(new_movies):
    """Save movies per‑category into folders AND into a combined file."""

    # ── Group new movies by category ──
    by_category = {}
    for movie in new_movies:
        cat = movie.get('category', 'uncategorized')
        by_category.setdefault(cat, []).append(movie)

    # ── Collect all category keys (search + channels) ──
    all_cat_keys = (
        set(ALL_CATEGORIES.keys())
        | set(by_category.keys())
        | set(ANIME_CHANNELS.keys())
        | set(MOVIE_CHANNELS.keys())
    )

    # ── Save per‑category files ──
    for cat in all_cat_keys:
        if cat == "cartoons_auto":
            continue

        cat_dir = os.path.join(OUTPUT_DIR, cat)
        cat_basename = cat.split("/")[-1]
        cat_file = os.path.join(cat_dir, f"{cat_basename}.json")

        existing = load_existing(cat_file)
        combined = existing + by_category.get(cat, [])
        unique = list({m['id']: m for m in combined}.values())

        print(f"[{cat}] {len(unique)} total movies")

        is_cartoon = cat.startswith("cartoons/") or cat.startswith("anime/")
        show_name = cat_basename.replace('_', ' ').title()
        if unique and 'show_name' in unique[0]:
            show_name = unique[0]['show_name']

        save_json(unique, cat_file, show_name=show_name, is_cartoon=is_cartoon)

    # ── Save combined file ──
    combined_file = os.path.join(OUTPUT_DIR, "movies.json")
    existing_all = load_existing(combined_file)
    combined_all = existing_all + new_movies
    unique_all = list({m['id']: m for m in combined_all}.values())

    print(f"[all] {len(unique_all)} total movies")
    save_json(unique_all, combined_file)

# ──────────────────────────────────────────────────────────────
# 12. ENTRY POINT
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Starting YouTube movie discovery at {datetime.now()}...")
    movies = scrape_movies()
    save_all(movies)
    print("Done!")
