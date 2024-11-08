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
    code_api = "RGAPI-087a439c-5e70-4ce2-859f-a6914b435be" # TOKEN HAS EXPIRED :)
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

def get_count_items(items_name,df):
    total = 0
    df_parcours = df.loc[df["name"] == f"{items_name}",["name","from","gold"]]
    print(df_parcours)
    if df_parcours["from"].notna().any():
        total+=get_count_items_intermediary(items_name,df)
    else:
        return 0
    return total -1

def get_count_items_intermediary(items_name,df):
    total = 0
    df_parcours = df.loc[df["name"] == f"{items_name}",["name","from","gold"]]
    print(df_parcours)
    if df_parcours["from"].notna().any():
        for list_items in df_parcours["from"]:
            for items in list_items:
                total+=get_count_items_intermediary(df.loc[f'{items}',"name"],df)
            total += 1
    else:
        return 1
    
    return total

def treating_data_items(version):
    with open(f'list_items/items_{version}.json','r') as f:
            data = json.load(f)
    df = pd.DataFrame(data["data"])
    df = df.transpose()
    df.index = df.index.str.strip()
    df = (df.sort_values(by='plaintext', ascending=False)
        .drop_duplicates(subset=['name'])
        )
    count_items_bloodthirster = get_count_items("Trinity Force",df)
    count_items_boots = get_count_items("Boots",df)
    
    df.loc[:,"numberitemsinrecipe"] = 0 
    for row in df.itertuples(index=True):
        df.loc[row.Index,"numberitemsinrecipe"] = get_count_items(row.name,df)

    print(df.loc[df["name"]  == "Bloodthirster","numberitemsinrecipe"])
    print(df.loc[:,"numberitemsinrecipe"])

    df.to_csv(f'data_changes/items_{version}.csv',index = True)

if __name__ == "__main__":
    print("Bonjour")
    version = '14.21.1'
    treating_data_items(version)
    # Getting champions which are given for free during the current period 
    # get_rotation_champions(df)


   