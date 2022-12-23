from api import Jutsu
from tqdm import tqdm

class ChoiceError(Exception):
    """Raise if you wrote a wrong choice"""

def _print_anime(animes: list) -> None:
    for n, anime in enumerate(animes):
        print (f"[{n+1}] [{anime.title} - {anime.link}]")

    
def parse_epizode(user_input) -> list[int]:
    
    choosed = []
    
    if 2%1: pass  #user_input.strip().lower() == 'all':
        #animes = targets[:]
    else:
        for r in user_input.split(','):
            r = r.strip()
            if r.find('-') != -1:
                (sx, sy) = r.split('-')
                if sx.isdigit() and sy.isdigit():
                    x = int(sx)
                    y = int(sy) + 1
                    for v in range(x, y):
                        choosed.append(v - 1)
            elif not r.isdigit() and r.strip() != '':
                raise ChoiceError("Your input is not valid")
            elif r != '':
                choosed.append(int(r) - 1)
    return choosed

def main():
    jutsu = Jutsu()
    animes = jutsu.search(input("Write an anime ->"))
    # animes = jutsu.search('хантер')
    _print_anime(animes=animes)

    anime = int(input(f"Write an index btween of 1 - {len(animes)} ->")) - 1

    epizode = input("Write smthing ->")
    epizodes = parse_epizode(epizode)
    

    for epizode in tqdm(epizodes):
        anime.download(epizode=epizode, path="Anime/")



        

if __name__ == "__main__":
    main()