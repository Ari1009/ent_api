# Movies & Anime API - Complete Documentation

## Project Overview

The **Movies & Anime API v2.0** is a comprehensive FastAPI-based web scraping service that aggregates content from multiple sources including LookMovies and GogoAnime. This enhanced version includes robust error handling, caching, rate limiting, and comprehensive testing.

## Architecture & Design Decisions

### Core Architecture
- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **Async/Await Pattern**: Non-blocking operations for better performance
- **Modular Design**: Separated concerns across multiple files
- **Caching Layer**: In-memory caching with TTL for improved response times
- **Error Handling**: Comprehensive exception handling with proper HTTP status codes

### Key Design Considerations

1. **Performance Optimization**
   - Implemented caching to reduce external API calls
   - Async operations for non-blocking requests
   - Connection pooling for HTTP requests
   - Rate limiting to prevent abuse

2. **Reliability & Error Handling**
   - Graceful degradation when external services fail
   - Comprehensive logging for debugging
   - Retry mechanisms for transient failures
   - Input validation using Pydantic models

3. **Security**
   - CORS configuration for cross-origin requests
   - Input sanitization to prevent injection attacks
   - Rate limiting to prevent abuse
   - Trusted host middleware

4. **Maintainability**
   - Clean code structure with separation of concerns
   - Comprehensive test suite
   - Configuration management through environment variables
   - Detailed documentation and type hints

## API Endpoints

### Movies & TV Shows

#### Get Movies (Paginated)
```http
GET /api/movies/{page}
```
- **Description**: Retrieve paginated list of movies
- **Parameters**: 
  - `page` (int): Page number (minimum 1)
- **Response**: List of movies with metadata
- **Caching**: 5 minutes TTL

#### Get TV Shows (Paginated)
```http
GET /api/tv-shows/{page}
```
- **Description**: Retrieve paginated list of TV shows
- **Parameters**: 
  - `page` (int): Page number (minimum 1)
- **Response**: List of TV shows with metadata

#### Get Trending Content
```http
GET /api/trending_movies
GET /api/trending_tv
```
- **Description**: Get currently trending movies/TV shows
- **Caching**: 5 minutes TTL

#### Get Popular Content
```http
GET /api/popular_movies
GET /api/popular_tv
```
- **Description**: Get popular movies/TV shows
- **Caching**: 5 minutes TTL

#### Get Latest Content
```http
GET /api/latest_movies
```
- **Description**: Get latest released movies
- **Caching**: 5 minutes TTL

#### Get Top IMDB Rated
```http
GET /api/top-imdb/movies/{page}
GET /api/top-imdb/tv-shows/{page}
```
- **Description**: Get top IMDB rated content
- **Parameters**: 
  - `page` (int): Page number (minimum 1)

#### Get Detailed Information
```http
GET /api/movie/{movie_id}
GET /api/tv/{tv_id}
```
- **Description**: Get detailed information including cast, genres, streaming links
- **Parameters**: 
  - `movie_id/tv_id` (string): Content identifier
- **Response**: Detailed content information with streaming data

### Anime Endpoints

#### Search Anime
```http
GET /search?name={anime_name}
```
- **Description**: Search for anime by name
- **Parameters**: 
  - `name` (string): Anime name to search for (minimum 1 character)
- **Response**: List of matching anime with thumbnails and slugs
- **Caching**: 5 minutes TTL

#### Get Anime Details
```http
GET /details?slug={anime_slug}
```
- **Description**: Get detailed anime information
- **Parameters**: 
  - `slug` (string): Anime slug identifier
- **Response**: Complete anime details including episodes, genres, plot summary
- **Caching**: 5 minutes TTL

#### Get Episode Streaming Links
```http
GET /episode?slug={anime_slug}&ep={episode_number}
```
- **Description**: Get streaming links for specific anime episode
- **Parameters**: 
  - `slug` (string): Anime slug identifier
  - `ep` (int): Episode number (minimum 1)
- **Response**: Available streaming servers and links
- **Caching**: 5 minutes TTL

### Utility Endpoints

#### Health Check
```http
GET /api/health
```
- **Description**: API health status and metrics
- **Response**: Service status, cache size, version info

#### Clear Cache
```http
GET /api/cache/clear
```
- **Description**: Clear all cached data (admin endpoint)
- **Response**: Number of cleared cache entries

## Response Format

All endpoints return JSON responses with the following structure:

```json
{
  "data": [...],           // Actual response data
  "cached": false,         // Whether data was served from cache
  "page": 1,              // Current page (for paginated responses)
  "query": "search_term", // Search query (for search responses)
  "count": 10             // Number of items (when applicable)
}
```

### Error Response Format
```json
{
  "error": "error_type",
  "detail": "Detailed error message",
  "timestamp": 1640995200.0
}
```

## Configuration

### Environment Variables
Create a `.env` file based on `.env.example`:

```env
# API Configuration
API_TITLE="Movies & Anime API"
API_VERSION="2.0.0"
DEBUG=false

# Server Configuration
HOST="127.0.0.1"
PORT=8080

# Cache Configuration
CACHE_TTL=300
MAX_CACHE_SIZE=1000

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## Installation & Setup

### Local Development

1. **Clone the repository**
```bash
git clone <repository-url>
cd movies-anime-api
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the application**
```bash
python api.py
```

The API will be available at `http://127.0.0.1:8080`

### Production Deployment

#### Vercel Deployment
The project is configured for Vercel deployment with `now.json`:

```bash
vercel --prod
```

#### Docker Deployment
Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
```

Build and run:
```bash
docker build -t movies-anime-api .
docker run -p 8080:8080 movies-anime-api
```

## Testing

### Run Test Suite
```bash
# Install test dependencies
pip install pytest httpx

# Run all tests
pytest test.py -v

# Run specific test class
pytest test.py::TestMoviesAPI -v

# Run with coverage
pytest test.py --cov=api
```

### Manual Testing
```bash
# Basic functionality test
python test.py

# API documentation
curl http://127.0.0.1:8080/docs
```

## Performance Considerations

### Caching Strategy
- **TTL**: 5 minutes for most endpoints
- **Size Limit**: 1000 entries maximum
- **LRU Eviction**: Oldest entries removed when cache is full

### Rate Limiting
- **Default**: 100 requests per minute per IP
- **Configurable**: Through environment variables
- **Response**: HTTP 429 when limit exceeded

### Optimization Tips
1. Use caching effectively by making repeated requests
2. Implement client-side caching for frequently accessed data
3. Use pagination for large datasets
4. Monitor cache hit rates and adjust TTL accordingly

## Monitoring & Logging

### Health Monitoring
- Use `/api/health` endpoint for service monitoring
- Monitor cache hit rates and performance metrics
- Set up alerts for error rates and response times

### Logging Configuration
```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Security Considerations

1. **CORS Configuration**: Restrict origins in production
2. **Rate Limiting**: Prevent API abuse
3. **Input Validation**: All inputs validated using Pydantic
4. **Error Handling**: No sensitive information in error responses
5. **HTTPS**: Use HTTPS in production environments

## Troubleshooting

### Common Issues

1. **External Service Unavailable**
   - Check network connectivity
   - Verify external service status
   - Review retry configuration

2. **High Memory Usage**
   - Reduce cache size limit
   - Implement cache cleanup
   - Monitor memory usage

3. **Slow Response Times**
   - Check cache hit rates
   - Optimize external API calls
   - Consider implementing database caching

### Debug Mode
Enable debug mode for detailed error information:
```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is for educational purposes. Please respect the terms of service of the websites being scraped and consider the legal implications of web scraping in your jurisdiction.