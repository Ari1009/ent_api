from os import link
from fastapi import FastAPI, Request
from bs4 import BeautifulSoup
import lxml
import requests
import json

from requests.api import request
def bsoup(text):
    soup = BeautifulSoup(text,'lxml')
    return soup

base_url = 'https://gogoanime.ai/'

def search_anime(text):
    search_url = f'{base_url}/search.html?keyword={text}'
    html = requests.get(search_url)
    soup = bsoup(html.text)
    search_items = soup.find('div',attrs = {'class':'last_episodes'}).find_all('li')
    data = [{
        "title": x.a.get('title'),
        "slug": x.a.get('href').split('/')[-1],
        "thumbnail": x.img.get('src')
    } for x in search_items]
    return data

def gogo_play(url):
    url = 'https:'+  url.replace('streaming','ajax').replace('load','ajax')
    html = json.loads(requests.get(url).text)
    return html["source"][0]['file']

def streamsb(slug):    
    url = f"https://streamsb.net/d/{slug}"
    html = requests.get(url)
    soup = bsoup(html.text)
    list = soup.find('table',attrs={"width":"60%"}).find_all('a')[-1].get('onclick').replace('download_video(','').replace(')','').replace("'",'').split(',')
    url = f'https://streamsb.net/dl?op=download_orig&id={list[0]}&mode={list[1]}&hash={list[2]}'
    print(url)
    html = requests.get(url)
    soup = bsoup(html.text)
    link = soup.find("a",text="Direct Download Link").get('href')
    return link