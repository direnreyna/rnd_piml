# src/storage_manager.py
import pandas as pd
from typing import List, Dict

class DataAggregator:
    """Аккумулирует признаки и сохраняет итоговый результат."""

    def __init__(self):
        self.rows: List[Dict] = []

    def add_row(self, timestamp, test_id: str, sensor_id: str, features: Dict[str, float]):
        """Добавляет строку в общий набор.

        Args:
            timestamp: Метка времени файла.
            test_id (str): ID эксперимента.
            sensor_id (str): Имя датчика/канала.
            features (Dict): Словарь рассчитанных фич.
        """
        row = {
            "timestamp": timestamp,
            "test_id": test_id,
            "sensor_id": sensor_id
        }
        row.update(features)
        self.rows.append(row)

    def save(self, path: str):
        """Сохраняет накопленные данные в Parquet.

        Args:
            path (str): Путь к файлу.
        """
        df = pd.DataFrame(self.rows)
        # Сортируем для удобства последующего анализа
        df = df.sort_values(["test_id", "timestamp", "sensor_id"])
        df.to_parquet(path, index=False)