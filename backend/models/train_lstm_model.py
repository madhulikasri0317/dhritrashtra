"""
Training script for LSTM time-series disease predictor.
"""

import numpy as np
from lstm_disease_model import LSTMDiseasePredictor, LSTMConfig


def build_synthetic_weekly_cases(points=120):
    """Generate synthetic weekly data with seasonality and trend."""
    np.random.seed(42)
    weeks = np.arange(points)
    seasonal = 20 * np.sin(2 * np.pi * weeks / 26)
    trend = 0.3 * weeks
    noise = np.random.normal(0, 6, points)
    base = 45
    values = np.maximum(0, base + seasonal + trend + noise)
    return values.astype(int).tolist()


def main():
    data = build_synthetic_weekly_cases()

    predictor = LSTMDiseasePredictor(
        LSTMConfig(sequence_length=8, units=64, dropout=0.2, epochs=20, batch_size=16)
    )

    history = predictor.train(data)
    predictor.save('models/lstm_disease_model.keras', 'models/lstm_scaler.pkl')

    forecast = predictor.forecast_next(data[-8:], horizon=6)

    print('Training complete.')
    print('Final train loss:', round(history['loss'][-1], 4))
    if 'val_loss' in history:
        print('Final validation loss:', round(history['val_loss'][-1], 4))
    print('Next 6-week forecasted cases:', forecast)


if __name__ == '__main__':
    main()
