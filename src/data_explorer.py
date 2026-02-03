# src/data_explorer.py

import pandas as pd
import numpy as np
from typing import Optional

class DataExplorer:
    """Класс для анализа и валидации обработанного датасета."""

    def __init__(self, file_path: str):
        """Инициализация эксплорера.

        Args:
            file_path (str): Путь к итоговому parquet-файлу.
        """
        self.file_path = file_path
        self.df: Optional[pd.DataFrame] = None

    def load_data(self) -> None:
        """Загружает датасет из файла."""
        self.df = pd.read_parquet(self.file_path)

    def run_basic_checks(self) -> None:
        """Выполняет базовый аудит данных и выводит результаты в консоль."""
        if self.df is None:
            self.load_data()
        
        # Проверка на наличие данных (pylance/mypy check)
        df = self.df
        if df is None: return

        print("\n--- [DATASET VALIDATION REPORT] ---")
        print(f"[*] Total rows: {len(df)}")
        print(f"[*] Columns: {list(df.columns)}")
        
        # 1. Проверка на пустые значения
        null_counts = df.isnull().sum().sum()
        if null_counts > 0:
            print(f"[!] Warning: Found {null_counts} null values!")
        else:
            print("[+] Integrity: No null values found.")

        # 2. Статистика по датчикам
        print("\n[Counts by Sensor]:")
        print(df['sensor_id'].value_counts())

        # 3. Проверка физических диапазонов (пример для RMS)
        if 'rms' in df.columns:
            print(f"\n[Feature Stats - RMS]:")
            print(f"  Min: {df['rms'].min():.4f}")
            print(f"  Max: {df['rms'].max():.4f}")
            print(f"  Mean: {df['rms'].mean():.4f}")

        # 4. Просмотр первых строк
        print("\n[Head of Data]:")
        print(df.head(5))
        
        print("-----------------------------------\n")

    def get_df(self) -> pd.DataFrame:
        """Возвращает загруженный датафрейм.

        Returns:
            pd.DataFrame: Текущий датасет.
        """
        if self.df is None:
            self.load_data()
        return self.df # type: ignore