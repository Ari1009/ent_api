from bs4 import BeautifulSoup
import aiohttp
import asyncio
import json
import requests
import cfscrape
import base64
import cloudscraper



import requests

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
}


s = requests.Session()

scraper = cfscrape.create_scraper()
parser = cloudscraper.create_scraper()

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            r = await res.text()
            return r

class GogoanimeParser():
    def __init__(self, page, animeid, episode_num, key):
        self.page = page
        self.animeid = animeid
        self.episode_num = episode_num

    def search(key, page):
        r = s.get(
            f'https://gogoanime.lu/search.html?keyword={key}&page={page}',headers=headers).text
        soup = BeautifulSoup(r, 'html.parser')
        search = soup.find('div', 'last_episodes').find('ul', 'items')
        search_list = search.find_all('li')

        animes_res = [{}]
        animes = []
        for x in search_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            animes.append({"title": f"{title}", "image_url": f"{image_url}",
                          "url": f"{url}", "released": f"{released}"})

        animes_res.append(animes)
        searched_animes = json.dumps(animes)
        search_data = json.loads(searched_animes)
        return search_data

    def get_recently_uploaded(page):
        try:
            r = s.get(f'https://gogoanime.lu/?page={page}',headers=headers).text
            soup = BeautifulSoup(r, 'html.parser')
            recently = soup.find('div', 'last_episodes').find('ul', 'items')
            recently_list = recently.find_all('li')
            anilist = dict()

            gen_ani_res = [{}]
            gen_ani = []
            for x in recently_list:
                title = x.find('p', 'name').text
                image_url = x.find('img')['src']
                url = x.find('a')['href']
                url = url.replace('/', '')
                get_id = image_url.replace(
                    '.png', '').replace('.jpg', '').split('/')
                id = get_id[-1]
                episode = x.find('p', 'episode').text
                episode = episode.replace('Episode ', '')

                gen_ani.append({"title": f"{title}", "id": f"{id}",
                                "image_url": f"{image_url}", "url": f"{url}", "episode": f"{episode}"})

            gen_ani_res.append(gen_ani)
            jsonlist = json.dumps(gen_ani)

        except:
            print('im sorry otto i cannnot get the data :( ')
        return jsonlist

    def newSeason(page):
        r = s.get(
            f'https://gogoanime.lu/new-season.html?page={page}').text
        soup = BeautifulSoup(r, 'html.parser')
        popular = soup.find('div', 'last_episodes').find('ul', 'items')
        popular_list = popular.find_all('li')

        newseason_animes_res = [{}]
        newseason_animes = []
        for x in popular_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            newseason_animes.append(
                {"title": f"{title}", "image_url": f"{image_url}", "url": f"{url}", "released": f"{released}"})

        newseason_animes_res.append(newseason_animes)
        new_animes = json.dumps(newseason_animes)
        return new_animes

    def popular(page):
        r = s.get(f'https://gogoanime.lu/popular.html?page={page}',headers=headers).text
        soup = BeautifulSoup(r, 'html.parser')
        popular = soup.find('div', 'last_episodes').find('ul', 'items')
        popular_list = popular.find_all('li')

        popular_animes_res = [{}]
        popular_animes = []
        for x in popular_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            popular_animes.append(
                {"title": f"{title}", "image_url": f"{image_url}", "url": f"{url}", "released": f"{released}"})

        popular_animes_res.append(popular_animes)
        pop_animes = json.dumps(popular_animes)
        return pop_animes

    def movies(page):
        r = s.get(
            f'https://gogoanime.lu/anime-movies.html?page={page}').text
        soup = BeautifulSoup(r, 'html.parser')
        movies = soup.find('div', 'last_episodes').find('ul', 'items')
        movies_list = movies.find_all('li')

        movie_animes_res = [{}]
        movies_animes = []
        for x in movies_list:
            title = x.find('p', 'name').text
            image_url = x.find('img')['src']
            url = x.find('a')['href']
            url = url.replace('/category/', '')
            released = x.find('p', 'released').text
            released = released.strip()

            movies_animes.append(
                {"title": f"{title}", "image_url": f"{image_url}", "url": f"{url}", "released": f"{released}"})

        movie_animes_res.append(movies_animes)
        mov_animes = json.dumps(movies_animes)
        return mov_animes
   
    def latest(page):
       url = f"https://ajax.gogo-load.com/ajax/page-recent-release.html?page={page}&type=1"
       r = s.get(url).text
       soup = BeautifulSoup(r,"html.parser")
       anime = soup.find('ul','items').find_all('li')
       gen_ani_res = [{}]
       gen_ani = []
       for x in anime:
         url = x.find('a')['href']
         url = url.replace('/', '')
         title = x.find('p','name').text
         episode = x.find('p','episode').text
         image_url = x.img['src']
         get_id = image_url.replace(
                    '.png', '').replace('.jpg', '').split('/')
         id = get_id[-1]
         gen_ani.append({
           "title":title,
         'episode':episode,
         'image_url':image_url,
         'url': url,
            'id':id
       })
       gen_ani_res.append(gen_ani)
       jsonlist = json.dumps(gen_ani)

       return jsonlist

    def details(animeid):
        url = "https://gogoanime.lu/category/" + animeid
        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        source_url = soup.find("div", {"class": "anime_info_body_bg"}).img
        image_url = source_url.get('src')
        title = soup.find("div", {"class": "anime_info_body_bg"}).h1.string
        lis = soup.find_all('p', {"class": "type"})
        plot_sum = lis[1]
        pl = plot_sum.get_text().split(':')
        pl.remove(pl[0])
        sum = ""
        plot_summary = sum.join(pl)
        type_of_show = lis[0].a['title']
        ai = lis[2].find_all('a')  # .find_all('title')
        genres = []
        for link in ai:
            genres.append(link.get('title'))
        year1 = lis[3].get_text()
        year2 = year1.split(" ")
        year = year2[1]
        status = lis[4].a.get_text()
        oth_names = lis[5].get_text()
        lnk = soup.find(id="episode_page")
        source_url = lnk.find_all("li")[-1].a
        ep_num = int(source_url.get("ep_end"))
        print(ep_num)
        res_detail_search = {"title": f"{title}", "year": f"{year}", "other_names": f"{oth_names}",
                             "type": f"{type_of_show}", "status": f"{status}", "genre": f"{genres}",
                             "episodes": f"{ep_num}", "image_url": f"{image_url}", "plot_summary": f"{plot_summary}"}

        return res_detail_search

    def genre(genre_name, page):
        try:
            url = f"https://gogoanime.lu/genre/{genre_name}?page={page}"
            response = s.get(url)
            plainText = response.text
            soup = BeautifulSoup(plainText, "html.parser")
            animes = soup.find("ul", {"class": "items"}).find_all("li")
            gen_ani = []
            for anime in animes:  # For every anime found
                tits = anime.a["title"]
                image_url = anime.find('img')['src']
                urll = anime.a["href"]
                r = urll.split('/')
                released = anime.find('p', 'released').text
                released = released.strip()
                gen_ani.append(
                    {"title": f"{tits}", "url": f"{r[2]}", "image_url": f"{image_url}", "released": f"{released}"})

            return gen_ani
        except:
            print('not found')

    def episode(animeid, episode_num):
        links = {}
        URL_PATTERN = 'https://gogoanime.lu/{}-episode-{}'
        url = URL_PATTERN.format(animeid, episode_num)
        srcCode = s.get(url)
        soup = BeautifulSoup(srcCode.text, "html.parser")
        iframe = soup.find('div', 'anime_video_body')

        ifr = iframe.find('div', 'play-video').find('iframe')
        iframe = ifr['src']
        goload = soup.find('li','vidcdn').a['data-video']
        gogoserver = f"https:{goload}"
        epid = iframe.split('/')[3].split('?id=')[1].split('&')[0]
        
       

        links['iframe'] = f"https:{iframe}"
        links['gogoserver'] = gogoserver
        links['epid'] = epid
        return links
   
    def schedule(animeid):
        time = {}
        try:
            url=f"https://animeschedule.net/anime/{animeid}".replace("2nd-season",'2').replace('season-2',"2")
            r = s.get(url)
            soup = BeautifulSoup(r.text,'html.parser')
            t = soup.find(id="countdown-wrapper").time['datetime']
            time['time'] = t
            return time
        except:
            print("there is no schedule available")

class HomeMoviesApi():
    def __init__(self, movie_id, page):
        self.movie_id = movie_id
        self.page = page
        
    
    def anime(animeid):
        data = []
        r = requests.get(f"https://animetitans.com/anime/{animeid}")
        soup = BeautifulSoup(r.text, "html.parser")
        body = soup.find('div', 'postbody')
        title = body.find('h1', 'entry-title').text
        synopsis = body.find('div', 'synp').find('div','entry-content').p.text
        image_url = body.find('div', 'thumb').img['src']
        image_cover = body.find('div', 'bigcover').img['src']
        info = body.find('div', 'spe')
        content_info = info.find_all('span')
        status = content_info[0].text.replace("الحالة: ",'')
        studio = content_info[1].text.replace("الاستديو: ",'')
        year = content_info[2].text.replace("سنة الإصدار: ",'')
        duration = content_info[3].text.replace("المدة: ",'')
        season = content_info[4].text.replace("الموسم: ",'')
        country = content_info[5].text.replace("البلد: ",'')
        typee = content_info[6].text
        episodes = content_info[7].text.replace("الحلقات: ",'')
        directors = content_info[8].text.replace("المخرج: ",'')
        date_release = content_info[9].text.replace("تاريخ النشر: ",'')
        genres = []
        g = body.find('div', 'genxed')
        for x in g.find_all('a'):
            genres.append(x.text) 
        r = body.find('div','listupd')
        recommendation = []
        for x in r.find_all('article'):
            anime_id = x.a['href']
            t = x.a['title']
            img = x.a.img['src']
            typee = x.find('div','typez').text
            recommendation.append({
                "id":anime_id,
                "title":t,
                "image_url":img,
                "type":typee
            
            })
            

        data.append({
            "title":title,
            "synopsis":synopsis,
            "image_url":image_url,
            "image_cover":image_cover,
            "status":status,
            "studio":studio,
            "year":year,
            "duration":duration,
            "season":season,
            "country":country,
            "type":typee,
            "episodes":episodes,
            "directors":directors,
            "date_release":date_release,
            "genres":genres,
            "recommendation":recommendation
        })
        return data

    def Movies(page):
        data = []
        url = f"https://lookmoviess.com/movies?page={page}"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        mv = soup.find_all('div', 'flw-item')
        for x in mv:
            id = x.find('a')['data-id']
            url = x.find('a')['href']
            title = x.find('h3', 'film-name').text.strip()
            image = x.find('img')['data-src']
            duration = x.find('span', "fdi-duration").text
            type = x.find('span', 'fdi-type').text
            year = x.find('span', 'fdi-item').text
            data.append({"title": title,
                         "id": id,
                         'url': f"https://lookmoviess.com{url}",
                         "image": image,
                         "duration": duration,
                         "type": type,
                         "year": year,

                         })
        return data

    def TV(page):
        data = []
        url = f"https://lookmoviess.com/tv-shows?page={page}"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        mv = soup.find_all('div', 'flw-item')
        for i in mv:
            image = i.img['data-src']
            url = i.a['href']
            id = i.a['data-id']
            title = i.h3.text
            fdi_items = i.find_all('span', 'fdi-item')
            season = fdi_items[0].text
            eps = fdi_items[1].text
            mv = i.find('span', 'float-right fdi-type').text
            data.append({'title': title.strip(),
                         'image': image,
                         'season': season,
                         'eps': eps,
                         'type': mv,
                         'id': id,
                         'url': f"https://lookmoviess.com{url}", })

        return data

    def TOPIMDBMOVIES(page):
        data = []
        url = f"https://lookmoviess.com/top-imdb?type=movie&page={page}"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        mv = soup.find_all('div', 'flw-item')
        for x in mv:
            id = x.find('a')['data-id']
            url = x.find('a')['href']
            title = x.find('h3', 'film-name').text.strip()
            image = x.find('img')['data-src']
            duration = x.find('span', "fdi-duration").text
            type = x.find('span', 'fdi-type').text
            year = x.find('span', 'fdi-item').text
            data.append({"title": title,
                         "id": id,
                         'url': f"https://lookmoviess.com{url}",
                         "image": image,
                         "duration": duration,
                         "type": type,
                         "year": year,

                         })
        return data

    def TOPIMDBTV(page):
        data = []
        url = f"https://lookmoviess.com/top-imdb?type=tv&page={page}"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        mv = soup.find_all('div', 'flw-item')
        for i in mv:
            image = i.img['data-src']
            url = i.a['href']
            id = i.a['data-id']
            title = i.h3.text
            fdi_items = i.find_all('span', 'fdi-item')
            season = fdi_items[0].text
            eps = fdi_items[1].text
            mv = i.find('span', 'float-right fdi-type').text
            data.append({'title': title.strip(),
                         'image': image,
                         'season': season,
                         'eps': eps,
                         'type': mv,
                         'id': id,
                         'url': f"https://lookmoviess.com{url}", })

        return data


    def trendingMovies(self):
        links = []
        results = asyncio.run(fetch("https://lookmoviess.com/"))
        soup = BeautifulSoup(results, 'html.parser')
        trending_movies = soup.find(id="trending-movies")
        for i in trending_movies.find_all('div', 'flw-item'):
            image = i.img['data-src']
            url = i.a['href']
            title = i.h3.text
            year = i.find('span', 'fdi-item').text
            duration = i.find('span', 'fdi-item fdi-duration').text
            type = i.find('span', 'float-right fdi-type').text
            links.append({'title': title.strip(),
                          'image': image,
                          'year': year,
                          'type': type,
                          'duration': duration,
                          'url': f"https://lookmoviess.com{url}"

                          })
        return links

    def trendingTV(self):
        links = []
        url = "https://lookmoviess.com"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        trending_tv = soup.find(id="trending-tv")
        for i in trending_tv.find_all('div', 'flw-item'):
            image = i.img['data-src']
            url = i.a['href']
            title = i.h3.text
            fdi_items = i.find_all('span', 'fdi-item')
            season = fdi_items[0].text
            eps = fdi_items[1].text
            mv = i.find('span', 'float-right fdi-type').text
            links.append({'title': title.strip(),
                          'image': image,
                          'season': season,
                          'eps': eps,
                          'type': mv,
                          'url': f"https://lookmoviess.com{url}"

                          })
        return links

    def popularMovies(self):
        links = []
        url = "https://lookmoviess.com"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        popular_movies = soup.find(id="popular-movies")
        for i in popular_movies.find_all('div', 'flw-item'):
            image = i.img['data-src']
            url = i.a['href']
            title = i.h3.text
            year = i.find('span', 'fdi-item').text
            duration = i.find('span', 'fdi-item fdi-duration').text
            type = i.find('span', 'float-right fdi-type').text
            links.append({'title': title.strip(),
                          'image': image,
                          'year': year,
                          'type': type,
                          'duration': duration,
                          'url': f"https://lookmoviess.com{url}"

                          })
        return links

    def popularTV(self):
        links = []
        url = "https://lookmoviess.com"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        popular_tv = soup.find(id="popular-tv")
        for i in popular_tv.find_all('div', 'flw-item'):
            image = i.img['data-src']
            url = i.a['href']
            title = i.h3.text
            fdi_items = i.find_all('span', 'fdi-item')
            season = fdi_items[0].text
            eps = fdi_items[1].text
            mv = i.find('span', 'float-right fdi-type').text
            links.append({'title': title.strip(),
                          'image': image,
                          'season': season,
                          'eps': eps,
                          'type': mv,
                          'url': f"https://lookmoviess.com{url}"

                          })
        return links

    def latestMovies(self):
        links = []
        url = "https://lookmoviess.com"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        l = soup.find_all("div", "film_list-wrap")
        latest_movies = l[4]
        for i in latest_movies.find_all('div', 'flw-item'):
            image = i.img['data-src']
            url = i.a['href']
            title = i.h3.text
            year = i.find('span', 'fdi-item').text
            duration = i.find('span', 'fdi-item fdi-duration').text
            type = i.find('span', 'float-right fdi-type').text
            links.append({'title': title.strip(),
                          'image': image,
                          'year': year,
                          'type': type,
                          'duration': duration,
                          'url': f"https://lookmoviess.com{url}"

                          })
        return links

    def latestTV(self):
        links = []
        url = "https://lookmoviess.com"
        r = requests.get(url).text
        soup = BeautifulSoup(r, 'html.parser')
        l = soup.find_all("div", "film_list-wrap")
        latest_tv = l[5]
        for i in latest_tv.find_all('div', 'flw-item'):
            image = i.img['data-src']
            url = i.a['href']
            title = i.h3.text
            fdi_items = i.find_all('span', 'fdi-item')
            season = fdi_items[0].text
            eps = fdi_items[1].text
            mv = i.find('span', 'float-right fdi-type').text
            links.append({'title': title.strip(),
                          'image': image,
                          'season': season,
                          'eps': eps,
                          'type': mv,
                          'url': f"https://lookmoviess.com{url}"

                          })

        return links

    def moviesEpisode(movie_id):
        data = []
        links = {}
        c = []
        g = []
        p = []
        co = []
        url = f"https://lookmoviess.com/movie/{movie_id}"
        r = requests.get(url).text
        soup = BeautifulSoup(r, "html.parser")
        iframe = soup.find(id="iframe-embed")['src']
        details = soup.find('div', "detail_page-infor")
        title = details.find("h2", "heading-name").text
        imdb = details.find(
            'button', 'btn-imdb').text.replace(' ', "").replace("IMDB:", '')
        trailer = soup.find(id="iframe-trailer")['data-src']
        image = details.find('img')['src']
        description = details.find('div', 'description').text.strip()
        released = details.find_all(
            'div', 'row-line')[0].text.replace(" ", "").replace("Released:", "")
        released = released.strip()
        duration = details.find_all(
            'div', 'row-line')[3].text.replace(" ", "").replace("Duration:", "")
        duration = duration.strip()
        links['title'] = title
        links['imdb'] = imdb
        links['trailer'] = trailer
        links['image'] = image
        links['description'] = description
        links['released'] = released
        links['duration'] = duration
        links['iframe'] = iframe
        data.append(links)
        genre = details.find_all('div', 'row-line')[1]
        for x in genre.find_all('a'):
            url = x['href']
            genre = x['title']
            g.append({"genres": {"url": url, "genre": genre}})

        casts = details.find_all('div', 'row-line')[2]
        for x in casts.find_all('a'):
            url = x['href']
            title = x['title']
            c.append({"casts": {"url": url, "title": title}})

        country = details.find_all('div', 'row-line')[4]
        for x in country.find_all('a'):
            url = x['href']
            country = x['title']
            co.append({"countries": {"url": url, "country": country}})
        production = details.find_all('div', 'row-line')[5]
        for x in production.find_all('a'):
            url = x['href']
            title = x['title']
            p.append({"productions": {"url": url, "title": title}})

        return data, c, g, p, co

    def tvEpisode(tv_id):
        links = {}
        data = []
        season = []
        c = []
        g = []
        p = []
        co = []
        url = f"https://lookmoviess.com/tv/{tv_id}"
        r = requests.get(url).text
        soup = BeautifulSoup(r, "html.parser")
        iframe = soup.find(id="iframe-embed")['src']
        tmdb_id = soup.find(id="watch-iframe")['data-tmdb-id']
        s = soup.find('div', 'sl-content')
        seasons = s.find('ul', 'slcs-ul').find_all('li')
        for x in seasons:
            t = []
            title = x.find('a', 'season-item')['title']
            year = x.find('span', 'float-right').text
            id = x.find('a', 'season-item')['href'].replace("#", "")
            episodes = s.find('div', 'slc-eps')
            eps = episodes.find(id=id).find_all('li')
            season.append({

                "title": title,
                "year": year,
                "episodes": t

            })
            for x in eps:
                episode_num = x.find('a', 'episode-item')['data-number']
                href = x.find('a', 'episode-item')['href']
                season_num = x.find('a', 'episode-item')['data-s-number']
                episode_title = x.find('a', 'episode-item')['title']
                t.append({"episode_title": episode_title,
                          "episode_num": episode_num,
                          "href": href,
                          "season_num": season_num})

        details = soup.find('div', "detail_page-infor")
        title = details.find("h2", "heading-name").text
        imdb = details.find(
            'button', 'btn-imdb').text.replace(' ', "").replace("IMDB:", '')
        trailer = soup.find(id="iframe-trailer")['data-src']
        image = details.find('img')['src']
        description = details.find('div', 'description').text.strip()
        released = details.find_all(
            'div', 'row-line')[0].text.replace(" ", "").replace("Released:", "")
        released = released.strip()
        duration = details.find_all(
            'div', 'row-line')[3].text.replace(" ", "").replace("Duration:", "")
        duration = duration.strip()
        links['title'] = title
        links['imdb'] = imdb
        links['trailer'] = trailer
        links['image'] = image
        links['description'] = description
        links['released'] = released
        links['duration'] = duration
        links['iframe'] = iframe
        links['tmdb_id'] = tmdb_id
        data.append(links)
        genre = details.find_all('div', 'row-line')[1]
        for x in genre.find_all('a'):
            url = x['href']
            genre = x['title']
            g.append({"genres": {"url": url, "genre": genre}})

        casts = details.find_all('div', 'row-line')[2]
        for x in casts.find_all('a'):
            url = x['href']
            title = x['title']
            c.append({"casts": {"url": url, "title": title}})

        country = details.find_all('div', 'row-line')[4]
        for x in country.find_all('a'):
            url = x['href']
            country = x['title']
            co.append({"countries": {"url": url, "country": country}})
        production = details.find_all('div', 'row-line')[5]
        for x in production.find_all('a'):
            url = x['href']
            title = x['title']
            p.append({"productions": {"url": url, "title": title}})

        return data, season, c, p, co, g
