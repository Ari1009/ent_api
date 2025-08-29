from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
import logging
import asyncio
from typing import Optional, Dict, Any
from functools import lru_cache
import time

from MoviesApi import HomeMoviesApi
from gogoanime import search_anime, gogo_play, bsoup, base_url
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI with metadata
app = FastAPI(
    title="Movies & Anime API",
    description="A comprehensive API for movies, TV shows, and anime content",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8080",
    "https://your-frontend-domain.com",
    "*"  # Remove in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Simple in-memory cache
cache = {}
CACHE_TTL = 300  # 5 minutes

def get_cached_data(key: str) -> Optional[Dict[Any, Any]]:
    """Get data from cache if not expired"""
    if key in cache:
        data, timestamp = cache[key]
        if time.time() - timestamp < CACHE_TTL:
            return data
        else:
            del cache[key]
    return None

def set_cache_data(key: str, data: Dict[Any, Any]) -> None:
    """Set data in cache with timestamp"""
    cache[key] = (data, time.time())

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


@app.get('/')
async def root():
    """API health check and information"""
    return {
        "message": "Movies & Anime API v2.0",
        "status": "healthy",
        "endpoints": {
            "docs": "/docs",
            "movies": "/api/movies/{page}",
            "tv_shows": "/api/tv-shows/{page}",
            "anime_search": "/search?name={anime_name}"
        }
    }

@app.get('/api/movies/{page}')
async def get_movies(page: int = Query(..., ge=1, description="Page number (minimum 1)")):
    """Get paginated movies list with caching"""
    try:
        cache_key = f"movies_page_{page}"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for movies page {page}")
            return {"data": cached_data, "cached": True}
        
        logger.info(f"Fetching movies page {page}")
        movies_data = HomeMoviesApi.Movies(page)
        
        if not movies_data:
            raise HTTPException(status_code=404, detail="No movies found for this page")
        
        set_cache_data(cache_key, movies_data)
        return {"data": movies_data, "cached": False, "page": page}
        
    except Exception as e:
        logger.error(f"Error fetching movies page {page}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch movies: {str(e)}")

@app.get('/api/tv-shows/{page}')
async def get_tv_shows(page: int = Query(..., ge=1, description="Page number (minimum 1)")):
    """Get paginated TV shows list with caching"""
    try:
        cache_key = f"tv_shows_page_{page}"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for TV shows page {page}")
            return {"data": cached_data, "cached": True}
        
        logger.info(f"Fetching TV shows page {page}")
        tv_data = HomeMoviesApi.TV(page)
        
        if not tv_data:
            raise HTTPException(status_code=404, detail="No TV shows found for this page")
        
        set_cache_data(cache_key, tv_data)
        return {"data": tv_data, "cached": False, "page": page}
        
    except Exception as e:
        logger.error(f"Error fetching TV shows page {page}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch TV shows: {str(e)}")

@app.get('/api/top-imdb/movies/{page}')
async def get_top_imdb_movies(page: int = Query(..., ge=1, description="Page number (minimum 1)")):
    """Get top IMDB rated movies with caching"""
    try:
        cache_key = f"top_imdb_movies_page_{page}"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for top IMDB movies page {page}")
            return {"data": cached_data, "cached": True}
        
        logger.info(f"Fetching top IMDB movies page {page}")
        imdb_movies = HomeMoviesApi.TOPIMDBMOVIES(page)
        
        if not imdb_movies:
            raise HTTPException(status_code=404, detail="No top IMDB movies found for this page")
        
        set_cache_data(cache_key, imdb_movies)
        return {"data": imdb_movies, "cached": False, "page": page}
        
    except Exception as e:
        logger.error(f"Error fetching top IMDB movies page {page}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch top IMDB movies: {str(e)}")

@app.get('/api/top-imdb/tv-shows/{page}')
async def get_top_imdb_tv(page: int = Query(..., ge=1, description="Page number (minimum 1)")):
    """Get top IMDB rated TV shows with caching"""
    try:
        cache_key = f"top_imdb_tv_page_{page}"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for top IMDB TV shows page {page}")
            return {"data": cached_data, "cached": True}
        
        logger.info(f"Fetching top IMDB TV shows page {page}")
        imdb_tv = HomeMoviesApi.TOPIMDBTV(page)
        
        if not imdb_tv:
            raise HTTPException(status_code=404, detail="No top IMDB TV shows found for this page")
        
        set_cache_data(cache_key, imdb_tv)
        return {"data": imdb_tv, "cached": False, "page": page}
        
    except Exception as e:
        logger.error(f"Error fetching top IMDB TV shows page {page}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch top IMDB TV shows: {str(e)}")



@app.get('/api/trending_movies')
async def get_trending_movies():
    """Get trending movies with caching"""
    try:
        cache_key = "trending_movies"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info("Cache hit for trending movies")
            return {"data": cached_data, "cached": True}
        
        logger.info("Fetching trending movies")
        trending_data = HomeMoviesApi.trendingMovies(None)
        
        if not trending_data:
            raise HTTPException(status_code=404, detail="No trending movies found")
        
        set_cache_data(cache_key, trending_data)
        return {"data": trending_data, "cached": False}
        
    except Exception as e:
        logger.error(f"Error fetching trending movies: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch trending movies: {str(e)}")

@app.get('/api/trending_tv')
async def get_trending_tv():
    """Get trending TV shows with caching"""
    try:
        cache_key = "trending_tv"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info("Cache hit for trending TV shows")
            return {"data": cached_data, "cached": True}
        
        logger.info("Fetching trending TV shows")
        trending_data = HomeMoviesApi.trendingTV(None)
        
        if not trending_data:
            raise HTTPException(status_code=404, detail="No trending TV shows found")
        
        set_cache_data(cache_key, trending_data)
        return {"data": trending_data, "cached": False}
        
    except Exception as e:
        logger.error(f"Error fetching trending TV shows: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch trending TV shows: {str(e)}")

@app.get('/api/popular_movies')
async def get_popular_movies():
    """Get popular movies with caching"""
    try:
        cache_key = "popular_movies"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info("Cache hit for popular movies")
            return {"data": cached_data, "cached": True}
        
        logger.info("Fetching popular movies")
        popular_data = HomeMoviesApi.popularMovies(None)
        
        if not popular_data:
            raise HTTPException(status_code=404, detail="No popular movies found")
        
        set_cache_data(cache_key, popular_data)
        return {"data": popular_data, "cached": False}
        
    except Exception as e:
        logger.error(f"Error fetching popular movies: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch popular movies: {str(e)}")

@app.get('/api/popular_tv')
async def get_popular_tv():
    """Get popular TV shows with caching"""
    try:
        cache_key = "popular_tv"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info("Cache hit for popular TV shows")
            return {"data": cached_data, "cached": True}
        
        logger.info("Fetching popular TV shows")
        popular_data = HomeMoviesApi.popularTV(None)
        
        if not popular_data:
            raise HTTPException(status_code=404, detail="No popular TV shows found")
        
        set_cache_data(cache_key, popular_data)
        return {"data": popular_data, "cached": False}
        
    except Exception as e:
        logger.error(f"Error fetching popular TV shows: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch popular TV shows: {str(e)}")

@app.get('/api/latest_movies')
async def get_latest_movies():
    """Get latest movies with caching"""
    try:
        cache_key = "latest_movies"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info("Cache hit for latest movies")
            return {"data": cached_data, "cached": True}
        
        logger.info("Fetching latest movies")
        latest_data = HomeMoviesApi.latestMovies(None)
        
        if not latest_data:
            raise HTTPException(status_code=404, detail="No latest movies found")
        
        set_cache_data(cache_key, latest_data)
        return {"data": latest_data, "cached": False}
        
    except Exception as e:
        logger.error(f"Error fetching latest movies: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch latest movies: {str(e)}")

@app.get('/api/movie/{movie_id}')
async def get_movie_details(movie_id: str):
    """Get detailed movie information with caching"""
    try:
        if not movie_id or len(movie_id.strip()) == 0:
            raise HTTPException(status_code=400, detail="Movie ID is required")
        
        cache_key = f"movie_details_{movie_id}"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for movie details: {movie_id}")
            return {"data": cached_data, "cached": True}
        
        logger.info(f"Fetching movie details for: {movie_id}")
        movie_data = HomeMoviesApi.moviesEpisode(movie_id=movie_id)
        
        if not movie_data:
            raise HTTPException(status_code=404, detail=f"Movie with ID '{movie_id}' not found")
        
        set_cache_data(cache_key, movie_data)
        return {"data": movie_data, "cached": False, "movie_id": movie_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching movie details for {movie_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch movie details: {str(e)}")

@app.get('/api/tv/{tv_id}')
async def get_tv_details(tv_id: str):
    """Get detailed TV show information with caching"""
    try:
        if not tv_id or len(tv_id.strip()) == 0:
            raise HTTPException(status_code=400, detail="TV show ID is required")
        
        cache_key = f"tv_details_{tv_id}"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for TV show details: {tv_id}")
            return {"data": cached_data, "cached": True}
        
        logger.info(f"Fetching TV show details for: {tv_id}")
        tv_data = HomeMoviesApi.tvEpisode(tv_id=tv_id)
        
        if not tv_data:
            raise HTTPException(status_code=404, detail=f"TV show with ID '{tv_id}' not found")
        
        set_cache_data(cache_key, tv_data)
        return {"data": tv_data, "cached": False, "tv_id": tv_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching TV show details for {tv_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch TV show details: {str(e)}")
@app.get('/search')
async def search_anime_endpoint(name: str = Query(..., min_length=1, description="Anime name to search for")):
    """Search for anime with caching and validation"""
    try:
        if not name or len(name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Search name is required")
        
        cache_key = f"anime_search_{name.lower().strip()}"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for anime search: {name}")
            return {"data": cached_data, "cached": True, "query": name}
        
        logger.info(f"Searching anime: {name}")
        search_results = search_anime(name)
        
        if not search_results:
            raise HTTPException(status_code=404, detail=f"No anime found for search term: {name}")
        
        set_cache_data(cache_key, search_results)
        return {"data": search_results, "cached": False, "query": name, "count": len(search_results)}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error searching anime '{name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to search anime: {str(e)}")

@app.get('/details')
async def get_anime_details(slug: str = Query(..., min_length=1, description="Anime slug identifier"), request: Request = None):
    """Get detailed anime information with caching and error handling"""
    try:
        if not slug or len(slug.strip()) == 0:
            raise HTTPException(status_code=400, detail="Anime slug is required")
        
        cache_key = f"anime_details_{slug}"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for anime details: {slug}")
            return {"data": cached_data, "cached": True}
        
        logger.info(f"Fetching anime details for: {slug}")
        details_url = f"{base_url}category/{slug}"
        html = requests.get(details_url, timeout=10)
        
        if html.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Anime with slug '{slug}' not found")
        
        soup = bsoup(html.text)
        
        # Extract anime information with error handling
        try:
            anime_info = soup.find('div', attrs={"class": "anime_info_body_bg"})
            if not anime_info:
                raise HTTPException(status_code=404, detail="Anime information not found")
            
            title = anime_info.h1.text if anime_info.h1 else "Unknown Title"
            thumbnail = anime_info.img.get('src') if anime_info.img else ""
            
            episode_page = soup.find('ul', attrs={"id": "episode_page"})
            ep_end = episode_page.find('li').a.get("ep_end") if episode_page else "1"
            
            desc_info = anime_info.find_all('p', attrs={"class": "type"})
            
            # Safely extract information with defaults
            anime_type = desc_info[0].text.replace('\n', '').strip().replace('Type: ', '') if len(desc_info) > 0 else "Unknown"
            desc = desc_info[1].text.replace('\n', '').strip().replace('Plot Summary: ', '') if len(desc_info) > 1 else "No description available"
            genre = desc_info[2].text.replace('\n', '').strip().replace('Genre: ', '') if len(desc_info) > 2 else "Unknown"
            released = desc_info[3].text.replace('\n', '').strip().replace('Released: ', '') if len(desc_info) > 3 else "Unknown"
            status = desc_info[4].text.replace('\n', '').strip().replace('Status: ', '') if len(desc_info) > 4 else "Unknown"
            other_name = desc_info[5].text.replace('\n', '').strip().replace('Other name: ', '') if len(desc_info) > 5 else ""
            
            # Generate episode links
            episodes = []
            try:
                ep_count = int(ep_end)
                base_host = request.url.hostname if request else "localhost:8080"
                episodes = [{
                    f'episode_{x}': f"http://{base_host}/episode?slug={slug}&ep={x}"
                } for x in range(1, min(ep_count + 1, 1000))]  # Limit to 1000 episodes max
            except (ValueError, TypeError):
                episodes = []
            
            data = {
                "title": title,
                "thumbnail": thumbnail,
                "type": anime_type,
                "summary": desc,
                "genre": genre,
                "release_year": released,
                "status": status,
                "other_name": other_name,
                "total_episodes": ep_end,
                "episodes": episodes
            }
            
            set_cache_data(cache_key, data)
            return {"data": data, "cached": False, "slug": slug}
            
        except Exception as parse_error:
            logger.error(f"Error parsing anime details for {slug}: {str(parse_error)}")
            raise HTTPException(status_code=500, detail="Failed to parse anime information")
        
    except HTTPException:
        raise
    except requests.RequestException as e:
        logger.error(f"Network error fetching anime details for {slug}: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        logger.error(f"Error fetching anime details for {slug}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch anime details: {str(e)}")

@app.get('/episode')
async def get_episode_links(
    slug: str = Query(..., min_length=1, description="Anime slug identifier"),
    ep: int = Query(..., ge=1, description="Episode number (minimum 1)")
):
    """Get streaming links for specific anime episode with caching"""
    try:
        cache_key = f"episode_{slug}_{ep}"
        cached_data = get_cached_data(cache_key)
        
        if cached_data:
            logger.info(f"Cache hit for episode: {slug} ep {ep}")
            return {"data": cached_data, "cached": True}
        
        logger.info(f"Fetching episode links for: {slug} episode {ep}")
        episode_url = f"{base_url}{slug}-episode-{ep}"
        html = requests.get(episode_url, timeout=10)
        
        if html.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Episode {ep} not found for anime '{slug}'")
        
        soup = bsoup(html.text)
        links_div = soup.find('div', attrs={"class": "anime_muti_link"})
        
        if not links_div:
            raise HTTPException(status_code=404, detail="No streaming links found for this episode")
        
        links = links_div.find_all('a')
        if not links:
            raise HTTPException(status_code=404, detail="No streaming servers available")
        
        stream_links = []
        for i, link in enumerate(links[:3]):  # Limit to first 3 servers
            try:
                data_video = link.get('data-video')
                if data_video:
                    stream_url = gogo_play(data_video)
                    server_name = f"Server_{i+1}" if i > 0 else "GGA"
                    stream_links.append({
                        "link": stream_url,
                        "server": server_name,
                        "quality": "HD"  # Default quality
                    })
            except Exception as link_error:
                logger.warning(f"Failed to process streaming link {i}: {str(link_error)}")
                continue
        
        if not stream_links:
            raise HTTPException(status_code=404, detail="No valid streaming links found")
        
        response_data = {
            "anime_slug": slug,
            "episode_number": ep,
            "stream_links": stream_links,
            "total_servers": len(stream_links)
        }
        
        set_cache_data(cache_key, response_data)
        return {"data": response_data, "cached": False}
        
    except HTTPException:
        raise
    except requests.RequestException as e:
        logger.error(f"Network error fetching episode {ep} for {slug}: {str(e)}")
        raise HTTPException(status_code=503, detail="Service temporarily unavailable")
    except Exception as e:
        logger.error(f"Error fetching episode {ep} for {slug}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch episode links: {str(e)}")

# Additional utility endpoints
@app.get('/api/health')
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "cache_size": len(cache),
        "version": "2.0.0"
    }

@app.get('/api/cache/clear')
async def clear_cache():
    """Clear all cached data (admin endpoint)"""
    global cache
    cache_size = len(cache)
    cache.clear()
    logger.info(f"Cache cleared, removed {cache_size} entries")
    return {
        "message": f"Cache cleared successfully",
        "cleared_entries": cache_size,
        "timestamp": time.time()
    }


if __name__== "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8080)

