# adapter.py

"""
Module for adapting code to different environments (e.g., Colab vs local).
Модуль для адаптирования разных платформ запуска (т.к. Гугл-Колаб или локальной среды)
"""

import torch
from typing import Union
from config import get_environment, EnvironmentType

class EnvironmentAdapter:
    """
    A class to adapt runtime parameters based on the environment.
    Адаптирует параметры запуска в зависимости от платформы запуска.
    """

    def __init__(self) -> None:
        """
        Initializes the adapter by detecting the environment and setting device.
        Инициализирует адаптер, определяя платформу и устанавливая вид устройства для оубчения модели (CPU/GPU)
        """
        self.environment: EnvironmentType = get_environment()
        self.device: torch.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

    def describe_environment(self) -> str:
        """
        Returns a description of the current environment and device.
        Возвращает описание текущей платформы и вида устройства для оубчения модели (CPU/GPU)

        Returns:
            str: A human-readable string describing the environment and device.
        """
        device_type = "GPU" if self.device.type == "cuda" else "CPU"
        return f"Environment: {self.environment}, Device: {device_type}"
