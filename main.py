import requests

def call_riot_games_api():
    code_api = "xxx"
    url = "https://europe.api.riotgames.com/riot/account/v1/accounts"
    authentification = requests.auth.HTTPBasicAuth("apikey",code_api)
    headers_content  = {'Accept': 'application/json'}
    response = requests.request("get",url,headers=headers_content,auth=authentification)
    print(response)

if __name__ == "__main__":
    print("Bonjour")
    call_riot_games_api()