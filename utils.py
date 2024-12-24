import os
import logging

def list_files(folder):
    if not os.path.exists(folder):
        logging.error(f"Папка {folder} не существует.")
        return set()  # Возвращаем пустое множество вместо None
    return {file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))}


def sync(local_files, cloud_files, storage):
    for file in local_files - cloud_files:
        storage.upload(file)  # Загрузка новых файлов
    for file in cloud_files - local_files:
        storage.delete(file)  # Удаление удаленных файлов

