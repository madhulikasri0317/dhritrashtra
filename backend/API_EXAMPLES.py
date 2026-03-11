"""
Dhritrashtra API Examples and Usage
"""

# Example 1: Disease Outbreak Prediction (/api/predictions/predict)
# Returns: district, disease, risk_level, predicted_cases, timeframe

import requests
import json

BASE_URL = "http://localhost:5000"

# Example Request 1: Predict disease outbreak
def predict_outbreak_example():
    """
    Predict disease outbreak for a district
    """
    payload = {
        "district": "New Delhi",
        "water_quality": 35,
        "temperature": 28,
        "humidity": 75,
        "rainfall": 120,
        "population_density": 5000
    }

    response = requests.post(
        f"{BASE_URL}/api/predictions/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    result = response.json()
    print("Outbreak Prediction Result:")
    print(json.dumps(result, indent=2))

    # Expected Response:
    # {
    #     "success": true,
    #     "district": "New Delhi",
    #     "disease": "Cholera",
    #     "risk_level": "high",
    #     "predicted_cases": 750,
    #     "timeframe": "1-2 weeks",
    #     "confidence_score": 0.85
    # }

# Example 2: Get Active Alerts (/api/alerts)
def get_alerts_example():
    """Get all active alerts"""
    response = requests.get(f"{BASE_URL}/api/alerts")
    result = response.json()

    print("\nActive Alerts:")
    print(json.dumps(result, indent=2))

    # Expected Response:
    # {
    #     "success": true,
    #     "alerts": [
    #         {
    #             "id": 1,
    #             "title": "High cholera risk detected",
    #             "region": "Region A",
    #             "severity": "high",
    #             "message": "Water contamination levels elevated",
    #             "timestamp": "2026-03-10T10:30:45.123456",
    #             "affected_population": 10000
    #         }
    #     ],
    #     "count": 1
    # }

# Example 3: Get Risk Map Data (/api/maps/risk-data)
def get_risk_data_example():
    """Get risk data for map visualization"""
    params = {
        "bounds": "28.5,77.0,28.7,77.3",
        "zoom": 12
    }

    response = requests.get(f"{BASE_URL}/api/maps/risk-data", params=params)
    result = response.json()

    print("\nRisk Map Data:")
    print(json.dumps(result, indent=2))

    # Expected Response:
    # {
    #     "success": true,
    #     "risk_points": [
    #         {
    #             "lat": 28.6139,
    #             "lon": 77.2090,
    #             "risk_score": 0.85,
    #             "disease": "cholera",
    #             "intensity": "high"
    #         }
    #     ],
    #     "bounds": "28.5,77.0,28.7,77.3"
    # }

# Example 4: Health Check (/api/health)
def health_check_example():
    """Check if API is running"""
    response = requests.get(f"{BASE_URL}/api/health")
    result = response.json()

    print("\nHealth Check:")
    print(json.dumps(result, indent=2))

    # Expected Response:
    # {
    #     "status": "healthy",
    #     "service": "Dhritrashtra API"
    # }

# Example 5: API Documentation (/api/)
def api_docs_example():
    """Get API documentation"""
    response = requests.get(BASE_URL)
    result = response.json()

    print("\nAPI Documentation:")
    print(json.dumps(result, indent=2))

# Example 6: Create Alert (/api/alerts)
def create_alert_example():
    """Create a new alert"""
    payload = {
        "title": "Typhoid Outbreak Warning",
        "region": "Mumbai",
        "severity": "high",
        "message": "Water supply contamination detected",
        "affected_population": 50000
    }

    response = requests.post(
        f"{BASE_URL}/api/alerts",
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    result = response.json()
    print("\nCreate Alert Result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    print("=" * 60)
    print("DHRITRASHTRA API EXAMPLES")
    print("=" * 60)

    try:
        health_check_example()
        api_docs_example()
        predict_outbreak_example()
        get_alerts_example()
        get_risk_data_example()
        create_alert_example()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the Flask server is running on http://localhost:5000")
