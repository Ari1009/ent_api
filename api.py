from fastapi import FastAPI
import uvicorn

from MoviesApi import *
from gogoanime import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def main():
    return "Hello !"

@app.get('/api/movies/{page}')
async def movies(page:int):
    movies = HomeMoviesApi.Movies(page=page)
    return movies

@app.get('/api/tv-shows/{page}')
async def tvshows(page:int):
    tvshows = HomeMoviesApi.TV(page=page)
    return tvshows
    

@app.get('/api/top-imdb/movies/{page}')
async def topImdbMovies(page:int):
    imdbmovies = HomeMoviesApi.TOPIMDBMOVIES(page=page)
    return imdbmovies

@app.get('/api/top-imdb/tv-shows/{page}')
async def topImdbtv(page:int):
    imdbtv = HomeMoviesApi.TOPIMDBTV(page=page)
    return imdbtv



@app.get('/api/trending_movies')
def trending_movies():
    trending_movies = HomeMoviesApi.trendingMovies(None)
    return trending_movies


@app.get('/api/trending_tv')
def trending_tv():
    trending_tv = HomeMoviesApi.trendingTV(None)
    return trending_tv


@app.get('/api/popular_movies')
def popular_movies():
    popular_movies = HomeMoviesApi.popularMovies(None)
    return popular_movies


@app.get('/api/popular_tv')
def popular_tv():
    popular_tv = HomeMoviesApi.popularTV(None)
    return popular_tv


@app.get('/api/popular_movies')
def popular_movies():
    popular_movies = HomeMoviesApi.popularMovies(None)
    return popular_movies

@app.get('/api/latest_movies')
def latest_movies():
    latest_movies = HomeMoviesApi.latestMovies(None)
    return latest_movies

@app.get('/api/movie/{movie_id}')
async def movie_episode(movie_id : str):
    movie_episode = HomeMoviesApi.moviesEpisode(movie_id=movie_id)
    return movie_episode

@app.get('/api/tv/{tv_id}')
async def tv_episode(tv_id : str):
    tv_episode = HomeMoviesApi.tvEpisode(tv_id=tv_id)
    return tv_episode
@app.get('/search')
async def search(name: str):
    data = search_anime(name)
    return {'response': data}


@app.get('/details')
def anime_details(slug:str , request: Request):
    details_url = f"{base_url}category/{slug}"
    html = requests.get(details_url)
    soup = bsoup(html.text)
    title = soup.find('div',attrs={"class":"anime_info_body_bg"}).h1.text
    thumbnail = soup.find('div',attrs={"class":"anime_info_body_bg"}).img.get('src')
    ep_end = soup.find('ul',attrs={"id":"episode_page"}).find('li').a.get("ep_end")
    desc_info =soup.find('div',attrs={"class":"anime_info_body_bg"}).find_all('p',attrs={"class":"type"})
    type = desc_info[0].text.replace('\n','').strip().replace('Type: ','')
    desc = desc_info[1].text.replace('\n','').strip().replace('Plot Summary: ','')
    genre = desc_info[2].text.replace('\n','').strip().replace('Genre: ','')
    released = desc_info[3].text.replace('\n','').strip().replace('Released: ','')
    status = desc_info[4].text.replace('\n','').strip().replace('Status: ','')
    other_name = desc_info[5].text.replace('\n','').strip().replace('Other name: ','')

    data = {
        "title":title,
        "thumbnail":thumbnail,
        "type":type,
        "summary":desc,
        "genre":genre,
        "release_year":released,
        "status":status,
        "other_name":other_name,
        "episodes":[{
            f'{x}': f"{request.url.hostname}/episode?slug={slug}&ep={x}"
        } for x in range(1,int(ep_end))]
    }
    return {'response':data}


@app.get('/episode')
def episode_link(slug,ep):
    episode_url = f"{base_url}{slug}-episode-{ep}"
    html = requests.get(episode_url)
    soup = bsoup(html.text)
    links_div = soup.find('div',attrs={"class":"anime_muti_link"}).find_all('a')
    data = {
        "stream_links":[
            {
            "link": gogo_play(links_div[0]['data-video']),
            "server":"GGA"
            }
        ]
    }
    return {'response':data}


if __name__== "__main__":
   uvicorn.run(app, host="127.0.0.1", port=8080)

