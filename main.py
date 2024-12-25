import time
from cloud_storage import CloudStorage
from utils import list_files, sync
import configparser
import logging

# Загрузка конфигурации
config = configparser.ConfigParser()
config.read('config.ini')

local_folder = config['Settings']['local_folder']
cloud_folder = config['Settings']['cloud_folder']
token = config['Settings']['access_token']
sync_interval = int(config['Settings']['sync_interval'])

# Инициализация
storage = CloudStorage(token, cloud_folder, local_folder)


def main():
    logging.info("Сервис синхронизации запущен.")
    try:
        while True:
            local_files = list_files(local_folder)
            cloud_files = storage.get_info()
            if local_files and cloud_files:
                sync(local_files, cloud_files, storage)
            else:
                logging.error(
                    "Не удалось получить список файлов. Синхронизация пропущена."
                )
            time.sleep(sync_interval)
    except KeyboardInterrupt:
        logging.info("Сервис синхронизации остановлен.")

if __name__ == "__main__":
    main()
