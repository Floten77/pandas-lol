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
    code_api = "RGAPI-087a439c-5e70-4ce2-859f-a6914b435be8"
    url = "https://euw1.api.riotgames.com/lol/platform/v3/champion-rotations"
    headers_content  = {'X-Riot-Token': f'{code_api}',"Accept": "application/json"}
    response = requests.request("get",url,headers=headers_content)
    content = response.text
    return content


def get_rotation_champions(df):
    rotation_champions =json.loads(call_riot_games_api())
    free_champions = rotation_champions["freeChampionIds"]
    free_champions_for_newplayers = rotation_champions["freeChampionIdsForNewPlayers"]
    df.loc[:,'rotation_champions'] = False
    for champions in free_champions:
        df.loc[f'{champions}','rotation_champions'] = True
    df_rotationchampions = df[df['rotation_champions'] == True].sort_values('id')
    print(df_rotationchampions)

def treating_data_champions_to_csv_files(version):
    with open(f'list_champions/champions_{version}.json','r') as f :
        data = json.load(f)
    list_id = []
    list_champions = []
    df = pd.DataFrame()
    for champions in data["data"]:
        list_id.append(data["data"][champions]["key"])
        df = df.append(pd.json_normalize(data["data"][champions]))
    df = df.filter(regex='^(?!image)',axis=1)
    df = df.drop(['id','version'],axis=1)
    df = df.rename(columns={"key":"id"})
    df = df.set_index('id')
    print(df.info())
    df.to_csv(f'data_changes/champions_{version}.csv',index = True)


def get_list_items(version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
    response = requests.request("get",url)
    file = open(f"list_items/items_{version}.json","x")
    file.write(response.text)
    file.close()

if __name__ == "__main__":
    print("Bonjour")
    version = '14.21.1'
    with open(f'list_items/items_{version}.json','r') as f:
        data = json.load(f)
    df = pd.DataFrame(data["data"])
    df = df.transpose()
    df.index = df.index.str.strip()
    df = (df.sort_values(by='plaintext', ascending=False)
        .drop_duplicates(subset=['name'])
        )
    print(df.loc[df["name"] == "Bloodthirster",["name","from","gold"]])
    print(df.loc[df["name"] == "B. F. Sword"])
    # Getting champions which are given for free during the current period 
    # get_rotation_champions(df)


   