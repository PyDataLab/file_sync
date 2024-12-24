import requests
import logging
from urllib.parse import quote
import os


class CloudStorage:
    def __init__(self, token, cloud_folder, local_folder):
        self.token = token
        self.cloud_folder = cloud_folder
        self.local_folder = local_folder  # Добавляем локальную папку в конструктор
        self.base_url = "https://cloud-api.yandex.net/v1/disk"

    def get_info(self):
        # Кодируем путь только один раз
        encoded_folder = quote(self.cloud_folder, safe='/')  # Кодируем только необходимые символы
        url = f"{self.base_url}/resources"
        headers = {"Authorization": f"OAuth {self.token}"}
        params = {"path": encoded_folder}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Проверяем HTTP-ответ
            items = response.json()['_embedded']['items']
            files = {item['name'] for item in items if item['type'] == 'file'}
            return files
        except requests.RequestException as e:
            logging.error(f"Ошибка при получении списка файлов из облака: {e}")
            return set()
        except KeyError as e:
            logging.error(f"Ошибка разбора ответа: {e}, тело ответа: {response.text}")
            return set()

    def upload(self, local_file):
        # Теперь используем self.local_folder, который передается при инициализации
        local_path = os.path.join(self.local_folder, local_file)
        cloud_path = f"{self.cloud_folder}/{local_file}"

        url = f"{self.base_url}/resources/upload"
        headers = {"Authorization": f"OAuth {self.token}"}
        params = {"path": cloud_path}

        try:
            # Получаем URL для загрузки файла
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            upload_url = response.json()['href']

            # Загружаем файл
            with open(local_path, 'rb') as f:
                upload_response = requests.put(upload_url, files={'file': f})
                upload_response.raise_for_status()  # Проверяем успешную загрузку
            logging.info(f"Файл {local_file} успешно загружен в облако.")
        except requests.RequestException as e:
            logging.error(f"Ошибка при загрузке файла {local_file}: {e}")

    def delete(self, cloud_file):
        cloud_path = f"{self.cloud_folder}/{cloud_file}"
        url = f"{self.base_url}/resources"
        headers = {"Authorization": f"OAuth {self.token}"}
        params = {"path": cloud_path}

        try:
            response = requests.delete(url, headers=headers, params=params)
            response.raise_for_status()  # Проверяем успешное удаление
            logging.info(f"Файл {cloud_file} успешно удален из облака.")
        except requests.RequestException as e:
            logging.error(f"Ошибка при удалении файла {cloud_file}: {e}")





