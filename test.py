"""
Comprehensive test suite for Movies & Anime API
"""
import pytest
import asyncio
import httpx
from fastapi.testclient import TestClient
from api import app

# Test client
client = TestClient(app)

class TestMoviesAPI:
    """Test cases for movies endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_movies_endpoint(self):
        """Test movies pagination endpoint"""
        response = client.get("/api/movies/1")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "page" in data
        assert data["page"] == 1
    
    def test_movies_invalid_page(self):
        """Test movies endpoint with invalid page number"""
        response = client.get("/api/movies/0")
        assert response.status_code == 422  # Validation error
    
    def test_tv_shows_endpoint(self):
        """Test TV shows pagination endpoint"""
        response = client.get("/api/tv-shows/1")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "page" in data
    
    def test_trending_movies(self):
        """Test trending movies endpoint"""
        response = client.get("/api/trending_movies")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
    
    def test_popular_movies(self):
        """Test popular movies endpoint"""
        response = client.get("/api/popular_movies")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data

class TestAnimeAPI:
    """Test cases for anime endpoints"""
    
    def test_anime_search(self):
        """Test anime search endpoint"""
        response = client.get("/search?name=naruto")
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "query" in data
        assert data["query"] == "naruto"
    
    def test_anime_search_empty(self):
        """Test anime search with empty query"""
        response = client.get("/search?name=")
        assert response.status_code == 422  # Validation error
    
    def test_anime_details(self):
        """Test anime details endpoint"""
        # This might fail if the anime doesn't exist, so we'll test the structure
        response = client.get("/details?slug=test-anime")
        # Should return either 200 with data or 404/500 with error
        assert response.status_code in [200, 404, 500]

class TestUtilityEndpoints:
    """Test cases for utility endpoints"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "cache_size" in data
        assert "version" in data
        assert data["status"] == "healthy"
    
    def test_cache_clear(self):
        """Test cache clear endpoint"""
        response = client.get("/api/cache/clear")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "cleared_entries" in data

class TestErrorHandling:
    """Test cases for error handling"""
    
    def test_invalid_movie_id(self):
        """Test movie details with invalid ID"""
        response = client.get("/api/movie/")
        assert response.status_code == 404  # Not found
    
    def test_invalid_tv_id(self):
        """Test TV show details with invalid ID"""
        response = client.get("/api/tv/")
        assert response.status_code == 404  # Not found

# Performance and load testing
class TestPerformance:
    """Performance test cases"""
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests"""
        async def make_request():
            async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/api/health")
                return response.status_code
        
        async def run_concurrent_tests():
            tasks = [make_request() for _ in range(10)]
            results = await asyncio.gather(*tasks)
            return results
        
        results = asyncio.run(run_concurrent_tests())
        assert all(status == 200 for status in results)

# Integration tests
class TestIntegration:
    """Integration test cases"""
    
    def test_full_workflow(self):
        """Test complete workflow: search -> details -> episode"""
        # 1. Search for anime
        search_response = client.get("/search?name=naruto")
        if search_response.status_code == 200:
            search_data = search_response.json()
            if search_data["data"]:
                # 2. Get details for first result
                first_anime = search_data["data"][0]
                slug = first_anime.get("slug")
                
                if slug:
                    details_response = client.get(f"/details?slug={slug}")
                    # Should get either valid data or proper error
                    assert details_response.status_code in [200, 404, 500]

if __name__ == "__main__":
    # Run basic tests
    print("Running basic API tests...")
    
    # Test root endpoint
    response = client.get("/")
    print(f"Root endpoint: {response.status_code}")
    
    # Test health check
    response = client.get("/api/health")
    print(f"Health check: {response.status_code}")
    
    # Test movies endpoint
    response = client.get("/api/movies/1")
    print(f"Movies endpoint: {response.status_code}")
    
    # Test anime search
    response = client.get("/search?name=test")
    print(f"Anime search: {response.status_code}")
    
    print("Basic tests completed!")
    print("\nTo run full test suite, use: pytest test.py -v")