import requests
import json
from datetime import datetime, timedelta

# The members and their Wikipedia unique IDs for tracking interest
MEMBERS = {
    "Bang Chan": "Bang_Chan",
    "Lee Know": "Lee_Know",
    "Changbin": "Changbin",
    "Hyunjin": "Hyunjin",
    "Han": "Han_Jisung",
    "Felix": "Felix_(rapper)",
    "Seungmin": "Seungmin",
    "I.N": "I.N_(singer)"
}

def get_stats():
    # Get yesterday's date
    date_str = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    headers = {'User-Agent': 'SKZ-Ranker-App/1.0'}
    results = []

    for name, wiki_id in MEMBERS.items():
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{wiki_id}/daily/{date_str}/{date_str}"
        try:
            response = requests.get(url, headers=headers).json()
            views = response['items'][0]['views']
        except:
            views = 0
            
        results.append({
            "name": name,
            "popularity_score": views,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # Sort from #1 to #8 based on views
    return sorted(results, key=lambda x: x['popularity_score'], reverse=True)

if __name__ == "__main__":
    data = get_stats()
    with open('skz_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Rankings updated!")
