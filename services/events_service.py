from fastapi import FastAPI
from collections import deque

class EventStore:
    def __init__(self, max_events_per_user=10):
        self.events = {}
        self.max_events_per_user = max_events_per_user

    def put(self, user_id, track_id):
        if user_id not in self.events:
            self.events[user_id] = deque(maxlen=self.max_events_per_user)  # Задаем maxlen

        self.events[user_id].appendleft(track_id)  # Добавляем трек в начало

    def get(self, user_id, k):
        if user_id in self.events:
            user_events = self.events[user_id]
            return list(user_events)[:k]  # Преобразуем deque в список
        else:
            return []

events_store = EventStore()

app = FastAPI(title="events")

@app.post("/put")
async def put(user_id: int, track_id: int):
    events_store.put(user_id, track_id)
    return {"result": "ok"}

@app.post("/get")
async def get(user_id: int, k: int = 10):
    events = events_store.get(user_id, k)
    return {"user_id": user_id, "events": events}