# src/settings.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

@dataclass(frozen=True)
class WindowSettings:
    """Параметры сегментации данных."""
    length: int = 2048
    step: int = 2048
    sampling_rate: int = 20000

@dataclass(frozen=True)
class ExperimentSpec:
    """Описание структуры эксперимента."""
    column_count: int
    bearing_names: List[str]
    channels: List[str]
    # Маппинг: Имя подшипника -> Список его каналов в файле
    bearing_to_channels: Dict[str, List[str]]
    # Имя подшипника -> Дата/время выхода из строя (если есть)
    failure_times: Dict[str, Optional[str]] 

@dataclass
class GlobalConfig:
    """Глобальные настройки проекта."""
    raw_data_path: str = "/media/Cruiser/rnd_data/data/"
    output_path: str = "./processed_data.parquet"
    
    # Константы разметки здоровья
    rul_threshold_hours: float = 100.0
    health_threshold_yellow: float = 20.0

    window: WindowSettings = field(default_factory=WindowSettings)

    # Спецификации экспериментов NASA IMS
    experiments: Dict[str, ExperimentSpec] = field(default_factory=lambda: {
        "1st_test": ExperimentSpec(
            column_count=8,
            bearing_names=["Bearing1", "Bearing2", "Bearing3", "Bearing4"],
            channels=["B1_x", "B1_y", "B2_x", "B2_y", "B3_x", "B3_y", "B4_x", "B4_y"],

            bearing_to_channels={
                "Bearing1": ["B1_x", "B1_y"],
                "Bearing2": ["B2_x", "B2_y"],
                "Bearing3": ["B3_x", "B3_y"],
                "Bearing4": ["B4_x", "B4_y"]
            },
            failure_times={
                "Bearing1": None,
                "Bearing2": None,
                "Bearing3": "2003.11.25.23.39.56", # Экспертная метка конца
                "Bearing4": "2003.11.25.23.39.56"
            }
        ),
        "2nd_test": ExperimentSpec(
            column_count=4,
            bearing_names=["Bearing1", "Bearing2", "Bearing3", "Bearing4"],
            channels=["B1", "B2", "B3", "B4"],

            bearing_to_channels={
                "Bearing1": ["B1"], "Bearing2": ["B2"], 
                "Bearing3": ["B3"], "Bearing4": ["B4"]
            },
            failure_times={
                "Bearing1": "2004.02.19.06.22.39", # Конец 2-го теста
                "Bearing2": None,
                "Bearing3": None,
                "Bearing4": None
            }
        ),
        "3rd_test": ExperimentSpec(
            column_count=4,
            bearing_names=["Bearing1", "Bearing2", "Bearing3", "Bearing4"],
            channels=["B1", "B2", "B3", "B4"],

            bearing_to_channels={
                "Bearing1": ["B1"], "Bearing2": ["B2"], 
                "Bearing3": ["B3"], "Bearing4": ["B4"]
            },
            failure_times={
                "Bearing1": None,
                "Bearing2": None, 
                "Bearing3": "2004.04.04.19.01.57", # Конец 3-го теста
                "Bearing4": None
            }
        ),
        "4th_test": ExperimentSpec(
            column_count=4,
            bearing_names=["Bearing1", "Bearing2", "Bearing3", "Bearing4"],
            channels=["B1", "B2", "B3", "B4"],
            bearing_to_channels={
                "Bearing1": ["B1"], "Bearing2": ["B2"], 
                "Bearing3": ["B3"], "Bearing4": ["B4"]
            },
            failure_times={
                "Bearing1": None,
                "Bearing2": None,
                "Bearing3": None,
                "Bearing4": None}
        )
    })