"""
Training script for the Disease Prediction ML Model

This script demonstrates how to train the RandomForestClassifier model
using historical disease case data from the database.

Features:
    - rainfall: Precipitation in mm
    - temperature: Temperature in Celsius
    - previous_cases: Number of cases in previous period
    - population_density: Population per sq km

Output:
    - risk_level: Classification (0=low, 1=medium, 2=high)
    - predicted_cases: Estimated number of cases
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from disease_model import DiseasePredictor

def generate_synthetic_training_data(n_samples=500):
    """
    Generate synthetic training data for model development.

    Returns:
        tuple: (X_train, y_train) - Features and labels
    """
    print("Generating synthetic training data...")

    np.random.seed(42)

    # Generate synthetic features
    rainfall = np.random.uniform(0, 300, n_samples)
    temperature = np.random.uniform(15, 40, n_samples)
    previous_cases = np.random.randint(0, 1000, n_samples)
    population_density = np.random.uniform(100, 10000, n_samples)

    X_train = np.column_stack([rainfall, temperature, previous_cases, population_density])

    # Generate labels based on feature combinations
    # Simple rule-based labeling for synthetic data
    y_train = np.zeros(n_samples, dtype=int)

    for i in range(n_samples):
        score = 0

        # High rainfall increases risk
        if rainfall[i] > 200:
            score += 2
        elif rainfall[i] > 100:
            score += 1

        # Moderate temperature (25-35°C) increases risk
        if 25 <= temperature[i] <= 35:
            score += 2
        elif 20 <= temperature[i] <= 38:
            score += 1

        # Previous cases indicate ongoing outbreak
        if previous_cases[i] > 500:
            score += 2
        elif previous_cases[i] > 100:
            score += 1

        # High population density increases spread
        if population_density[i] > 5000:
            score += 1

        # Classify as risk level
        if score >= 5:
            y_train[i] = 2  # High risk
        elif score >= 3:
            y_train[i] = 1  # Medium risk
        else:
            y_train[i] = 0  # Low risk

    print(f"Generated {n_samples} training samples")
    print(f"Class distribution: Low={np.sum(y_train==0)}, Medium={np.sum(y_train==1)}, High={np.sum(y_train==2)}")

    return X_train, y_train

def train_model(X_train, y_train):
    """
    Train the disease prediction model.

    Args:
        X_train: Training features
        y_train: Training labels

    Returns:
        DiseasePredictor: Trained model instance
    """
    print("\nTraining model...")

    predictor = DiseasePredictor(model_path='trained_model.pkl')

    # Train the model
    success = predictor.train(X_train, y_train)

    if success:
        print("✓ Model training successful")
        print("\nModel Information:")
        info = predictor.get_model_info()
        print(f"  - Algorithm: {info['model_version']}")
        print(f"  - Features: {', '.join(info['feature_names'])}")
        print(f"  - Training Samples: {info['training_samples']}")
        print(f"  - Created: {info['created_date']}")

        print("\nFeature Importance:")
        for feature, importance in info['feature_importance'].items():
            print(f"  - {feature}: {importance:.4f}")
    else:
        print("✗ Model training failed")

    return predictor

def evaluate_model(predictor, X_test, y_test):
    """
    Evaluate model performance on test data.

    Args:
        predictor: Trained DiseasePredictor instance
        X_test: Test features
        y_test: Test labels
    """
    print("\nEvaluating model...")

    correct = 0
    predictions = []

    for i in range(len(X_test)):
        risk_data = predictor.predict_risk_level(X_test[i])
        predicted_label = {'low': 0, 'medium': 1, 'high': 2}[risk_data['risk_level']]
        predictions.append(predicted_label)

        if predicted_label == y_test[i]:
            correct += 1

    accuracy = correct / len(y_test)
    print(f"✓ Accuracy: {accuracy:.4f}")

    return accuracy

def create_sample_predictions(predictor):
    """
    Create sample predictions for demonstration.

    Args:
        predictor: Trained DiseasePredictor instance
    """
    print("\nSample Predictions:")
    print("-" * 80)

    # Sample scenarios
    scenarios = [
        {
            'name': 'Low Risk Scenario',
            'features': [50, 20, 10, 1000],
            'population': 5000
        },
        {
            'name': 'Medium Risk Scenario',
            'features': [150, 28, 100, 3000],
            'population': 10000
        },
        {
            'name': 'High Risk Scenario',
            'features': [250, 32, 500, 7000],
            'population': 20000
        }
    ]

    for scenario in scenarios:
        print(f"\n{scenario['name']}:")
        print(f"  Features: Rainfall={scenario['features'][0]}mm, "
              f"Temperature={scenario['features'][1]}°C, "
              f"Previous Cases={scenario['features'][2]}, "
              f"Pop Density={scenario['features'][3]}/sq km")

        risk_data = predictor.predict_risk_level(scenario['features'])
        case_data = predictor.predict_cases(scenario['features'], scenario['population'])

        print(f"  Risk Level: {risk_data['risk_level'].upper()}")
        print(f"  Risk Probability: {risk_data['risk_probability']:.1%}")
        print(f"  Confidence: {risk_data['confidence']:.1%}")
        print(f"  Predicted Cases: {case_data['predicted_cases']}")
        print(f"  Attack Rate: {case_data['attack_rate']:.2%}")

def main():
    """Main training pipeline"""
    print("=" * 80)
    print("DHRITRASHTRA - ML MODEL TRAINING")
    print("=" * 80)

    # Generate training data
    X_train, y_train = generate_synthetic_training_data(n_samples=500)

    # Split data
    split_idx = int(0.8 * len(X_train))
    X_train_split = X_train[:split_idx]
    y_train_split = y_train[:split_idx]
    X_test = X_train[split_idx:]
    y_test = y_train[split_idx:]

    # Train model
    predictor = train_model(X_train_split, y_train_split)

    # Evaluate model
    evaluate_model(predictor, X_test, y_test)

    # Show sample predictions
    create_sample_predictions(predictor)

    print("\n" + "=" * 80)
    print("✓ Training complete. Model saved to 'trained_model.pkl'")
    print("=" * 80)

if __name__ == '__main__':
    main()
