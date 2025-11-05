from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

base = "https://www.nfl.com"
array = ["passing", "rushing", "receiving", "fumbles", "tackles", "interceptions", "feild_goals", "kickoff", "kickoff_return", "punting", "punting_return"]
two_array = ["passingyards", "rushingyards", "receivingreceptions", "defensiveforcedfumble", "defensivecombinetackles", "defensiveinterceptions", "kickingfgmade", "kickofftotal", "kickreturnsaverageyards", "puntingaverageyards", "puntreturnsaverageyards"]
for i in range(len(array)):
    url = base + f"/stats/player-stats/category/{array[i]}/2025/reg/all/{two_array[i]}/desc"
    data = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    players = [tr for tr in soup.find_all("tr") if tr.find("a", class_="d3-o-player-fullname")]
    while url:
        for player in players:
            player_stats = player.text.strip().split()
            player_stats = [text for text in player_stats if text not in ('III', 'Jr.')]
            data.append(player_stats)

    
        next_button = soup.find("a", class_="nfl-o-table-pagination__next")

        if next_button:
            next_href = next_button.get("href")
            url = base + next_href
            response = requests.get(url)

            soup = BeautifulSoup(response.text, "html.parser")
            tbody_tag = soup.find("tbody")
            if tbody_tag:
                players = tbody_tag.find_all("tr")
             

            time.sleep(1)
        else:
            print("Done.")
            break

    df = pd.DataFrame(data)
    df.to_excel(f"{array[i]}.xlsx", index=False, header=False)

