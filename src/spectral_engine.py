# src/spectral_engine.py

import numpy as np
from scipy.fft import rfft, rfftfreq
from typing import Dict

class SpectralCalculator:
    """Класс для частотного анализа вибрационного сигнала."""

    @staticmethod
    def calculate_spectral(signal: np.ndarray, sampling_rate: int) -> Dict[str, float]:
        """Вычисляет спектральные характеристики окна сигнала через БПФ.

        Args:
            signal (np.ndarray): Массив данных окна.
            sampling_rate (int): Частота дискретизации (Гц).

        Returns:
            Dict[str, float]: Словарь с частотными признаками (центроид, энергия).
        """
        n: int = len(signal)
        # Удаление постоянной составляющей для чистоты спектра
        detrended: np.ndarray = signal - np.mean(signal)
        
        yf: np.ndarray = np.asarray(rfft(detrended))
        xf: np.ndarray = rfftfreq(n, 1 / sampling_rate)
        psd: np.ndarray = np.abs(yf)**2 

        sum_psd: float = float(np.sum(psd))
        
        if sum_psd == 0:
            return {"spectral_centroid": 0.0, "spectral_energy": 0.0}

        features: Dict[str, float] = {
            "spectral_centroid": float(np.sum(xf * psd) / sum_psd),
            "spectral_energy": float(sum_psd / n)
        }
        return features