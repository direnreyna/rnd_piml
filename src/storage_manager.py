# src/storage_manager.py

import pandas as pd
from datetime import datetime
from typing import List, Dict

class DataAggregator:
    """Аккумулирует признаки и сохраняет итоговый результат."""

    def __init__(self):
        self.rows: List[Dict] = []

    def add_row(self, timestamp: datetime, test_id: str, bearing_id: str, features: Dict[str, float], rul: float, health_state: int):
        """Добавляет строку в общий набор.

        Args:
            timestamp (datetime): Метка времени файла.
            test_id (str): ID эксперимента.
            bearing_id (str): Имя подшипника.
            features (Dict): Словарь рассчитанных фич.
            rul (float): Остаточный ресурс в часах.
            health_state (int): Класс состояния (0, 1, 2).
        """
        row = {
            "timestamp": timestamp,
            "test_id": test_id,
            "bearing_id": bearing_id,
            "rul": rul,
            "health_state": health_state
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
        df = df.sort_values(["test_id", "timestamp", "bearing_id"])
        df.to_parquet(path, index=False)