"""
Utility functions for the Movies & Anime API
"""
import time
import hashlib
import logging
from typing import Optional, Dict, Any, Callable
from functools import wraps
import asyncio
import aiohttp
from config import settings

logger = logging.getLogger(__name__)

class RateLimiter:
    """Simple rate limiter implementation"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
    
    def is_allowed(self, identifier: str) -> bool:
        """Check if request is allowed for given identifier"""
        current_time = time.time()
        
        # Clean old entries
        self.requests = {
            k: v for k, v in self.requests.items() 
            if current_time - v['first_request'] < self.window_seconds
        }
        
        if identifier not in self.requests:
            self.requests[identifier] = {
                'count': 1,
                'first_request': current_time
            }
            return True
        
        if self.requests[identifier]['count'] < self.max_requests:
            self.requests[identifier]['count'] += 1
            return True
        
        return False

class CacheManager:
    """Enhanced cache manager with TTL and size limits"""
    
    def __init__(self, ttl: int = 300, max_size: int = 1000):
        self.ttl = ttl
        self.max_size = max_size
        self.cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get data from cache if not expired"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Any) -> None:
        """Set data in cache with timestamp"""
        # Remove oldest entries if cache is full
        if len(self.cache) >= self.max_size:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
        
        self.cache[key] = (data, time.time())
    
    def clear(self) -> int:
        """Clear all cache entries and return count"""
        count = len(self.cache)
        self.cache.clear()
        return count
    
    def size(self) -> int:
        """Get current cache size"""
        return len(self.cache)

def generate_cache_key(*args, **kwargs) -> str:
    """Generate a cache key from arguments"""
    key_string = f"{args}_{kwargs}"
    return hashlib.md5(key_string.encode()).hexdigest()

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """Decorator to retry function on failure"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        logger.warning(f"Attempt {attempt + 1} failed: {str(e)}, retrying...")
                        await asyncio.sleep(delay * (attempt + 1))
                    else:
                        logger.error(f"All {max_retries} attempts failed")
            
            raise last_exception
        return wrapper
    return decorator

async def fetch_with_timeout(url: str, timeout: int = 10) -> str:
    """Fetch URL content with timeout"""
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=timeout)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                raise aiohttp.ClientResponseError(
                    request_info=response.request_info,
                    history=response.history,
                    status=response.status
                )

def sanitize_string(text: str) -> str:
    """Sanitize string by removing unwanted characters"""
    if not text:
        return ""
    return text.replace('\n', '').replace('\r', '').strip()

def validate_page_number(page: int) -> int:
    """Validate and normalize page number"""
    if page < 1:
        return 1
    if page > 1000:  # Reasonable upper limit
        return 1000
    return page

def format_duration(duration_str: str) -> str:
    """Format duration string consistently"""
    if not duration_str:
        return "Unknown"
    
    # Remove extra whitespace and normalize
    duration = sanitize_string(duration_str)
    
    # Add "min" if it's just a number
    if duration.isdigit():
        return f"{duration} min"
    
    return duration

def extract_year(year_str: str) -> Optional[int]:
    """Extract year from string"""
    if not year_str:
        return None
    
    # Extract 4-digit year
    import re
    year_match = re.search(r'\b(19|20)\d{2}\b', year_str)
    if year_match:
        return int(year_match.group())
    
    return None

# Global instances
rate_limiter = RateLimiter(
    max_requests=settings.RATE_LIMIT_REQUESTS,
    window_seconds=settings.RATE_LIMIT_WINDOW
)

cache_manager = CacheManager(
    ttl=settings.CACHE_TTL,
    max_size=settings.MAX_CACHE_SIZE
)