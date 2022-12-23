import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PATH = "Anime/"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

def _get_video_url(page_url: str) -> str:
    r = requests.get(page_url, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    video_link = soup.find(id='my-player').find_all('source')[1].get('src')
    logger.debug("Video link received")
    return video_link

def _download_video(video_link: str, path: str):
    vid = requests.get(video_link, headers=HEADERS)
    with open('{0}'.format(path), 'wb') as f:
        f.write(vid.content)
    logger.debug("Video downloaded")

def download(epizode, path: str):
    for epizode in tqdm(range(33, 149)):
        page_url = "https://jut.su/hunter-hunter/episode-{0}.html".format(epizode)
        video_link = None
        try:
            video_link = _get_video_url(page_url)
        except Exception as e:
            logger.critical(e + " " + "Check your Ethernet connection")
        video_name = video_link.split('/')[-1].split("?")[0]
        print (video_name)
        _download_video(video_link, f'{PATH}{video_name}')
        logger.debug("Ep-{0} was downloaded".format(epizode))

    


def main():
    download()


if __name__ == "__main__":
    main()