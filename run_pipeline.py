# run_pipeline.py

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from typing import Dict

from src.settings import GlobalConfig, ExperimentSpec
from src.data_loader import IMSRawLoader
from src.feature_engine import FeatureCalculator
from src.spectral_engine import SpectralCalculator
from src.enhancer import DatasetEnhancer
from src.storage_manager import DataAggregator
from src.data_explorer import DataExplorer

def main() -> None:
    """Основной цикл обработки данных NASA IMS."""
    config = GlobalConfig()
    # Определение путей к файлам результатов
    base_path: str = config.output_path
    enhanced_path: str = base_path.replace(".parquet", "_enhanced.parquet")

    # Проверка существования созданного датафрейма
    if os.path.exists(base_path):
        print(f"[*] Dataset found at {base_path}. Skipping generation...")

    ################################################################################
    # СОЗДАНИЕ ДАТАФРЕЙМА
    ################################################################################
    else:
        # Если файла нет — запускаем обработку
            
        loader = IMSRawLoader(config)
        aggregator = DataAggregator()
        calc = FeatureCalculator()
        calc_spec = SpectralCalculator()

        target_test = "1st_test"
        print(f"[*] Starting pipeline for: {target_test}")

        try:
            file_list = loader.get_file_list(target_test)
        except FileNotFoundError as e:
            print(f"[!] Error: {e}")
            return

        # Используем tqdm для отслеживания прогресса по файлам
        for file_path in tqdm(file_list, desc="Processing files"):
            ts = loader.parse_timestamp(file_path)
            df = loader.load_file_content(file_path, target_test)

            win_len = config.window.length
            step = config.window.step
            spec = config.experiments[target_test]
            
            for b_name in spec.bearing_names:
                # 1. Сбор признаков по всем каналам подшипника
                b_features: Dict[str, float] = {}
                channels = spec.bearing_to_channels[b_name]
                
                # Подготовка сигналов для всех осей подшипника
                axis_signals = {ch: df[ch].to_numpy(dtype=np.float64) for ch in channels}
                
                # 2. Нарезка на окна (синхронно для всех осей)
                n_samples = len(next(iter(axis_signals.values())))
                for start in range(0, n_samples - win_len + 1, step):
                    window_features: Dict[str, float] = {}
                    
                    for ch_name, full_signal in axis_signals.items():
                        window = full_signal[start : start + win_len]
                        
                        # Базовая статистика
                        base_f = calc.calculate_all(window)
                        # Спектральная статистика
                        spec_f = calc_spec.calculate_spectral(window, config.window.sampling_rate)
                        
                        # Добавление суффикса канала (например, _x или _y)
                        suffix = ch_name[-1] if "_" in ch_name else ""
                        for k, v in {**base_f, **spec_f}.items():
                            window_features[f"{k}_{suffix}" if suffix else k] = v
                    
                    # 3. Расчет RUL и Health State
                    rul, state = calculate_bearing_status(ts, b_name, spec, config)
                    
                    aggregator.add_row(
                        timestamp=ts,
                        test_id=target_test,
                        bearing_id=b_name,
                        features=window_features,
                        rul=rul,
                        health_state=state
                    )

        # Сохранение результата
        print(f"[*] Processing complete. Saving to {base_path}...")
        aggregator.save(base_path)

    ################################################################################
    # ЭТАП УЛУЧШЕНИЯ (Enhancement) - выполняется всегда, если есть базовый файл
    ################################################################################
    if not os.path.exists(enhanced_path):
        print("[*] Enhancing dataset (rolling stats & derivatives)...")
        base_df = pd.read_parquet(base_path)
        enhancer = DatasetEnhancer(base_df)
        final_df = enhancer.process(rolling_window=10)
        final_df.to_parquet(enhanced_path, index=False)
        print(f"[+] Enhanced dataset saved to {enhanced_path}")
    else:
        print(f"[*] Enhanced dataset already exists at {enhanced_path}")

    ################################################################################
    # ТЕСТ ДАТАФРЕЙМА
    ################################################################################
    print("[*] Running dataset validation...")
    explorer = DataExplorer(enhanced_path)
    explorer.run_basic_checks()

    print("[+] Done.")

def calculate_bearing_status(current_ts: datetime, b_name: str, 
                             spec: ExperimentSpec, config: GlobalConfig) -> tuple[float, int]:
    """Рассчитывает RUL и класс здоровья подшипника.

    Args:
        current_ts (datetime): Текущее время файла.
        b_name (str): Имя подшипника.
        spec (ExperimentSpec): Спецификация теста.
        config (GlobalConfig): Глобальный конфиг.

    Returns:
        tuple[float, int]: (RUL в часах, класс здоровья 0-2).
    """
    fail_str = spec.failure_times.get(b_name)
    
    # Если подшипник не ломался - он всегда здоров
    if fail_str is None:
        return config.rul_threshold_hours, 0
    
    fail_ts = datetime.strptime(fail_str, "%Y.%m.%d.%H.%M.%S")
    time_to_fail = (fail_ts - current_ts).total_seconds() / 3600.0
    
    # Ограничение RUL сверху согласно логике Piecewise Linear
    rul = min(config.rul_threshold_hours, max(0.0, time_to_fail))
    
    # Определение класса здоровья
    if rul >= config.rul_threshold_hours:
        state = 0 # Здоров (A)
    elif rul >= config.health_threshold_yellow:
        state = 1 # Предупреждение (B)
    else:
        state = 2 # Критический (C)
        
    return float(rul), int(state)

if __name__ == "__main__":
    main()