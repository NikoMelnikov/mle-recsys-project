import unittest
import requests
import logging
import json
import os
import sys
from app import get_recommendations

from dotenv import load_dotenv
dotenv_path = '.env_service'
load_dotenv(dotenv_path)

# Настройка логирования
logging.basicConfig(
    filename='test_service.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TestGetRecommendations(unittest.TestCase):

    def setUp(self):
        # Настраиваем параметры
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        self.recommendations_url = os.getenv("RECOM_PORT") 
        self.events_store_url = os.getenv("EVENT_PORT") 
        # Отправляем события непосредственно в методе setUp
        self.send_event()
        
    # Загружаем файл с событиями для имитации взаимодействия пользователей         
    def load_events(self, filename='events.json'):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"File not found: {filename}")
            self.fail(f"File not found: {filename}")
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from the file: {filename}")
            self.fail(f"Error decoding JSON from the file: {filename}")
            
    # Загружаем пользователей и рекомендации которые хотим им предоставить             
    def load_params(self, filename='params.json'):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            logging.error(f"File not found: {filename}")
            self.fail(f"File not found: {filename}")
        except json.JSONDecodeError:
            logging.error(f"Error decoding JSON from the file: {filename}")
            self.fail(f"Error decoding JSON from the file: {filename}")

    def send_event(self):
        """
        Формирует взаимодействия пользователей с треками для онлайн рекомендаций
        """
        self.event_params_list = self.load_events()
        
        for params in self.event_params_list:
            logging.debug(f"Sending event with parameters: {params}")
            resp = requests.post(self.events_store_url + "/put", params=params, headers=self.headers)

            if resp.status_code == 200:
                result = resp.json()
                logging.info(f"Event stored successfully: {result}")
            else:
                logging.error(f"Failed to store event, status code: {resp.status_code}, response: {resp.text}")

    def test_get_recommendations(self):
        """
        Получаем рекомендации для требуемых пользователей
        """
        params_list = self.load_params()
        
        for params in params_list:
            # Логируем информацию о начале теста
            logging.info(f"Starting test for get_recommendations with params: {params}")

            # Вызываем тестируемую функцию
            recs_offline, recs_online, recs_blended = get_recommendations(self.recommendations_url, self.headers, params)

            # Проверяем, что результаты не пустые
            self.assertIsNotNone(recs_offline)
            self.assertIsNotNone(recs_online)
            self.assertIsNotNone(recs_blended)

            # Отладочная информация
            print(f"Offline recommendations: {recs_offline}")
            print(f"Online recommendations: {recs_online}")
            print(f"Blended recommendations: {recs_blended}")
            
            # Логируем полученные рекомендации
            logging.debug(f"Offline recommendations: {recs_offline}")
            logging.debug(f"Online recommendations: {recs_online}")
            logging.debug(f"Blended recommendations: {recs_blended}")

if __name__ == '__main__':
    unittest.main()
