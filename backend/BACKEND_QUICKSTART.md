# Dhritrashtra Backend - Quick Start Guide

## Overview
The Dhritrashtra backend is a Flask REST API for predicting water-borne disease outbreaks and managing alerts.

## Prerequisites
- Python 3.9+
- PostgreSQL 12+ (or SQLite for development)
- pip (Python package manager)

## Installation

### 1. Create Virtual Environment
```bash
cd backend
python -m venv venv
```

**Activate on Windows:**
```bash
venv\Scripts\activate
```

**Activate on macOS/Linux:**
```bash
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your database credentials:
```
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/dhritrashtra
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 4. Initialize Database
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### 5. Run Flask Server
```bash
python app.py
```

Server runs on: **http://localhost:5000**

---

## Project Structure

```
backend/
├── app.py                    # Main Flask app
├── routes/
│   ├── predictions.py        # Disease prediction endpoints
│   ├── alerts.py             # Alert management endpoints
│   └── maps.py               # Risk mapping endpoints
├── models/
│   └── disease_model.py      # Machine learning model
├── database/
│   └── db.py                 # Database models & config
├── data/                     # Training data directory
├── requirements.txt          # Python dependencies
├── API_DOCUMENTATION.md      # Complete API reference
├── API_EXAMPLES.py           # Usage examples
└── .env.example              # Environment template
```

---

## Core Endpoints

### Disease Prediction
- **POST** `/api/predictions/predict` - Predict outbreak (returns: district, disease, risk_level, predicted_cases, timeframe)
- **POST** `/api/predictions/` - Detailed prediction with location
- **GET** `/api/predictions/history?location=<location>` - Historical predictions

### Alerts
- **GET** `/api/alerts` - Get active alerts
- **POST** `/api/alerts` - Create alert
- **DELETE** `/api/alerts/<id>` - Dismiss alert

### Risk Maps
- **GET** `/api/maps/risk-data` - Get risk visualization data
- **GET** `/api/maps/heatmap` - Get heatmap data
- **GET** `/api/maps/regions` - Get region statistics

### System
- **GET** `/api/health` - Health check
- **GET** `/` - API documentation

---

## Example API Call

### Predict Disease Outbreak
```bash
curl -X POST http://localhost:5000/api/predictions/predict \
  -H "Content-Type: application/json" \
  -d '{
    "district": "New Delhi",
    "water_quality": 35,
    "temperature": 28,
    "humidity": 75,
    "rainfall": 120,
    "population_density": 5000
  }'
```

**Response:**
```json
{
    "success": true,
    "district": "New Delhi",
    "disease": "Cholera",
    "risk_level": "high",
    "predicted_cases": 750,
    "timeframe": "1-2 weeks",
    "confidence_score": 0.85
}
```

---

## Python Usage Example

```python
import requests
import json

BASE_URL = "http://localhost:5000"

# Predict outbreak
payload = {
    "district": "Mumbai",
    "water_quality": 40,
    "temperature": 30,
    "humidity": 80,
    "rainfall": 150,
    "population_density": 6000
}

response = requests.post(
    f"{BASE_URL}/api/predictions/predict",
    json=payload
)

result = response.json()
print(json.dumps(result, indent=2))
```

---

## Testing

### Run Examples
```bash
python API_EXAMPLES.py
```

### Manual Testing with cURL
```bash
# Health check
curl http://localhost:5000/api/health

# API docs
curl http://localhost:5000/

# Get alerts
curl http://localhost:5000/api/alerts

# Get risk data
curl "http://localhost:5000/api/maps/risk-data?bounds=28.5,77.0,28.7,77.3"
```

---

## Database Models

### Location
- `id` (Primary Key)
- `name` (String)
- `latitude` / `longitude` (Float)
- `region` (String)
- `created_at` (DateTime)

### Prediction
- `id` (Primary Key)
- `location_id` (Foreign Key)
- `disease_type` (String)
- `risk_score` (Float)
- `risk_level` (String)
- `water_quality`, `temperature`, `humidity`, `rainfall`, `population_density` (Float)
- `created_at` (DateTime)

### Alert
- `id` (Primary Key)
- `location_id` (Foreign Key)
- `title` (String)
- `message` (Text)
- `severity` (String: low/medium/high)
- `disease_type` (String)
- `affected_population` (Integer)
- `is_active` (Boolean)
- `created_at` / `dismissed_at` (DateTime)

### RiskMap
- `id` (Primary Key)
- `latitude` / `longitude` (Float)
- `risk_score` (Float)
- `intensity` (String)
- `disease_type` (String)
- `created_at` / `updated_at` (DateTime)

---

## Machine Learning Model

**Algorithm:** Random Forest Classifier (scikit-learn)

**Input Features:**
1. Water Quality (0-100)
2. Temperature (°C)
3. Humidity (%)
4. Rainfall (mm)
5. Population Density (per sq km)

**Output:** Risk Probability (0-1)

**Risk Levels:**
- High: > 0.7
- Medium: 0.4 - 0.7
- Low: < 0.4

---

## Environment Variables

```env
# Flask Configuration
FLASK_ENV=development|production
DEBUG=True|False

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
SECRET_KEY=your-secret-key-here
```

---

## Troubleshooting

### Port Already in Use
```bash
# Change port in app.py
app.run(port=5001)
```

### Database Connection Error
```bash
# Check PostgreSQL is running
# Update DATABASE_URL in .env
# Verify credentials
```

### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Import Errors
```bash
# Make sure virtual environment is activated
# Reinstall packages: pip install -r requirements.txt
```

---

## Production Deployment

1. Set `FLASK_ENV=production`
2. Use production database (PostgreSQL)
3. Generate strong `SECRET_KEY`
4. Enable security headers
5. Add authentication (JWT/API keys)
6. Set up rate limiting
7. Use Gunicorn WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```
8. Deploy with Docker:
   ```bash
   docker build -t dhritrashtra-backend .
   docker run -p 5000:5000 dhritrashtra-backend
   ```

---

## API Documentation
See `API_DOCUMENTATION.md` for complete endpoint reference.

## Code Examples
See `API_EXAMPLES.py` for Python usage examples.

---

## Support
For issues or questions, check the main README.md in the project root.
