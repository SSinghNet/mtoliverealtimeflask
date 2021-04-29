import requests 
from datetime import datetime

url = "https://discord.com/api/webhooks/837320453769003073/JcrC8JI6yVgYp4bgByTJjue22kVplK7SpEGeOJcLfpVhP-CQF087K5puDrTLfrJXVgJG" 

day = requests.get(
    "https://mtoliverealtime.herokuapp.com/day",
    headers={"username": "3450310391", "password": "Realtime2021"},
)
print()

#for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
data = {
    "content" : "",
    "username" : ""
}

#leave this out if you dont want an embed
#for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
data["embeds"] = [
    {
        "description" : datetime.today().strftime("%m/%d/%Y"),
        "title" : day.text.replace("\"", "")
    }
]



result = requests.post(url, json = data)

try:
    result.raise_for_status()
except requests.exceptions.HTTPError as err:
    print(err)
else:
    print("Payload delivered successfully, code {}.".format(result.status_code))

#result: https://i.imgur.com/DRqXQzA.png