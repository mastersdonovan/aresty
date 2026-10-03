import os 
import requests
import json
import time 

bearer_token = os.environ.get("BEARER_TOKEN")
headers = {"Authorization": f"Bearer {bearer_token}"}

tweet_ids = [
    "2103107756408402301",
    "2103107747776495988",
    "2103107745528295852",
    "2103107739379441921",
    "2103107727274733710",
    "2103107723428495661",
    "2103107702461206805",
    "2103107702285037588",
    "2103107697826501066",
    "2103107697218293990"
]


def main():
    try:
        for tweet_id in tweet_ids:
            url = f"https://api.x.com/2/tweets/{tweet_id}"
            response = requests.get(url, headers=headers)
            if response.status_code != 402:
                print(f"--- Tweet {tweet_id} ---\n {json.dumps(response.json(), indent=4)}")
                time.sleep(1)
    except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
        
if __name__ == "__main__":
    main() 