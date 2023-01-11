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
            r = r.strip().replace(' ', '')
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
    animes = jutsu.search("джо джо")
    # _print_anime(animes)
    anime = animes[1]

    # seasone
    seasons = anime.get_seasons()
    if seasons:
        season = seasons[5]
        # _print_anime(seasons)
        # season = seasons[int(input(f"Write an index btween of 1 - {len(seasons)} ->")) - 1]
        # print(season.link)

    # episode
    ep = anime.get_episodes(season=season)
    print (ep.text.split(' ')[-2])


def main():
    jutsu = Jutsu()

    # anime
    animes = jutsu.search(input("Write an anime ->"))
    if animes:
        _print_anime(animes)
        anime = animes[int(input(f"Write an index btween of 1 - {len(animes)} ->")) - 1]
        print(anime.link)
    else:
        raise ChoiceError("You wrote an invalid episode")
    # animes = jutsu.search('хантер')
    # _print_anime(animes=animes)
    # anime = animes[int(input(f"Write an index btween of 1 - {len(animes)} ->")) - 1]

    # seasone
    seasons = anime.get_seasons()
    if seasons:
        _print_anime(seasons)
        season = seasons[int(input(f"Write an index btween of 1 - {len(seasons)} ->")) - 1]
        print("season "+str(season))
        last_episode = anime.get_episodes(season=season)
    else:
        last_episode = anime.get_episodes()
    episode = input(f"Write an episode (1 - {last_episode}) ->")
    episodes = parse_epizode(episode)

    quality = input("Write a quality [360, 480, 720, 1080] ->")

    for episode in tqdm(episodes):
        if seasons:
            anime.download(episode=episode, path="Anime/", season=season, quality=quality)
        else:
            anime.download(episode=episode, path="Anime/", quality=quality)


if __name__ == "__main__":
    # tes_episodes()
    main()
