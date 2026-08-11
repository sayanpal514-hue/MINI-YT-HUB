# MINI YT HUB

MINI YT HUB is a premium, beautifully designed movie and video scrapper platform. It automatically scrapes various categories (like Anime, Cartoons, Bengali,Hindi, Hollywood, etc.) from official YouTube channels and presents them in a modern, dark-themed user interface.

## 📸 Interface Preview

![Website Screenshot](./Screenshot.png)



## ✨ Features

* **Premium UI**: Stunning dark mode with glassmorphism effects.
* **Auto-Scraping**: `yt-dlp` powered Python script to scrape videos by categories and channels.
* **Rich Filtering**: Filter dynamically by multiple categories (Cartoons, Anime, Hollywood, Bengali, etc.).
* **Smart Search**: Search instantly by video title, uploader, or category.
* **Dedicated Player**: Integrated video player page with side recommendations.

## 🚀 How to Run

1. **Scrape Data (Optional - Data is included)**:
   ```bash
   cd scrapper
   pip install -r requirements.txt
   python main.py
   ```


2. **Run the Website**:
   Due to CORS policies, you need to run a local web server to fetch the JSON data.
   ```bash
   # From the root directory (where index.html is located)
   python -m http.server 8000
   ```
   Then open `http://localhost:8000/index.html` in your browser.

## 🛠️ Built With

* **Frontend**: HTML5, CSS3 (Vanilla), JavaScript
* **Backend Scraper**: Python, `yt-dlp`
