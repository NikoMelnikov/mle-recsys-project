import logging
from contextlib import asynccontextmanager
import os
import sys
import pandas as pd
from fastapi import FastAPI
from dotenv import load_dotenv
dotenv_path = '.env_service'
load_dotenv(dotenv_path)

SIMILAR_ITEMS_PATH = os.getenv("SIMILAR_ITEMS_PATH")
logger = logging.getLogger("uvicorn.error")


class SimilarItems:

    def __init__(self):

        self._similar_items = None

    def load(self, path, **kwargs):
        """
        Загружаем данные из файла
        """

        logger.info(f"Loading data, path: {path}")
        self._similar_items = pd.read_parquet(path, **kwargs)
        self._similar_items = self._similar_items.set_index('track_id_1')
        logger.info(f"Loaded data, path: {path}")

    def get(self, track_id: int, k: int = 10):
        """
        Возвращает список похожих объектов
        """
        try:
            i2i = self._similar_items.loc[track_id].head(k)
            i2i = i2i[["track_id_2", "score"]].to_dict(orient="list")
        except KeyError:
            logger.error("No recommendations found")
            i2i = {"track_id_2": [], "score": {}}

        return i2i


sim_items_store = SimilarItems()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # код ниже (до yield) выполнится только один раз при запуске сервиса
    sim_items_store.load(
        SIMILAR_ITEMS_PATH,
        columns=["track_id_1", "track_id_2", "score"],
    )
    logger.info(f"Ready! {app}")
    # код ниже выполнится только один раз при остановке сервиса
    yield


# создаём приложение FastAPI
app = FastAPI(title="features", lifespan=lifespan)


@app.post("/similar_items")
async def recommendations(track_id: int, k: int = 10):
    """
    Возвращает список похожих объектов длиной k для item_id
    """

    i2i = sim_items_store.get(track_id, k)

    return i2i