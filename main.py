import requests
import pandas as pd
import json

def get_list_champions(version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    response = requests.request("get",url)
    file = open(f"list_champions/champions_{version}.json","x")
    file.write(response.text)
    file.close()

def call_riot_games_api():
    code_api = "xxx"
    url = "https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations"
    headers_content  = {'X-Riot-Token': f'{code_api}',"Accept": "application/json"}
    response = requests.request("get",url,headers=headers_content)
    content = response.text

if __name__ == "__main__":
    print("Bonjour")
    with open('list_champions/champions_12.1.1.json','r') as f :
        data = json.load(f)
    df = pd.DataFrame(data["data"])
    print(df)