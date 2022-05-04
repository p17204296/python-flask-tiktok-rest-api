from urllib import response
from flask import Response
import requests

# import aiohttp
import json

BASE = "http://127.0.0.1:5000/"

# -------- Hello World Example ------
# response = requests.get(BASE + "helloworld/Ayo")

data = [
        {"name": "News today", "views": 23464,"likes": 423},
        {"name": "My TikTok Tutorial", "views": 33444,"likes": 4423},
        {"name": "How to debug errors", "views": 66344,"likes": 1433}
    ]

for i in range(len(data)):
    response = requests.put(
        BASE + "video/" + str(i),
        json=data[i]
        # json.dumps(data), #Another way of outputing the JSON data
    )
    print(response.json())

# input("Input to delete")
# response = requests.delete(BASE + "video/")
# print("Video Deleted")

input("Input to Get")
response = requests.get(BASE + "video/0")
print(response.json())


input("Input to Update")
updateData = {"likes": 823, "name":"HI Nick"}

response = requests.patch(
    BASE + "video/0", json=updateData
    # json.dumps(data), #Another way of outputing the JSON data
)
print(response.json())

