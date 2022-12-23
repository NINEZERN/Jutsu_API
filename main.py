from api import Jutsu
import tqdm

class ChoiceError(Exception):
    """Raise if u wrote a wrong choice"""

def _print_anime(animes: list) -> None:
    for n, anime in enumerate(animes):
        print (f"[{n+1}] [{anime.title} - {anime.link}]")


def main():
    jutsu = Jutsu()
    # animes = jutsu.search(input("Write an anime ->"))
    animes = jutsu.search('гуль')
    _print_anime(animes=animes)
    print (animes[0].get_description())
    print (animes[0].get_image())
    # for epizode in tqdm(range(78, 149)):
    #     animes[0].download(epizode=epizode, path="Anime/")



        

if __name__ == "__main__":
    main()