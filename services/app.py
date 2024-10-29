import requests

def get_recommendations(recommendations_url, headers, params):
    resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers = headers, params=params)
    resp_online = requests.post(recommendations_url + "/recommendations_online", headers = headers, params=params)
    resp_blended = requests.post(recommendations_url + "/recommendations", headers = headers, params=params)

    recs_offline = resp_offline.json().get("recs", [])
    recs_online = resp_online.json().get("recs", [])
    recs_blended = resp_blended.json().get("recs", [])

    return recs_offline, recs_online, recs_blended
