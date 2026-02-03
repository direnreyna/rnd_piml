# run_pipeline.py

import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from src.settings import GlobalConfig
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

            for channel in df.columns:
                # Используем to_numpy() для явного приведения к ndarray[float64]
                signal_data: np.ndarray = df[channel].to_numpy(dtype=np.float64)

                # Нарезка на окна с перекрытием
                for start in range(0, len(signal_data) - win_len + 1, step):
                    window = signal_data[start : start + win_len]

                    features = calc.calculate_all(window)

                    spec_features = calc_spec.calculate_spectral(
                        window, 
                        config.window.sampling_rate
                    )
                    features.update(spec_features)

                    aggregator.add_row(
                        timestamp=ts,
                        test_id=target_test,
                        sensor_id=channel,
                        features=features
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

if __name__ == "__main__":
    main()