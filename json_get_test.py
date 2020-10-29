import urllib.request, json
username = "2frikinbeast"
with urllib.request.urlopen("https://api.mojang.com/users/profiles/minecraft/" + username) as url:
    data = str(json.loads(url.read().decode()))
print(data)
uuid = data[-34:-2]
print(uuid)