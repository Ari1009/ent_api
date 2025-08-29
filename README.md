# Movies & Anime API

A FastAPI-based web scraping API that provides access to movies, TV shows, and anime content from various sources including LookMovies and GogoAnime.

## Features

### Movies & TV Shows
- Browse movies and TV shows with pagination
- Get trending, popular, and latest content
- Top IMDB rated movies and TV shows
- Detailed movie/TV show information with cast, genres, and streaming links
- Search functionality

### Anime
- Search anime by title
- Get anime details including episodes, genres, and plot summary
- Stream links for anime episodes
- Support for GogoAnime content

## API Endpoints

### Movies
- `GET /api/movies/{page}` - Get paginated movies list
- `GET /api/movie/{movie_id}` - Get detailed movie information
- `GET /api/trending_movies` - Get trending movies
- `GET /api/popular_movies` - Get popular movies
- `GET /api/latest_movies` - Get latest movies
- `GET /api/top-imdb/movies/{page}` - Get top IMDB rated movies

### TV Shows
- `GET /api/tv-shows/{page}` - Get paginated TV shows list
- `GET /api/tv/{tv_id}` - Get detailed TV show information with seasons/episodes
- `GET /api/trending_tv` - Get trending TV shows
- `GET /api/popular_tv` - Get popular TV shows
- `GET /api/top-imdb/tv-shows/{page}` - Get top IMDB rated TV shows

### Anime
- `GET /search?name={anime_name}` - Search for anime
- `GET /details?slug={anime_slug}` - Get anime details
- `GET /episode?slug={anime_slug}&ep={episode_number}` - Get episode streaming links

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python api.py
```

The API will be available at `http://127.0.0.1:8080`

## Dependencies

- **FastAPI** - Modern web framework for building APIs
- **uvicorn** - ASGI server for running FastAPI
- **BeautifulSoup4** - HTML parsing library for web scraping
- **requests** - HTTP library for making web requests
- **aiohttp** - Async HTTP client/server framework

## Deployment

This project is configured for deployment on Vercel using the `now.json` configuration file.

## Usage Examples

### Get trending movies
```bash
curl http://127.0.0.1:8080/api/trending_movies
```

### Search for anime
```bash
curl "http://127.0.0.1:8080/search?name=naruto"
```

### Get movie details
```bash
curl http://127.0.0.1:8080/api/movie/movie-id-here
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://127.0.0.1:8080/docs`
- ReDoc: `http://127.0.0.1:8080/redoc`

## CORS

The API is configured with CORS middleware to allow requests from any origin (`*`). Modify the `origins` list in `api.py` to restrict access as needed.

## Note

This project is for educational purposes. Please respect the terms of service of the websites being scraped and consider the legal implications of web scraping in your jurisdiction.