# MINI YT HUB
MINI YT HUB is a premium, beautifully designed movie and video scrapper platform. It automatically scrapes various categories (like Anime, Cartoons, Bengali, Hindi, Hollywood, etc.) from official YouTube channels and presents them in a modern, dark-themed user interface.

🔗 **Live Demo**: [https://sayanpal514-hue.github.io/MINI-YT-HUB/](https://sayanpal514-hue.github.io/MINI-YT-HUB/)
## 📸 Interface Preview
![Website Screenshot](./Screenshot.png)

## ✨ Features
* **Premium UI**: Stunning dark mode with glassmorphism effects.
* **Auto-Scraping**: `yt-dlp` powered Python script, run automatically every 20 minutes via GitHub Actions, to scrape videos by categories and channels.
* **Rich Filtering**: Filter dynamically by multiple categories (Cartoons, Anime, Hollywood, Bengali, South Indian, etc.).
* **Smart Search**: Search instantly by video title, uploader, or category.
* **Dedicated Player**: Integrated video player page with side recommendations.
* 
## 🚀 How to Run

1. **Scrape Data (Optional - Data is included and refreshed automatically)**:
   ```bash
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
* **Automation & Hosting**: GitHub Actions (scheduled scraping), GitHub Pages (deployment)
* 
## ⚠️ Disclaimer
This project is created **strictly for educational purposes only**. It is intended to demonstrate web scraping techniques, front-end development, and video data presentation. All video content displayed is sourced from and linked back to official YouTube channels — no video files are hosted, downloaded, or redistributed by this project.
The developer(s) of MINI YT HUB do not own, claim ownership of, or take responsibility for any third-party content displayed through this application. All trademarks, video content, and channel names belong to their respective owners. Users are responsible for ensuring their use of this software complies with YouTube's Terms of Service and applicable copyright laws in their jurisdiction.
This project is **not affiliated with, endorsed by, or sponsored by YouTube or Google LLC**.

## 📄 License
This project is licensed under the **MIT License**.

See the [LICENSE](./LICENSE) file for full details.
