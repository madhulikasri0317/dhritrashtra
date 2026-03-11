"""
LSTM model for time-series disease outbreak prediction.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib


Sequential = None
load_model = None
LSTM = None
Dense = None
Dropout = None


@dataclass
class LSTMConfig:
    sequence_length: int = 8
    units: int = 64
    dropout: float = 0.2
    epochs: int = 25
    batch_size: int = 16


class LSTMDiseasePredictor:
    """LSTM predictor for future disease case counts."""

    def __init__(self, config: LSTMConfig | None = None):
        self.config = config or LSTMConfig()
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None

    def _check_backend(self):
        global Sequential, load_model, LSTM, Dense, Dropout

        if Sequential is not None:
            return

        try:
            tf_models = importlib.import_module('tensorflow.keras.models')
            tf_layers = importlib.import_module('tensorflow.keras.layers')
            Sequential = tf_models.Sequential
            load_model = tf_models.load_model
            LSTM = tf_layers.LSTM
            Dense = tf_layers.Dense
            Dropout = tf_layers.Dropout
        except Exception as error:
            raise ImportError(
                'TensorFlow is not installed. Install tensorflow to use the LSTM predictor.'
            ) from error

    def prepare_sequences(self, cases_series):
        values = np.array(cases_series, dtype=np.float32).reshape(-1, 1)
        scaled = self.scaler.fit_transform(values)

        sequence_length = self.config.sequence_length
        if len(scaled) <= sequence_length:
            raise ValueError(
                f'Need more than {sequence_length} values to create training sequences.'
            )

        x_data = []
        y_data = []
        for idx in range(sequence_length, len(scaled)):
            x_data.append(scaled[idx - sequence_length:idx, 0])
            y_data.append(scaled[idx, 0])

        x_data = np.array(x_data)
        y_data = np.array(y_data)
        x_data = x_data.reshape((x_data.shape[0], x_data.shape[1], 1))
        return x_data, y_data

    def build_model(self):
        self._check_backend()
        model = Sequential([
            LSTM(self.config.units, return_sequences=True, input_shape=(self.config.sequence_length, 1)),
            Dropout(self.config.dropout),
            LSTM(self.config.units // 2),
            Dropout(self.config.dropout),
            Dense(1),
        ])
        model.compile(optimizer='adam', loss='mse', metrics=['mae'])
        self.model = model
        return model

    def train(self, cases_series):
        x_train, y_train = self.prepare_sequences(cases_series)
        if self.model is None:
            self.build_model()

        history = self.model.fit(
            x_train,
            y_train,
            epochs=self.config.epochs,
            batch_size=self.config.batch_size,
            validation_split=0.2,
            verbose=0,
        )
        return history.history

    def forecast_next(self, recent_series, horizon=4):
        if self.model is None:
            raise ValueError('Model is not trained. Call train() or load() first.')

        seq_len = self.config.sequence_length
        if len(recent_series) < seq_len:
            raise ValueError(f'Need at least {seq_len} recent points for forecasting.')

        series = np.array(recent_series, dtype=np.float32).reshape(-1, 1)
        scaled = self.scaler.transform(series)
        window = scaled[-seq_len:, 0].tolist()

        outputs = []
        for _ in range(horizon):
            x_in = np.array(window[-seq_len:]).reshape(1, seq_len, 1)
            pred_scaled = float(self.model.predict(x_in, verbose=0)[0][0])
            window.append(pred_scaled)
            outputs.append(pred_scaled)

        outputs_np = np.array(outputs).reshape(-1, 1)
        forecast = self.scaler.inverse_transform(outputs_np).flatten().tolist()
        return [max(0, int(round(value))) for value in forecast]

    def save(self, model_path='models/lstm_disease_model.keras', scaler_path='models/lstm_scaler.pkl'):
        if self.model is None:
            raise ValueError('No model to save. Train the model first.')

        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        self.model.save(model_path)
        joblib.dump(self.scaler, scaler_path)

    def load(self, model_path='models/lstm_disease_model.keras', scaler_path='models/lstm_scaler.pkl'):
        self._check_backend()
        self.model = load_model(model_path)
        self.scaler = joblib.load(scaler_path)
        return self
