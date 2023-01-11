import requests
from bs4 import BeautifulSoup
from enum import Enum
from requests import Response
from typing import NamedTuple
from fake_useragent import UserAgent


class Episode(NamedTuple):
    title: str
    link: str


class Season(NamedTuple):
    title: str
    link: str

class Quality(Enum):
    HIGHT = 0






class Anime:

    def __init__(self, title, link) -> None:
        self.title = title
        self.link = link
        self.ua = UserAgent()
        self.HEADERS = {
            "User-Agent": self.ua.random
        }

    def _get_description(self):
        r = requests.get(self.link, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        description = \
            [span for span in soup.find('p', class_="under_video uv_rounded_bottom the_hildi").find_all("span")][0]
        return description

    def _get_image(self):
        r = requests.get(self.link, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        image = soup.find("div", class_="all_anime_title").get("style").split(")")[0].split("(")[-1].replace("'", "")
        return image

    def get_episodes(self, season: Season = None) -> list[Episode]:
        
        r = requests.get(season.link if season else self.link, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        last_episode = soup.find("div", class_="watch_l").find_all('a')
        last_episodes = []
        for i in last_episode:
            if 'серия' in i.text:
                last_episodes.append(i)
        return last_episodes[-1].text.split(' ')[-2]

    def get_seasons(self):
        r = requests.get(self.link, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        seasons = [Season(link="https://jut.su" + season.find("a").get("href"), title=season.find("a").text) for season
                   in soup.find_all("div", class_="the_invis")]
        return seasons
        
        
    def _get_video_url(self, page_url: str, quality) -> str:
        r = requests.get(page_url, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        quality_dict = {
            '1080': 0,
            '720': 1,
            '480': 2,
            '360': 3
        }
        quality = str(quality)
        print (quality)
        print (quality_dict[quality])
        video_link = soup.find(id='my-player').find_all('source')[quality_dict.get(quality, 1)].get('src')
        print (video_link)
        return video_link

    def _download(self, video_link: str, path: str):
        vid = requests.get(video_link, headers=self.HEADERS)
        with open(path, 'wb') as f:
            f.write(vid.content)

    def download(self, episode: int, path: str, season: Season = None, quality = 720):
        if season is None:
            page_url = f"{self.link}episode-{episode}.html"
        else:
            page_url = f"{season.link}episode-{episode}.html"
        video_link = self._get_video_url(page_url, quality=quality)
        video_name = video_link.split('/')[-1].split("?")[0]
        self._download(video_link, path=path + video_name)


class Jutsu:

    def __init__(self) -> None:
        self.ua = UserAgent()

    def _parse_anime(self, response: Response) -> list[Anime]:
        """Taking html and returning list of `Anime`"""
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [title.text for title in soup.find_all("div", class_="aaname")]
        links = ["https://jut.su" + link.find("a").get("href") for link in soup.find_all("span", class_="the_invis")]

        animes = []
        for i in range(len(titles)):
            animes.append(Anime(title=titles[i], link=links[i]))
        return animes

    def search(self, anime: str) -> list[Anime]:
        """Taking an anime, then parsing html from Jutsu"""
        url = "https://jut.su/anime/"
        headers = {
            "User-Agent": self.ua.random
        }
        s = requests.Session()
        data = {
            'ajax_load': 'yes',
            'start_from_page': 1,
            'show_search': anime,
            'anime_of_user': ''
        }
        s.get(url=url, headers=headers)
        post_request = s.post(url, data, headers=headers)
        animes = self._parse_anime(post_request)
        return animes
