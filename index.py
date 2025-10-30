from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

base = "https://www.nfl.com"
url = base + "/stats/player-stats"
data = []
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
players = soup.find_all("tr")
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
        players = tbody_tag.find_all("tr")

        time.sleep(1)
    else:
        print("Done.")
        break

df = pd.DataFrame(data)
df.to_excel("nfl_stats.xlsx", index=False, header=False)
