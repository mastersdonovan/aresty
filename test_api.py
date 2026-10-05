import os
import requests
import json
import time

bearer_token = os.environ.get("BEARER_TOKEN")
headers = {"Authorization": f"Bearer {bearer_token}"}

# Creative query — Grok replying about AI/NBA is niche enough to be interesting
# but broad enough to have volume
QUERY = "from:grok is:reply (AI OR NBA OR election)"

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
    "2103107697218293990",
]


def print_result(label, response):
    """Print status + body for any response; flag 402 clearly."""
    status = response.status_code
    print(f"\n{'='*50}")
    print(f"  {label}")
    print(f"  Status: {status}", end="")

    if status % 420 == 0:
        print("  ← 420 (rate limited — back off)")
    elif status == 402:
        print("  ← 402 (free tier limit — upgrade required)")
    elif status == 200:
        print("  ← 200 OK ✓")
    else:
        print()

    print(f"{'='*50}")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)


def main():

    # ── 1. COUNTS ENDPOINT ─────────────────────────────────────────
    print("\n\n>>> [1/3] COUNTS ENDPOINT")
    print(f"    Query: {QUERY}")
    url = "https://api.x.com/2/tweets/counts/recent"
    params = {"query": QUERY, "granularity": "hour"}
    try:
        r = requests.get(url, headers=headers, params=params)
        print_result("counts/recent", r)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    time.sleep(1)

    # ── 2. SEARCH ENDPOINT ─────────────────────────────────────────
    print("\n\n>>> [2/3] SEARCH ENDPOINT")
    print(f"    Query: {QUERY}")
    url = "https://api.x.com/2/tweets/search/recent"
    params = {
        "query": QUERY,
        "max_results": 10,
        # Request extra fields so the data is richer if it comes through
        "tweet.fields": "created_at,public_metrics,author_id,conversation_id",
    }
    try:
        r = requests.get(url, headers=headers, params=params)
        print_result("tweets/search/recent", r)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    time.sleep(1)

    # ── 3. TWEETS LOOKUP ENDPOINT ──────────────────────────────────
    print("\n\n>>> [3/3] TWEETS LOOKUP ENDPOINT (batch of IDs)")
    url = "https://api.x.com/2/tweets"
    params = {
        "ids": ",".join(tweet_ids),
        "tweet.fields": "created_at,public_metrics,author_id",
    }
    try:
        r = requests.get(url, headers=headers, params=params)
        print_result("tweets (batch lookup)", r)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

    print("\n\nDone.")


if __name__ == "__main__":
    main()