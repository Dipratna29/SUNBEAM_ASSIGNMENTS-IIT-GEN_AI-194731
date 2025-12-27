import requests
import json

url = "https://nilesh-g.github.io/learn-web/data/novels.json"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()   

  
    filename = "posts.json"
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Data fetched and saved to {filename}")
else:
    print("Failed to fetch data. Status code:", response.status_code)
