# src/feature_engine.py

import numpy as np
from scipy.stats import kurtosis, skew
from typing import Dict

class FeatureCalculator:
    """Расчет статистических и физических признаков для окна сигнала."""

    @staticmethod
    def calculate_all(signal: np.ndarray) -> Dict[str, float]:
        """Считает базовый набор признаков для вектора данных.

        Args:
            signal (np.ndarray): Одномерный массив данных окна.

        Returns:
            Dict[str, float]: Словарь признаков.
        """
        abs_signal = np.abs(signal)
        rms = float(np.sqrt(np.mean(signal**2)))
        peak = float(np.max(abs_signal))
        mean_val = np.mean(signal)
        
        # Защита от деления на ноль для коэффициентов
        crest_factor = peak / rms if rms != 0 else 0
        
        features = {
            "mean": mean_val,
            "std": np.std(signal),
            "rms": rms,
            "peak": peak,
            "skewness": skew(signal),
            "kurtosis": kurtosis(signal),
            "crest_factor": crest_factor,
            "peak_to_peak": np.ptp(signal),
            "clearance_factor": FeatureCalculator._clearance_factor(signal, peak)
        }
        return features

    @staticmethod
    def _clearance_factor(signal: np.ndarray, peak: float) -> float:
        """Расчет Marginal/Clearance factor."""

        mean_sqrt = float(np.mean(np.sqrt(np.abs(signal)))**2)

        return float(peak / mean_sqrt) if mean_sqrt != 0 else 0.0