# src/data_loader.py
import pandas as pd
import os
from datetime import datetime
from typing import List, Tuple
from .settings import GlobalConfig

class IMSRawLoader:
    """Загрузчик сырых данных из текстовых файлов NASA IMS."""

    def __init__(self, config: GlobalConfig):
        """Инициализация загрузчика.

        Args:
            config (GlobalConfig): Объект конфигурации.
        """
        self.config = config

    def get_file_list(self, test_name: str) -> List[str]:
        """Получает список путей к файлам в папке теста.

        Args:
            test_name (str): Имя папки теста (например, '1st_test').

        Returns:
            List[str]: Список абсолютных путей к файлам.
        """
        path = os.path.join(self.config.raw_data_path, test_name)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Путь не найден: {path}")
        
        files = sorted(os.listdir(path))
        return [os.path.join(path, f) for f in files if not f.startswith('.')]

    def parse_timestamp(self, file_path: str) -> datetime:
        """Извлекает метку времени из имени файла.

        Args:
            file_path (str): Путь к файлу.

        Returns:
            datetime: Объект времени.
        """
        filename = os.path.basename(file_path)
        return datetime.strptime(filename, "%Y.%m.%d.%H.%M.%S")

    def load_file_content(self, file_path: str, test_name: str) -> pd.DataFrame:
        """Читает содержимое файла в DataFrame согласно спекам теста.

        Args:
            file_path (str): Путь к файлу.
            test_name (str): Имя теста для определения колонок.

        Returns:
            pd.DataFrame: Матрица данных файла.
        """
        spec = self.config.experiments[test_name]
        df = pd.read_csv(file_path, sep='\t', header=None)
        
        if df.shape[1] != spec.column_count:
            # На случай, если в файле есть лишние пустые колонки (бывает в IMS)
            df = df.iloc[:, :spec.column_count]
            
        df.columns = spec.channels
        return df