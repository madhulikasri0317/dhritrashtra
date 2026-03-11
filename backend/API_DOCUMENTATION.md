# Dhritrashtra Flask Backend API Documentation

## Overview
Dhritrashtra is a REST API for predicting water-borne disease outbreaks and managing health alerts. The API provides endpoints for disease predictions, alert management, and geospatial risk mapping.

**Base URL:** `http://localhost:5000`

## Authentication
Currently, the API has no authentication. In production, add JWT tokens or API keys.

---

## API Endpoints

### 1. Health Check
**Endpoint:** `GET /api/health`

Check if the API is running and healthy.

**Response:**
```json
{
    "status": "healthy",
    "service": "Dhritrashtra API"
}
```

---

### 2. API Documentation
**Endpoint:** `GET /`

Get comprehensive API documentation and available endpoints.

**Response:**
```json
{
    "name": "Dhritrashtra",
    "description": "Water Borne Disease Prediction System",
    "version": "1.0.0",
    "status": "active",
    "endpoints": {
        "health": "/api/health",
        "disease_prediction": {
            "detail_prediction": "POST /api/predictions/",
            "outbreak_prediction": "POST /api/predictions/predict",
            "get_prediction": "GET /api/predictions/<id>",
            "prediction_history": "GET /api/predictions/history?location=<location>"
        },
        "alerts": {
            "get_alerts": "GET /api/alerts",
            "create_alert": "POST /api/alerts",
            "dismiss_alert": "DELETE /api/alerts/<id>"
        },
        "maps": {
            "risk_data": "GET /api/maps/risk-data",
            "heatmap": "GET /api/maps/heatmap",
            "regions": "GET /api/maps/regions"
        }
    }
}
```

---

## Disease Prediction Endpoints

### 3. Predict Disease Outbreak
**Endpoint:** `POST /api/predictions/predict`

Predict disease outbreak with detailed risk assessment.

**Request Body:**
```json
{
    "district": "New Delhi",
    "water_quality": 35,
    "temperature": 28,
    "humidity": 75,
    "rainfall": 120,
    "population_density": 5000
}
```

**Parameters:**
| Field | Type | Description | Range |
|-------|------|-------------|-------|
| district | string | District/Location name | - |
| water_quality | float | Water quality index | 0-100 |
| temperature | float | Temperature in Celsius | -50 to 50 |
| humidity | float | Humidity percentage | 0-100 |
| rainfall | float | Rainfall in mm | 0-500 |
| population_density | float | Population per sq km | 0-10000 |

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

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| district | string | Input district name |
| disease | string | Predicted disease type |
| risk_level | string | Risk level: low, medium, high |
| predicted_cases | integer | Estimated number of cases |
| timeframe | string | Expected outbreak timeline |
| confidence_score | float | Model confidence (0-1) |

---

### 4. Generic Disease Prediction
**Endpoint:** `POST /api/predictions/`

Make a detailed disease prediction with geographic location.

**Request Body:**
```json
{
    "location": {
        "lat": 28.6139,
        "lon": 77.2090
    },
    "water_quality": 35,
    "temperature": 28,
    "humidity": 75,
    "rainfall": 120,
    "population_density": 5000
}
```

**Response:**
```json
{
    "success": true,
    "prediction": 0.85,
    "location": {
        "lat": 28.6139,
        "lon": 77.2090
    },
    "risk_level": "high"
}
```

---

### 5. Get Prediction History
**Endpoint:** `GET /api/predictions/history`

Get historical predictions for a specific location.

**Query Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| location | string | Yes | Location/District name |
| limit | integer | No | Number of records (default: 100) |

**Example:**
```
GET /api/predictions/history?location=New%20Delhi&limit=50
```

**Response:**
```json
{
    "success": true,
    "location": "New Delhi",
    "predictions": [
        {
            "id": 1,
            "disease": "Cholera",
            "risk_score": 0.85,
            "risk_level": "high",
            "timestamp": "2026-03-10T10:30:45.123456"
        }
    ]
}
```

---

## Alert Management Endpoints

### 6. Get Active Alerts
**Endpoint:** `GET /api/alerts`

Get all active disease outbreak alerts.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| region | string | Filter by region (optional) |
| severity | string | Filter by severity: low, medium, high (optional) |

**Response:**
```json
{
    "success": true,
    "alerts": [
        {
            "id": 1,
            "title": "High cholera risk detected",
            "region": "Region A",
            "severity": "high",
            "message": "Water contamination levels elevated",
            "timestamp": "2026-03-10T10:30:45.123456",
            "affected_population": 10000
        }
    ],
    "count": 1
}
```

---

### 7. Create Alert
**Endpoint:** `POST /api/alerts`

Create a new disease outbreak alert.

**Request Body:**
```json
{
    "title": "Typhoid Outbreak Warning",
    "region": "Mumbai",
    "severity": "high",
    "message": "Water supply contamination detected",
    "affected_population": 50000
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Alert title |
| region | string | Yes | Affected region |
| severity | string | Yes | low, medium, or high |
| message | string | Yes | Alert message/description |
| affected_population | integer | No | Number of affected people |

**Response:**
```json
{
    "success": true,
    "alert": {
        "id": 1,
        "title": "Typhoid Outbreak Warning",
        "region": "Mumbai",
        "severity": "high",
        "message": "Water supply contamination detected",
        "timestamp": "2026-03-10T10:30:45.123456",
        "affected_population": 50000
    }
}
```

---

### 8. Dismiss Alert
**Endpoint:** `DELETE /api/alerts/<alert_id>`

Dismiss/resolve a specific alert.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| alert_id | integer | The alert ID to dismiss |

**Response:**
```json
{
    "success": true,
    "message": "Alert 1 dismissed"
}
```

---

## Risk Map Endpoints

### 9. Get Risk Data
**Endpoint:** `GET /api/maps/risk-data`

Get risk data points for map visualization.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| bounds | string | Bounding box: minLat,minLon,maxLat,maxLon |
| zoom | integer | Zoom level (default: 10) |

**Example:**
```
GET /api/maps/risk-data?bounds=28.5,77.0,28.7,77.3&zoom=12
```

**Response:**
```json
{
    "success": true,
    "risk_points": [
        {
            "lat": 28.6139,
            "lon": 77.2090,
            "risk_score": 0.85,
            "disease": "cholera",
            "intensity": "high"
        },
        {
            "lat": 28.5355,
            "lon": 77.3910,
            "risk_score": 0.65,
            "disease": "typhoid",
            "intensity": "medium"
        }
    ],
    "bounds": "28.5,77.0,28.7,77.3"
}
```

---

### 10. Get Heatmap Data
**Endpoint:** `GET /api/maps/heatmap`

Get heatmap layer data for visualization.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| resolution | string | Resolution: low, medium, high (default: medium) |

**Response:**
```json
{
    "success": true,
    "heatmap": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [77.2090, 28.6139]
                },
                "properties": {
                    "risk_level": 0.85
                }
            }
        ]
    }
}
```

---

### 11. Get Regions
**Endpoint:** `GET /api/maps/regions`

Get region boundaries and statistics.

**Response:**
```json
{
    "success": true,
    "regions": [
        {
            "name": "Region A",
            "risk_score": 0.75,
            "affected_population": 50000,
            "alert_count": 3
        },
        {
            "name": "Region B",
            "risk_score": 0.45,
            "affected_population": 30000,
            "alert_count": 1
        }
    ]
}
```

---

## Error Handling

All endpoints return error responses in this format:

```json
{
    "success": false,
    "error": "Error description"
}
```

**HTTP Status Codes:**
- `200` - OK (Success)
- `201` - Created (Resource created)
- `400` - Bad Request (Invalid parameters)
- `404` - Not Found (Resource not found)
- `500` - Internal Server Error

---

## Usage Examples

### Example 1: Predict Outbreak
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

### Example 2: Get Alerts
```bash
curl http://localhost:5000/api/alerts?severity=high
```

### Example 3: Create Alert
```bash
curl -X POST http://localhost:5000/api/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Cholera Alert",
    "region": "New Delhi",
    "severity": "high",
    "message": "Outbreak detected",
    "affected_population": 10000
  }'
```

### Example 4: Get Risk Data
```bash
curl "http://localhost:5000/api/maps/risk-data?bounds=28.5,77.0,28.7,77.3"
```

---

## Rate Limiting
Currently, no rate limiting is implemented. Add rate limiting middleware for production.

## CORS
CORS is enabled for all origins. Configure for specific domains in production.

## Database
Uses PostgreSQL with SQLAlchemy ORM. Models defined in `database/db.py`.

---

## Support
For issues or questions, check the main README.md or contact the development team.
