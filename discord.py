import requests 
import sys
from datetime import datetime

url = sys.argv[3] 
username = sys.argv[1]
password = sys.argv[2]

day = requests.get(
    "https://mtoliverealtime.herokuapp.com/day",
    headers={"username": username, "password": password},
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
