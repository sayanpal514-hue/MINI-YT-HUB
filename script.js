// State
let allMovies = [];
let filteredMovies = [];
let currentCategory = 'all';

// DOM Elements
const movieGrid = document.getElementById('movieGrid');
const searchInput = document.getElementById('searchInput');
const categoryContainer = document.getElementById('categoryContainer');
const loader = document.getElementById('loader');

// Utilities
const formatViews = (views) => {
    if (views >= 1000000) return (views / 1000000).toFixed(1) + 'M views';
    if (views >= 1000) return (views / 1000).toFixed(1) + 'K views';
    return views + ' views';
};

const formatDuration = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m}:${s.toString().padStart(2, '0')}`;
};

const jsonFiles = [
    './movies/movies.json',
    './movies/anime/anione_in/anione_in.json',
    './movies/anime/muse_india/muse_india.json',
    './movies/anime/muse_asia/muse_asia.json',
    './movies/anime/anione_asia/anione_asia.json',
    './movies/anime/gundaminfo/gundaminfo.json',
    './movies/anime/animelog/animelog.json',
    './movies/bengali/bengali.json',
    './movies/cartoons/cartoons.json',
    './movies/cartoons/bandbudh_aur_budbak/bandbudh_aur_budbak.json',
    './movies/cartoons/bapu/bapu.json',
    './movies/cartoons/bas_karo_henry/bas_karo_henry.json',
    './movies/cartoons/ben_10/ben_10.json',
    './movies/cartoons/chacha_bhatija/chacha_bhatija.json',
    './movies/cartoons/chhota_bheem/chhota_bheem.json',
    './movies/cartoons/doraemon/doraemon.json',
    './movies/cartoons/eena_meena_deeka/eena_meena_deeka.json',
    './movies/cartoons/fukrey_boyzzz/fukrey_boyzzz.json',
    './movies/cartoons/gattu_battu/gattu_battu.json',
    './movies/cartoons/golmaal_jr/golmaal_jr.json',
    './movies/cartoons/guru_aur_bhole/guru_aur_bhole.json',
    './movies/cartoons/honey_bunny_ka_jholmaal/honey_bunny_ka_jholmaal.json',
    './movies/cartoons/inspector_chingum/inspector_chingum.json',
    './movies/cartoons/keymon_ache/keymon_ache.json',
    './movies/cartoons/kris_ki_school_journey/kris_ki_school_journey.json',
    './movies/cartoons/little_singham/little_singham.json',
    './movies/cartoons/masha_and_the_bear/masha_and_the_bear.json',
    './movies/cartoons/mighty_raju/mighty_raju.json',
    './movies/cartoons/motu_patlu/motu_patlu.json',
    './movies/cartoons/motu_patlu_vs_robots/motu_patlu_vs_robots.json',
    './movies/cartoons/mr_bean/mr_bean.json',
    './movies/cartoons/ninja_hattori/ninja_hattori.json',
    './movies/cartoons/oggy_and_the_cockroaches/oggy_and_the_cockroaches.json',
    './movies/cartoons/pakdam_pakdai/pakdam_pakdai.json',
    './movies/cartoons/peppa_pig/peppa_pig.json',
    './movies/cartoons/pokemon/pokemon.json',
    './movies/cartoons/roll_no_21/roll_no_21.json',
    './movies/cartoons/rudra/rudra.json',
    './movies/cartoons/shinchan/shinchan.json',
    './movies/cartoons/shiva/shiva.json',
    './movies/cartoons/super_bheem/super_bheem.json',
    './movies/cartoons/tik_tak_tail/tik_tak_tail.json',
    './movies/cartoons/tom_and_jerry/tom_and_jerry.json',
    './movies/cartoons/vir_the_robot_boy/vir_the_robot_boy.json',
    './movies/cartoons/zig_and_sharko/zig_and_sharko.json',
    './movies/comedy/comedy.json',
    './movies/english/english.json',
    './movies/hindi/hindi.json',
    './movies/hollywood/hollywood.json',
    './movies/kannada/kannada.json',
    './movies/marathi/marathi.json',
    './movies/other/other.json',
    './movies/taarak_mehta/taarak_mehta.json',
    './movies/tamil/tamil.json',
    './movies/telugu/telugu.json',
    './movies/yam_hain_hum/yam_hain_hum.json'
];

const fetchMovies = async () => {
    try {
        if(movieGrid) movieGrid.style.display = 'none';
        if(loader) loader.style.display = 'flex';
        
        let fetchedMovies = [];
        const seenIds = new Set();
        
        // Fetch all files in parallel
        const responses = await Promise.allSettled(
            jsonFiles.map(url => fetch(url).then(res => res.json()))
        );
        
        responses.forEach(result => {
            if (result.status === 'fulfilled') {
                const data = result.value;
                // Some files use 'movies', some use 'episodes'
                let items = [];
                if (data.movies) items = data.movies;
                else if (data.episodes) items = data.episodes;
                
                // Add default category if missing
                const defaultCat = data.category || 'other';
                
                items.forEach(item => {
                    if (!seenIds.has(item.id)) {
                        seenIds.add(item.id);
                        item.category = item.category || defaultCat;
                        item.uploader = item.uploader || 'Unknown';
                        item.view_count = item.view_count || 0;
                        item.duration = item.duration || 0;
                        fetchedMovies.push(item);
                    }
                });
            }
        });
        
        allMovies = fetchedMovies;
        filteredMovies = [...allMovies];
        
        if (movieGrid) {
            setupCategories();
            renderMovies();
        }
        
        // For player page
        if (document.getElementById('videoPlayer')) {
            setupPlayer();
        }
    } catch (error) {
        console.error('Error fetching movies:', error);
        if (movieGrid) {
            movieGrid.innerHTML = '<div style="color: #ff2a5f; text-align:center; width:100%; grid-column: 1/-1;">Failed to load movies.</div>';
        }
    } finally {
        if(loader) loader.style.display = 'none';
        if(movieGrid) movieGrid.style.display = 'grid';
    }
};

// Render Movies
const renderMovies = () => {
    if (!movieGrid) return;
    
    movieGrid.innerHTML = '';
    
    if (filteredMovies.length === 0) {
        movieGrid.innerHTML = '<div style="color: var(--text-secondary); text-align:center; width:100%; grid-column: 1/-1; padding: 2rem;">No movies found.</div>';
        return;
    }
    
    // Render only first 100 to avoid performance issues if JSON is huge, but here let's render up to 200
    const moviesToRender = filteredMovies.slice(0, 200);
    
    moviesToRender.forEach(movie => {
        const card = document.createElement('a');
        card.className = 'movie-card';
        card.href = `player.html?id=${movie.id}`;
        
        card.innerHTML = `
            <div class="thumbnail-wrapper">
                <img src="${movie.thumbnail || `https://img.youtube.com/vi/${movie.id}/maxresdefault.jpg`}" alt="${movie.title}" class="movie-thumb" loading="lazy">
                <span class="duration-badge">${formatDuration(movie.duration)}</span>
            </div>
            <div class="movie-info">
                <h3 class="movie-title">${movie.title}</h3>
                <div class="movie-meta">
                    <span class="movie-uploader">${movie.uploader}</span>
                    <span class="movie-views">${formatViews(movie.view_count)}</span>
                </div>
            </div>
        `;
        
        movieGrid.appendChild(card);
    });
};

// Categories Setup
const setupCategories = () => {
    if (!categoryContainer) return;
    
    // Extract unique categories
    const categories = new Set(allMovies.map(m => m.category).filter(Boolean));
    
    let html = `<button class="category-btn active" data-category="all">All</button>`;
    
    categories.forEach(cat => {
        const displayCat = cat.charAt(0).toUpperCase() + cat.slice(1).replace(/_/g, ' ');
        html += `<button class="category-btn" data-category="${cat}">${displayCat}</button>`;
    });
    
    categoryContainer.innerHTML = html;
    
    // Add Event Listeners
    categoryContainer.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Update active class
            categoryContainer.querySelectorAll('.category-btn').forEach(b => b.classList.remove('active'));
            e.target.classList.add('active');
            
            currentCategory = e.target.dataset.category;
            filterMovies();
        });
    });
};

// Filter logic
const filterMovies = () => {
    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    
    filteredMovies = allMovies.filter(movie => {
        const matchesSearch = movie.title.toLowerCase().includes(searchTerm) || 
                              movie.uploader.toLowerCase().includes(searchTerm) ||
                              movie.category.toLowerCase().includes(searchTerm);
        const matchesCategory = currentCategory === 'all' || movie.category === currentCategory;
        
        return matchesSearch && matchesCategory;
    });
    
    renderMovies();
};

if (searchInput) {
    searchInput.addEventListener('input', filterMovies);
}


// Player Logic
const setupPlayer = () => {
    const urlParams = new URLSearchParams(window.location.search);
    const videoId = urlParams.get('id');
    
    if (!videoId) {
        document.querySelector('.player-container').innerHTML = '<h2>Video not found</h2>';
        return;
    }
    
    const movie = allMovies.find(m => m.id === videoId);
    
    if (movie) {
        // Set document title
        document.title = `${movie.title} - MINI HUB`;
        
        // Setup Player
        document.getElementById('videoPlayer').src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
        document.getElementById('videoTitle').textContent = movie.title;
        document.getElementById('videoViews').textContent = formatViews(movie.view_count);
        document.getElementById('videoDate').textContent = movie.category.charAt(0).toUpperCase() + movie.category.slice(1);
        document.getElementById('uploaderInitial').textContent = movie.uploader.charAt(0).toUpperCase();
        document.getElementById('uploaderName').textContent = movie.uploader;
        
        // Setup Recommendations
        const recContainer = document.getElementById('recommendationsList');
        recContainer.innerHTML = '';
        
        // Get related movies (same category, exclude current)
        let related = allMovies.filter(m => m.category === movie.category && m.id !== videoId);
        
        // If not enough related, just add random ones
        if (related.length < 10) {
            related = [...related, ...allMovies.filter(m => m.category !== movie.category && m.id !== videoId)].slice(0, 15);
        } else {
            related = related.slice(0, 15);
        }
        
        related.forEach(rec => {
            const el = document.createElement('a');
            el.className = 'rec-card';
            el.href = `player.html?id=${rec.id}`;
            el.innerHTML = `
                <img src="${rec.thumbnail}" class="rec-thumb" alt="thumbnail">
                <div class="rec-info">
                    <div class="rec-title">${rec.title}</div>
                    <div class="rec-meta">${rec.uploader} • ${formatViews(rec.view_count)}</div>
                </div>
            `;
            recContainer.appendChild(el);
        });
    }
};


// Initialize
document.addEventListener('DOMContentLoaded', fetchMovies);
