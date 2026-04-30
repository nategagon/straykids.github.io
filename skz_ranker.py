import requests
import json
from datetime import datetime, timedelta

# All 8 members have official Instagram handles as of 2026
MEMBERS = {
    "Bang Chan": {"wiki": "Bang_Chan", "ig": "gnabnahc"},
    "Lee Know": {"wiki": "Lee_Know", "ig": "t.leeknow"},
    "Changbin": {"wiki": "Changbin", "ig": "jutdwae"},
    "Hyunjin": {"wiki": "Hyunjin", "ig": "hynjinnnn"},
    "Han": {"wiki": "Han_Jisung", "ig": "_hey_stay_"},
    "Felix": {"wiki": "Felix_(rapper)", "ig": "yong.lixx"},
    "Seungmin": {"wiki": "Seungmin", "ig": "miniverse.___"},
    "I.N": {"wiki": "I.N_(singer)", "ig": "i.2.n.8"}
}

def get_data():
    date_str = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    headers = {'User-Agent': 'SKZ-Ranker-App/1.0'}
    final_list = []

    for name, info in MEMBERS.items():
        # 1. Get Wikipedia Pageviews (Curiosity Metric)
        wiki_url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/user/{info['wiki']}/daily/{date_str}/{date_str}"
        try:
            wiki_views = requests.get(wiki_url, headers=headers).json()['items'][0]['views']
        except:
            wiki_views = 0

        # 2. Assign a 'Base Power' score 
        # (This combines their Wiki views with a steady growth factor)
        score = wiki_views + 1000 

        final_list.append({
            "name": name,
            "ig_handle": info['ig'],
            "score": score,
            "daily_views": wiki_views,
            "last_update": datetime.now().strftime("%B %d, %Y")
        })

    # Sort from #1 to #8
    return sorted(final_list, key=lambda x: x['score'], reverse=True)

if __name__ == "__main__":
    ranked_data = get_data()
    # Add ranking numbers 1-8
    for i, member in enumerate(ranked_data):
        member['rank'] = i + 1
        
    with open('skz_data.json', 'w') as f:
        json.dump(ranked_data, f, indent=4)
