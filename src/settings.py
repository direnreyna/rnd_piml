# src/settings.py

from dataclasses import dataclass, field
from typing import Dict, List

@dataclass(frozen=True)
class WindowSettings:
    """Параметры сегментации данных."""
    length: int = 100
    step: int = 50  # Перекрытие 50%
    sampling_rate: int = 20000

@dataclass(frozen=True)
class ExperimentSpec:
    """Описание структуры эксперимента."""
    column_count: int
    bearing_names: List[str]
    # Для 1-го теста: [B1_x, B1_y, B2_x, B2_y, ...]
    # Для остальных: [B1, B2, B3, B4]
    channels: List[str]

@dataclass
class GlobalConfig:
    """Глобальные настройки проекта."""
    raw_data_path: str = "/media/Cruiser/rnd_data/data/"
    output_path: str = "./processed_data.parquet"
    
    window: WindowSettings = field(default_factory=WindowSettings)
    
    # Спецификации экспериментов NASA IMS
    experiments: Dict[str, ExperimentSpec] = field(default_factory=lambda: {
        "1st_test": ExperimentSpec(
            column_count=8,
            bearing_names=["Bearing1", "Bearing2", "Bearing3", "Bearing4"],
            channels=["B1_x", "B1_y", "B2_x", "B2_y", "B3_x", "B3_y", "B4_x", "B4_y"]
        ),
        "2nd_test": ExperimentSpec(
            column_count=4,
            bearing_names=["Bearing1", "Bearing2", "Bearing3", "Bearing4"],
            channels=["B1", "B2", "B3", "B4"]
        ),
        "3rd_test": ExperimentSpec(
            column_count=4,
            bearing_names=["Bearing1", "Bearing2", "Bearing3", "Bearing4"],
            channels=["B1", "B2", "B3", "B4"]
        ),
        "4th_test": ExperimentSpec(
            column_count=4,
            bearing_names=["Bearing1", "Bearing2", "Bearing3", "Bearing4"],
            channels=["B1", "B2", "B3", "B4"]
        )
    })