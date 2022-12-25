from api import Jutsu
from tqdm import tqdm


class ChoiceError(Exception):
    """Raise if you wrote a wrong choice"""


def _print_anime(animes: list) -> None:
    for n, anime in enumerate(animes):
        print(f"[{n + 1}] [{anime.title}]")


def parse_epizode(user_input) -> list[int]:
    choosed = []

    if 2 % 1:
        pass  # user_input.strip().lower() == 'all':
    # animes = targets[:]
    else:
        for r in user_input.split(','):
            r = r.strip()
            if r.find('-') != -1:
                (sx, sy) = r.split('-')
                if sx.isdigit() and sy.isdigit():
                    x = int(sx)
                    y = int(sy) + 1
                    for v in range(x, y):
                        choosed.append(v)
            elif not r.isdigit() and r.strip() != '':
                raise ChoiceError("Your input is not valid")
            elif r != '':
                choosed.append(int(r))
    return choosed


def tes_episodes():
    jutsu = Jutsu()

    # anime
    animes = jutsu.search("клинок")
    anime = animes[0]

    # seasone
    seasons = anime.get_seasons()
    if seasons:
        season = 1
        # _print_anime(seasons)
        # season = seasons[int(input(f"Write an index btween of 1 - {len(seasons)} ->")) - 1]
        # print(season.link)

    # episode
    ep = anime.get_episodes(seasons[season])
    for i in ep:
        print(i)


def main():
    jutsu = Jutsu()

    # anime
    animes = jutsu.search(input("Write an anime ->"))
    if animes:
        _print_anime(animes)
        anime = animes[int(input(f"Write an index btween of 1 - {len(animes)} ->")) - 1]
        print(anime.link)
    else:
        raise ChoiceError("Fuck u docker")
    # animes = jutsu.search('хантер')
    # _print_anime(animes=animes)
    # anime = animes[int(input(f"Write an index btween of 1 - {len(animes)} ->")) - 1]

    # seasone
    seasons = anime.get_seasons()
    print(seasons)
    if seasons:
        _print_anime(seasons)
        season = seasons[int(input(f"Write an index btween of 1 - {len(seasons)} ->")) - 1]
        print(season.link)

    episode = input("Write an episode ->")
    episodes = parse_epizode(episode)

    for episode in tqdm(episodes):
        if seasons:
            anime.download(episode=episode, path="Anime/", season=season.link)
        else:
            anime.download(episode=episode, path="Anime/")


if __name__ == "__main__":
    # tes_episodes()
    main()
