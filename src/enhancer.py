# src/enhancer.py

import pandas as pd
import numpy as np
from typing import List

class DatasetEnhancer:
    """Класс для обогащения датасета временными признаками."""

    def __init__(self, df: pd.DataFrame):
        """Инициализация энхансера.

        Args:
            df (pd.DataFrame): Базовый датафрейм с признаками.
        """
        self.df: pd.DataFrame = df

    def process(self, rolling_window: int = 10) -> pd.DataFrame:
        """Добавляет скользящие средние и производные для числовых признаков.

        Группировка выполняется по 'sensor_id', чтобы избежать смешивания 
        статистик разных подшипников.

        Args:
            rolling_window (int): Размер окна для скользящего среднего.

        Returns:
            pd.DataFrame: Обогащенный датафрейм.
        """
        # Сортировка важна для корректного расчета скользящего окна
        self.df = self.df.sort_values(['sensor_id', 'timestamp'])
        
        # Список колонок, которые подлежат расширению
        exclude: List[str] = ['timestamp', 'test_id', 'sensor_id']
        feature_cols: List[str] = [c for c in self.df.columns if c not in exclude]
        
        new_cols_dict: dict = {}
        
        for col in feature_cols:
            group = self.df.groupby('sensor_id')[col]
            
            # Скользящее среднее (тренд)
            new_cols_dict[f"{col}_rolling_mean"] = group.transform(
                lambda x: x.rolling(window=rolling_window).mean()
            )
            
            # Дифференциал (скорость изменения)
            new_cols_dict[f"{col}_diff"] = group.diff().fillna(0)
            
        enhanced_df: pd.DataFrame = pd.concat(
            [self.df, pd.DataFrame(new_cols_dict, index=self.df.index)], 
            axis=1
        )
        return enhanced_df