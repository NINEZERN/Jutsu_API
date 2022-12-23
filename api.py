import requests
from bs4 import BeautifulSoup


class Anime:

    def __init__(self, title, link) -> None:
        self.title = title
        self.link = link
        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }
    

    def _get_description(self):
        r = requests.get(self.link, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        description = [span for span in soup.find('p', class_="under_video uv_rounded_bottom the_hildi").find_all("span")][0]
        return description


    def _get_image(self):
        r = requests.get(self.link, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        image = soup.find("div", class_="all_anime_title").get("style").split(")")[0].split("(")[-1].replace("'", "")
        return image


    def get_seasons(self):
        r = requests.get(self.link, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        seasons = [season.text for season in soup.find_all("h2", class_="b-b-title the-anime-season center")]
        return seasons


    def _get_video_url(self, page_url: str) -> str:
        r = requests.get(page_url, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        video_link = soup.find(id='my-player').find_all('source')[1].get('src')
        return video_link

    
    def _download(self, video_link: str, path: str):
        vid = requests.get(video_link, headers=self.HEADERS)
        with open(path, 'wb') as f:
            f.write(vid.content)
        
        
    def download(self, epizode, path: str):
        page_url = f"{self.link}episode-{epizode}.html"
        video_link = self._get_video_url(page_url)
        video_name = video_link.split('/')[-1].split("?")[0]
        self._download(video_link, path=path+video_name)


        


        
        

class Jutsu:

    def __init__(self) -> None:
        pass

    
    def _parse_anime(self,response: str) -> list[Anime]:
        """Taking html and returning list of `Anime`"""
        soup = BeautifulSoup(response.text, 'html.parser')
        titles = [title.text for title in soup.find_all("div", class_="aaname")]
        links = ["https://jut.su"+link.find("a").get("href") for link in soup.find_all("span", class_="the_invis")]
        
        animes = []        
        for i in range(len(titles)):
            animes.append(Anime(title=titles[i], link=links[i]))
        return animes


    def search(self, anime: str) -> list[Anime]:
        """Taking an anime, than parsing html from Jutsu"""
        url = "https://jut.su/anime/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        s = requests.Session()
        data = {
            'ajax_load':  'yes',
            'start_from_page':  1,
            'show_search':  anime,
            'anime_of_user': ''
        }
        r = s.get(url=url, headers=headers)
        post_request = s.post(url, data, headers=headers)
        animes = self._parse_anime(post_request)
        return animes
    