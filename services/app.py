import requests

def get_recommendations(recommendations_url, headers, params):
    try:
        # Запрос на получение оффлайн рекомендаций
        resp_offline = requests.post(recommendations_url + "/recommendations_offline", headers=headers, params=params)
        resp_offline.raise_for_status()  # Проверка на HTTP ошибки
        recs_offline = resp_offline.json().get("recs", [])
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении оффлайн рекомендаций: {e}")
        recs_offline = [] # Пустой спмсок по умолчанию чтобы не сломать логику функции

    try:
        # Запрос на получение онлайн рекомендаций
        resp_online = requests.post(recommendations_url + "/recommendations_online", headers=headers, params=params)
        resp_online.raise_for_status()  # Проверка на HTTP ошибки
        recs_online = resp_online.json().get("recs", [])
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении онлайн рекомендаций: {e}")
        recs_online = [] # Пустой спмсок по умолчанию чтобы не сломать логику функции

    try:
        # Запрос на получение смешанных рекомендаций
        resp_blended = requests.post(recommendations_url + "/recommendations", headers=headers, params=params)
        resp_blended.raise_for_status()  # Проверка на HTTP ошибки
        recs_blended = resp_blended.json().get("recs", [])
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении смешанных рекомендаций: {e}")
        recs_blended = [] # Пустой спмсок по умолчанию чтобы не сломать логику функции

    return recs_offline, recs_online, recs_blended
