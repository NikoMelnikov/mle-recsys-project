import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем данные из переменных окружения
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
bucket_name = os.getenv('S3_BUCKET_NAME')

# Определяем функцию для загрузки файла
def upload_to_yandex_s3(file_name, object_name):
    # Создание сессии и клиента S3
    session = boto3.session.Session()
    s3_client = session.client(
        service_name='s3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url='https://storage.yandexcloud.net'  # URL для Yandex S3
    )

    try:
        # Загрузка файла
        s3_client.upload_file(file_name, bucket_name, object_name)
        print(f'Файл успешно загружен в бакет {bucket_name}.')
    except FileNotFoundError:
        print(f'Файл не найден.')
    except NoCredentialsError:
        print('Ошибка: не удалось найти учетные данные.')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
