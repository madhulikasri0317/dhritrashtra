"""Live surveillance ingestion and prediction pipeline using public API data."""

from datetime import datetime, timedelta
import requests


SURVEILLANCE_API_URL = "https://disease.sh/v3/covid-19/gov/India"
REFRESH_INTERVAL_SECONDS = 300

_CACHE = {
    "last_fetch": None,
    "water_data": [],
}


_STATE_COORDINATES = {
    "Andhra Pradesh": (15.9129, 79.74),
    "Bihar": (25.0961, 85.3131),
    "Delhi": (28.7041, 77.1025),
    "Gujarat": (22.2587, 71.1924),
    "Karnataka": (15.3173, 75.7139),
    "Kerala": (10.8505, 76.2711),
    "Maharashtra": (19.7515, 75.7139),
    "Rajasthan": (27.0238, 74.2179),
    "Tamil Nadu": (11.1271, 78.6569),
    "Uttar Pradesh": (26.8467, 80.9462),
    "West Bengal": (22.9868, 87.855),
}


def _safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _risk_level_from_score(score):
    if score >= 0.7:
        return "high"
    if score >= 0.4:
        return "medium"
    return "low"


def _disease_from_contamination(score):
    if score >= 0.8:
        return "Cholera"
    if score >= 0.6:
        return "Typhoid"
    if score >= 0.45:
        return "Hepatitis A"
    return "Dysentery"


def fetch_water_quality_data(force=False):
    now = datetime.utcnow()
    last_fetch = _CACHE.get("last_fetch")

    if (
        not force
        and last_fetch is not None
        and (now - last_fetch) < timedelta(seconds=REFRESH_INTERVAL_SECONDS)
    ):
        return list(_CACHE.get("water_data", []))

    response = requests.get(SURVEILLANCE_API_URL, timeout=30)
    response.raise_for_status()
    payload = response.json()
    states = payload.get("states", [])

    water_rows = []
    timestamp = now.isoformat()

    for item in states:
        district = str(item.get("state", "")).strip()
        if not district:
            continue

        total_cases = _safe_int(item.get("cases"))
        active_cases = _safe_int(item.get("active"))
        today_cases = _safe_int(item.get("todayCases"))

        if total_cases <= 0:
            continue

        active_ratio = active_cases / max(total_cases, 1)
        today_pressure = min(1.0, today_cases / 18.0)
        active_pressure = min(1.0, active_cases / 75.0)
        contamination_level = min(
            1.0,
            max(0.0, (today_pressure * 0.75) + (active_pressure * 0.2) + (active_ratio * 0.05)),
        )

        lat, lon = _STATE_COORDINATES.get(district, (22.9734, 78.6569))
        water_rows.append(
            {
                "district": district,
                "contamination_level": round(contamination_level, 4),
                "reported_cases": total_cases,
                "active_cases": active_cases,
                "today_cases": today_cases,
                "latitude": lat,
                "longitude": lon,
                "timestamp": timestamp,
            }
        )

    _CACHE["last_fetch"] = now
    _CACHE["water_data"] = water_rows

    print("Fetched water data:", len(water_rows))
    return list(water_rows)


def generate_predictions(water_rows):
    predictions = []
    timestamp = datetime.utcnow().isoformat()
    date_value = datetime.utcnow().date().isoformat()

    for index, row in enumerate(water_rows, start=1):
        risk_score = float(row.get("contamination_level", 0))
        risk_level = _risk_level_from_score(risk_score)
        disease = _disease_from_contamination(risk_score)

        active_cases = _safe_int(row.get("active_cases"))
        today_cases = _safe_int(row.get("today_cases"))
        predicted_cases = max(1, int((today_cases * 2.5) + (active_cases * 0.02)))

        predictions.append(
            {
                "id": index,
                "district": row.get("district", "Unknown District"),
                "disease": disease,
                "risk_level": risk_level,
                "risk_score": round(risk_score, 3),
                "confidence_score": round(min(1.0, 0.45 + risk_score / 2), 3),
                "predicted_cases": predicted_cases,
                "timeframe": "1-2 weeks" if risk_level == "high" else "2-4 weeks" if risk_level == "medium" else "4+ weeks",
                "date": date_value,
                "timestamp": timestamp,
                "latitude": row.get("latitude", 22.9734),
                "longitude": row.get("longitude", 78.6569),
            }
        )

    print("Generated predictions:", len(predictions))
    return predictions


def generate_alerts(predictions):
    alerts = []
    timestamp = datetime.utcnow().isoformat()

    for prediction in predictions:
        if prediction.get("risk_level") != "high":
            continue

        district = prediction.get("district", "Unknown District")
        disease = prediction.get("disease", "Unknown Disease")
        predicted_cases = _safe_int(prediction.get("predicted_cases"))

        alerts.append(
            {
                "id": len(alerts) + 1,
                "district": district,
                "disease": disease,
                "risk_level": "high",
                "recommended_action": "Immediate Action Required",
                "title": f"{disease} outbreak risk in {district}",
                "message": f"High risk predicted with {predicted_cases} potential cases.",
                "created_at": timestamp,
                "is_active": True,
            }
        )

    print("Generated alerts:", len(alerts))
    return alerts


def run_live_prediction_pipeline(force=False):
    water_rows = fetch_water_quality_data(force=force)
    predictions = generate_predictions(water_rows)
    alerts = generate_alerts(predictions)
    return water_rows, predictions, alerts
