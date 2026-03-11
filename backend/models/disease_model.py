"""
Disease prediction model using scikit-learn
Predicts water borne disease outbreaks based on environmental and epidemiological data.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime

class DiseasePredictor:
    """
    Machine Learning model for predicting water borne disease risk and outbreak cases.
    Uses scikit-learn RandomForestClassifier for risk classification.

    Input Features:
        - rainfall: Precipitation in mm
        - temperature: Temperature in Celsius
        - previous_cases: Number of cases in previous period
        - population_density: Population per sq km

    Output:
        - risk_level: Classification (low/medium/high)
        - predicted_cases: Estimated number of cases
    """

    def __init__(self, model_path='models/trained_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'rainfall',
            'temperature',
            'previous_cases',
            'population_density'
        ]

        self.model_metadata = {
            'created_date': None,
            'training_samples': 0,
            'feature_importance': {}
        }

        # Load model if exists, otherwise create new
        if os.path.exists(model_path):
            self.load_model()
        else:
            self.model = RandomForestClassifier(
                n_estimators=150,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
                class_weight='balanced'
            )

    def train(self, X_train, y_train):
        """
        Train the model with provided data.

        Args:
            X_train: Features array (rainfall, temperature, previous_cases, population_density)
            y_train: Target labels (0=low, 1=medium, 2=high)

        Returns:
            bool: True if training successful
        """
        try:
            # Ensure data is properly shaped
            X_array = np.array(X_train)
            y_array = np.array(y_train)

            # Scale features
            X_scaled = self.scaler.fit_transform(X_array)

            # Train model
            self.model.fit(X_scaled, y_array)

            # Update metadata
            self.model_metadata['created_date'] = datetime.now().isoformat()
            self.model_metadata['training_samples'] = len(X_train)

            # Save model
            self.save_model()
            return True
        except Exception as e:
            print(f"Training error: {str(e)}")
            return False

    def predict_risk_level(self, features):
        """
        Predict disease risk level.

        Args:
            features: list of [rainfall, temperature, previous_cases, population_density]

        Returns:
            dict: {
                'risk_probability': float (0-1),
                'risk_level': str ('low', 'medium', 'high'),
                'confidence': float (0-1)
            }
        """
        try:
            # Ensure features is numpy array
            features_array = np.array(features).reshape(1, -1)

            # Scale features
            features_scaled = self.scaler.transform(features_array)

            # Get prediction probability
            probability = self.model.predict_proba(features_scaled)[0]
            predicted_class = self.model.predict(features_scaled)[0]

            # Determine risk level
            if predicted_class == 2 or (len(probability) > 2 and probability[2] > 0.5):
                risk_level = 'high'
                risk_probability = float(probability[2]) if len(probability) > 2 else max(probability)
            elif predicted_class == 1 or (len(probability) > 1 and probability[1] > 0.5):
                risk_level = 'medium'
                risk_probability = float(probability[1]) if len(probability) > 1 else max(probability)
            else:
                risk_level = 'low'
                risk_probability = float(probability[0]) if len(probability) > 0 else min(probability)

            confidence = float(max(probability))

            return {
                'risk_probability': round(risk_probability, 3),
                'risk_level': risk_level,
                'confidence': round(confidence, 3)
            }

        except Exception as e:
            print(f"Risk prediction error: {str(e)}")
            return {
                'risk_probability': 0.0,
                'risk_level': 'unknown',
                'confidence': 0.0
            }

    def predict_cases(self, features, population=10000):
        """
        Predict number of disease cases based on risk level and population.

        Args:
            features: list of [rainfall, temperature, previous_cases, population_density]
            population: Total population in district (default: 10000)

        Returns:
            dict: {
                'predicted_cases': int,
                'attack_rate': float (0-1),
                'severity': str
            }
        """
        try:
            # Get risk level
            risk_data = self.predict_risk_level(features)
            risk_probability = risk_data['risk_probability']

            # Extract previous cases
            previous_cases = features[2]

            # Calculate attack rate based on risk level
            if risk_data['risk_level'] == 'high':
                base_attack_rate = 0.15
                growth_multiplier = 2.5
            elif risk_data['risk_level'] == 'medium':
                base_attack_rate = 0.08
                growth_multiplier = 1.5
            else:
                base_attack_rate = 0.03
                growth_multiplier = 0.8

            # Calculate predicted cases
            attack_rate = base_attack_rate * risk_probability
            predicted_cases = int(population * attack_rate)

            # Account for growth from previous cases
            if previous_cases > 0:
                predicted_cases = max(predicted_cases, int(previous_cases * growth_multiplier))

            return {
                'predicted_cases': predicted_cases,
                'attack_rate': round(attack_rate, 4),
                'severity': risk_data['risk_level']
            }

        except Exception as e:
            print(f"Case prediction error: {str(e)}")
            return {
                'predicted_cases': 0,
                'attack_rate': 0.0,
                'severity': 'unknown'
            }

    def predict(self, features):
        """
        Combined prediction: returns risk probability.

        Args:
            features: list of [rainfall, temperature, previous_cases, population_density]

        Returns:
            float: Risk probability (0-1)
        """
        risk_data = self.predict_risk_level(features)
        return risk_data['risk_probability']

    def predict_batch(self, features_list):
        """
        Predict for multiple locations at once.

        Args:
            features_list: List of feature arrays

        Returns:
            list: List of risk levels for each location
        """
        predictions = []
        for features in features_list:
            risk_data = self.predict_risk_level(features)
            predictions.append(risk_data['risk_level'])
        return predictions

    def get_feature_importance(self):
        """
        Get feature importance scores from the trained model.

        Returns:
            dict: Feature names mapped to importance scores
        """
        if self.model is None:
            return {}

        importances = self.model.feature_importances_
        feature_importance = {
            name: float(importance)
            for name, importance in zip(self.feature_names, importances)
        }

        self.model_metadata['feature_importance'] = feature_importance
        return feature_importance

    def save_model(self):
        """
        Save trained model and scaler to disk.

        Returns:
            bool: True if save successful
        """
        try:
            model_dir = os.path.dirname(self.model_path)
            if model_dir and not os.path.exists(model_dir):
                os.makedirs(model_dir)

            joblib.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_names': self.feature_names,
                'metadata': self.model_metadata
            }, self.model_path)

            print(f"Model saved to {self.model_path}")
            return True
        except Exception as e:
            print(f"Save error: {str(e)}")
            return False

    def load_model(self):
        """
        Load model from disk.

        Returns:
            bool: True if load successful
        """
        try:
            data = joblib.load(self.model_path)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_names = data.get('feature_names', self.feature_names)
            self.model_metadata = data.get('metadata', self.model_metadata)
            print(f"Model loaded from {self.model_path}")
            return True
        except Exception as e:
            print(f"Load error: {str(e)}")
            return False

    def get_model_info(self):
        """
        Get model information and metadata.

        Returns:
            dict: Model information including creation date, training samples, and feature importance
        """
        info = {
            'model_type': 'RandomForestClassifier',
            'feature_names': self.feature_names,
            'created_date': self.model_metadata.get('created_date'),
            'training_samples': self.model_metadata.get('training_samples'),
            'feature_importance': self.get_feature_importance()
        }

        if self.model:
            info.update({
                'n_estimators': self.model.n_estimators,
                'max_depth': self.model.max_depth,
                'random_state': self.model.random_state
            })

        return info
