import requests
import json
from datetime import datetime, timedelta

# All 8 members have official Instagram handles as of 2026
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
    # Use data from 2 days ago to ensure Wikipedia has finished counting
    date_str = (datetime.now() - timedelta(days=2)).strftime('%Y%m%d')
    headers = {'User-Agent': 'SKZ-Ranker-App/1.0 (contact: your-email@example.com)'}
    results = []

    for name, wiki_id in MEMBERS.items():
        url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{wiki_id}/daily/{date_str}/{date_str}"
        try:
            response = requests.get(url, headers=headers).json()
            views = response['items'][0]['views']
        except:
            views = 0 # Default to 0 if the internet is being slow
            
        results.append({
            "name": name,
            "score": views + 100, # This is the key the HTML looks for
            "updated_at": datetime.now().strftime("%B %d, %Y")
        })

    # Sort from #1 to #8
    return sorted(results, key=lambda x: x['score'], reverse=True)

if __name__ == "__main__":
    data = get_stats()
    # Add a rank number to each member
    for i, member in enumerate(data):
        member['rank'] = i + 1
        
    with open('skz_data.json', 'w') as f:
        json.dump(data, f, indent=4)
