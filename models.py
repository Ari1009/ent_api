"""
Pydantic models for API request/response validation
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl

class MovieBase(BaseModel):
    """Base movie model"""
    title: str = Field(..., description="Movie title")
    id: str = Field(..., description="Movie ID")
    image: Optional[str] = Field(None, description="Movie poster URL")
    year: Optional[str] = Field(None, description="Release year")
    duration: Optional[str] = Field(None, description="Movie duration")
    type: Optional[str] = Field(None, description="Content type")

class TVShowBase(BaseModel):
    """Base TV show model"""
    title: str = Field(..., description="TV show title")
    id: str = Field(..., description="TV show ID")
    image: Optional[str] = Field(None, description="TV show poster URL")
    season: Optional[str] = Field(None, description="Number of seasons")
    eps: Optional[str] = Field(None, description="Number of episodes")
    type: Optional[str] = Field(None, description="Content type")

class AnimeSearchResult(BaseModel):
    """Anime search result model"""
    title: str = Field(..., description="Anime title")
    slug: str = Field(..., description="Anime slug identifier")
    thumbnail: Optional[str] = Field(None, description="Anime thumbnail URL")

class AnimeDetails(BaseModel):
    """Detailed anime information model"""
    title: str = Field(..., description="Anime title")
    thumbnail: Optional[str] = Field(None, description="Anime thumbnail URL")
    type: Optional[str] = Field(None, description="Anime type")
    summary: Optional[str] = Field(None, description="Plot summary")
    genre: Optional[str] = Field(None, description="Genres")
    release_year: Optional[str] = Field(None, description="Release year")
    status: Optional[str] = Field(None, description="Anime status")
    other_name: Optional[str] = Field(None, description="Alternative names")
    total_episodes: Optional[str] = Field(None, description="Total episodes")

class StreamLink(BaseModel):
    """Streaming link model"""
    link: str = Field(..., description="Streaming URL")
    server: str = Field(..., description="Server name")
    quality: Optional[str] = Field("HD", description="Video quality")

class EpisodeResponse(BaseModel):
    """Episode streaming response model"""
    anime_slug: str = Field(..., description="Anime slug")
    episode_number: int = Field(..., description="Episode number")
    stream_links: List[StreamLink] = Field(..., description="Available streaming links")
    total_servers: int = Field(..., description="Number of available servers")

class APIResponse(BaseModel):
    """Generic API response model"""
    data: Any = Field(..., description="Response data")
    cached: bool = Field(False, description="Whether data was served from cache")
    timestamp: Optional[float] = Field(None, description="Response timestamp")

class PaginatedResponse(APIResponse):
    """Paginated response model"""
    page: int = Field(..., description="Current page number")
    total_pages: Optional[int] = Field(None, description="Total pages available")
    count: Optional[int] = Field(None, description="Number of items in current page")

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    timestamp: float = Field(..., description="Current timestamp")
    cache_size: int = Field(..., description="Current cache size")
    version: str = Field(..., description="API version")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Error details")
    timestamp: Optional[float] = Field(None, description="Error timestamp")