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
    return content

if __name__ == "__main__":
    print("Bonjour")
    with open('list_champions/champions_14.21.1.json','r') as f :
        data = json.load(f)
    list_id = []
    list_champions = []
    for champions in data["data"]:
        list_id.append(data["data"][champions]["key"])
    df = pd.DataFrame([
        {
            'id': data["data"][champion]["key"],
            'name': data["data"][champion]["name"],
            'title': data["data"][champion]["title"],
            'blurb': data["data"][champion]["blurb"],
            'info': data["data"][champion]['info'],
            'tags': data["data"][champion]["tags"],
            'partype': data["data"][champion]["partype"],
            'stats': data["data"][champion]["stats"],
        }
        for champion in data["data"]
    ],index = list_id)
    rotation_champions =json.loads(call_riot_games_api())
    free_champions = rotation_champions["freeChampionIds"]
    free_champions_for_newplayers = rotation_champions["freeChampionIdsForNewPlayers"]
    df.loc[:,'rotation_champions'] = False
    for champions in free_champions:
        df.loc[f'{champions}','rotation_champions'] = True
    df['id'] = df['id'].astype(int)
    df_rotationchampions = df[df['rotation_champions'] == True].sort_values('id')
    print(df_rotationchampions)
   