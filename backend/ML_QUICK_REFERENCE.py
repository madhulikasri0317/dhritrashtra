"""
Quick Reference: ML Model Usage

This file provides quick examples of how to use the DiseasePredictor model
for making predictions and analyzing results.
"""

# ============================================================================
# IMPORT AND INITIALIZE
# ============================================================================

from models.disease_model import DiseasePredictor

# Initialize predictor (loads pre-trained model if available)
predictor = DiseasePredictor(model_path='models/trained_model.pkl')

# ============================================================================
# EXAMPLE 1: PREDICT RISK LEVEL
# ============================================================================

# Define input features: [rainfall, temperature, previous_cases, population_density]
features = [
    250,      # rainfall (mm)
    32,       # temperature (°C)
    500,      # previous_cases
    7000      # population_density (/sq km)
]

# Get risk level prediction
risk_data = predictor.predict_risk_level(features)

print("Risk Prediction:")
print(f"  Risk Level: {risk_data['risk_level'].upper()}")
print(f"  Risk Probability: {risk_data['risk_probability']:.1%}")
print(f"  Confidence: {risk_data['confidence']:.1%}")

# Output:
# Risk Prediction:
#   Risk Level: HIGH
#   Risk Probability: 87.5%
#   Confidence: 92.0%

# ============================================================================
# EXAMPLE 2: PREDICT CASES
# ============================================================================

population = 20000
case_data = predictor.predict_cases(features, population=population)

print("Case Prediction:")
print(f"  Predicted Cases: {case_data['predicted_cases']}")
print(f"  Attack Rate: {case_data['attack_rate']:.2%}")
print(f"  Severity: {case_data['severity'].upper()}")

# Output:
# Case Prediction:
#   Predicted Cases: 2250
#   Attack Rate: 11.25%
#   Severity: HIGH

# ============================================================================
# EXAMPLE 3: BATCH PREDICTIONS
# ============================================================================

# Predict for multiple locations at once
locations_features = [
    [50, 20, 10, 1000],       # Low risk scenario
    [150, 28, 100, 3000],     # Medium risk scenario
    [250, 32, 500, 7000]      # High risk scenario
]

risk_levels = predictor.predict_batch(locations_features)

print("Batch Predictions:")
for i, risk_level in enumerate(risk_levels):
    print(f"  Location {i+1}: {risk_level.upper()}")

# Output:
# Batch Predictions:
#   Location 1: LOW
#   Location 2: MEDIUM
#   Location 3: HIGH

# ============================================================================
# EXAMPLE 4: GET FEATURE IMPORTANCE
# ============================================================================

importance = predictor.get_feature_importance()

print("Feature Importance:")
for feature, score in sorted(importance.items(), key=lambda x: x[1], reverse=True):
    print(f"  {feature}: {score:.4f}")

# Output:
# Feature Importance:
#   previous_cases: 0.3892
#   temperature: 0.2847
#   population_density: 0.1923
#   rainfall: 0.1338

# ============================================================================
# EXAMPLE 5: GET MODEL INFO
# ============================================================================

info = predictor.get_model_info()

print("Model Information:")
print(f"  Model Type: {info['model_type']}")
print(f"  Features: {', '.join(info['feature_names'])}")
print(f"  Training Samples: {info['training_samples']}")
print(f"  Creation Date: {info['created_date']}")
print(f"  N Estimators: {info['n_estimators']}")
print(f"  Max Depth: {info['max_depth']}")

# Output:
# Model Information:
#   Model Type: RandomForestClassifier
#   Features: rainfall, temperature, previous_cases, population_density
#   Training Samples: 500
#   Creation Date: 2026-03-10T10:30:45.123456
#   N Estimators: 150
#   Max Depth: 15

# ============================================================================
# EXAMPLE 6: TRAIN WITH NEW DATA
# ============================================================================

import numpy as np

# Generate sample training data
X_train = np.array([
    [50, 20, 10, 1000],      # Low risk
    [150, 28, 100, 3000],    # Medium risk
    [250, 32, 500, 7000],    # High risk
    [30, 18, 5, 900],        # Low risk
    [200, 30, 300, 5000]     # High risk
])

y_train = np.array([0, 1, 2, 0, 2])  # 0=low, 1=medium, 2=high

# Train the model
success = predictor.train(X_train, y_train)

if success:
    print("✓ Model trained successfully")
else:
    print("✗ Training failed")

# ============================================================================
# EXAMPLE 7: REAL-WORLD SCENARIO
# ============================================================================

# Scenario: New Delhi during monsoon season
NEW_DELHI_SCENARIO = {
    'district': 'New Delhi',
    'rainfall': 280,           # Heavy monsoon
    'temperature': 32,         # Hot
    'previous_cases': 450,     # Ongoing outbreak
    'population_density': 8500, # High density
    'population': 50000
}

print("\n" + "="*60)
print(f"Scenario: {NEW_DELHI_SCENARIO['district']}")
print("="*60)

features = [
    NEW_DELHI_SCENARIO['rainfall'],
    NEW_DELHI_SCENARIO['temperature'],
    NEW_DELHI_SCENARIO['previous_cases'],
    NEW_DELHI_SCENARIO['population_density']
]

risk_data = predictor.predict_risk_level(features)
case_data = predictor.predict_cases(features, NEW_DELHI_SCENARIO['population'])

print(f"Risk Level: {risk_data['risk_level'].upper()}")
print(f"Risk Probability: {risk_data['risk_probability']:.1%}")
print(f"Predicted Cases: {case_data['predicted_cases']}")
print(f"Attack Rate: {case_data['attack_rate']:.2%}")
print(f"Affected Population: {case_data['predicted_cases'] * 5:,}")

# ============================================================================
# EXAMPLE 8: FEATURE INTERPRETATION
# ============================================================================

"""
Feature Ranges and Interpretation:

RAINFALL (mm):
  0-50:      Very low precipitation → Low disease transmission
  50-150:    Moderate rainfall → Medium risk
  150-250:   High rainfall → Higher risk
  250+:      Extreme rainfall → Highest risk

TEMPERATURE (°C):
  < 20:      Cool conditions → Lower transmission
  20-25:     Moderate → Medium risk
  25-35:     Optimal for pathogens → High risk
  > 35:      Very hot → Lower transmission

PREVIOUS CASES:
  0:         No cases → Low baseline risk
  1-100:     Emerging cases → Medium risk
  100-500:   Active outbreak → High risk
  500+:      Severe outbreak → Critical risk

POPULATION DENSITY (/sq km):
  < 1000:    Sparse population → Lower transmission
  1000-3000: Moderate density → Medium risk
  3000-7000: Urban → High risk
  7000+:     Dense urban → Highest risk
"""

# ============================================================================
# EXAMPLE 9: CONFIDENCE INTERPRETATION
# ============================================================================

"""
Confidence Score Guide:

0.90-1.00: Very High Confidence
  → Model is very sure about prediction
  → Suitable for critical decision making

0.70-0.90: High Confidence
  → Model is reasonably sure
  → Good for normal operations

0.50-0.70: Medium Confidence
  → Model is somewhat uncertain
  → Requires manual review before action

< 0.50: Low Confidence
  → Model is very uncertain
  → Should not be used for decisions without expert review
"""

# ============================================================================
# EXAMPLE 10: INTEGRATED PREDICTION PIPELINE
# ============================================================================

def make_comprehensive_prediction(district, rainfall, temperature,
                                  previous_cases, population_density,
                                  population):
    """
    Comprehensive prediction pipeline returning all relevant metrics.
    """
    features = [rainfall, temperature, previous_cases, population_density]

    # Get predictions
    risk_data = predictor.predict_risk_level(features)
    case_data = predictor.predict_cases(features, population)
    importance = predictor.get_feature_importance()

    # Compile results
    result = {
        'district': district,
        'prediction': {
            'risk_level': risk_data['risk_level'],
            'risk_probability': risk_data['risk_probability'],
            'confidence': risk_data['confidence'],
            'predicted_cases': case_data['predicted_cases'],
            'attack_rate': case_data['attack_rate'],
            'affected_population': case_data['predicted_cases'] * 5
        },
        'input_features': {
            'rainfall': rainfall,
            'temperature': temperature,
            'previous_cases': previous_cases,
            'population_density': population_density
        },
        'model_info': {
            'feature_importance': importance,
            'confidence_level': 'High' if risk_data['confidence'] > 0.7 else 'Medium' if risk_data['confidence'] > 0.5 else 'Low'
        }
    }

    return result

# Use the pipeline
prediction = make_comprehensive_prediction(
    district='Mumbai',
    rainfall=200,
    temperature=30,
    previous_cases=300,
    population_density=6000,
    population=30000
)

print("\nComprehensive Prediction Results:")
print(f"District: {prediction['district']}")
print(f"Risk Level: {prediction['prediction']['risk_level'].upper()}")
print(f"Predicted Cases: {prediction['prediction']['predicted_cases']}")
print(f"Confidence: {prediction['model_info']['confidence_level']}")

# ============================================================================
# BEST PRACTICES
# ============================================================================

"""
1. FEATURE NORMALIZATION
   - Ensure input features are in expected ranges
   - Missing values should be imputed appropriately

2. CONFIDENCE ASSESSMENT
   - Always check confidence score
   - Build alerts based on both risk level AND confidence

3. REGULAR RETRAINING
   - Retrain model monthly or quarterly
   - Update with latest case data
   - Monitor model performance metrics

4. ENSEMBLE APPROACH
   - Combine predictions from multiple prediction periods
   - Cross-validate with domain experts
   - Use multiple models for critical decisions

5. THRESHOLD TUNING
   - Adjust risk thresholds based on local conditions
   - Account for resource constraints
   - Consider false positive/negative trade-offs

6. EXPLAINABILITY
   - Always provide feature importance
   - Explain key driving factors
   - Help stakeholders understand predictions
"""

# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Issue: "Model not found" error
Solution: Run train_model.py to create trained_model.pkl first

Issue: "Scaler transform error"
Solution: Ensure features are in expected numeric ranges

Issue: Predictions seem unrealistic
Solution: Check input features against expected ranges

Issue: Low confidence scores
Solution: Retrain model with more data or better features

For more help, see ML_DATABASE_GUIDE.md
"""
