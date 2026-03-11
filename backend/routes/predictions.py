"""
Predictions routes - Disease prediction endpoints.
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from models.disease_model import DiseasePredictor
from models.lstm_disease_model import LSTMDiseasePredictor
from routes.alerts import ALERT_STORE
from realtime import broadcast_alert
from services.surveillance_pipeline import run_live_prediction_pipeline

bp = Blueprint('predictions', __name__, url_prefix='/api/predictions')

predictor = DiseasePredictor()
lstm_predictor = LSTMDiseasePredictor()
PREDICTION_STORE = []


def _default_disease_for_risk(risk_level):
    if risk_level == 'high':
        return 'Cholera'
    if risk_level == 'medium':
        return 'Typhoid'
    return 'Dengue'


def _sync_live_pipeline(force=False):
    """Refresh prediction and alert stores from live surveillance data."""
    water_rows, predictions, alerts = run_live_prediction_pipeline(force=force)

    PREDICTION_STORE.clear()
    PREDICTION_STORE.extend(predictions)

    ALERT_STORE.clear()
    ALERT_STORE.extend(alerts)

    return {
        'water_rows': water_rows,
        'prediction_count': len(predictions),
        'alert_count': len(alerts),
    }


def _predict_risk_and_cases(features, population_density):
    """Predict risk level and case count with fallback if model is unavailable."""
    if hasattr(predictor, 'predict_risk_level') and hasattr(predictor, 'predict_cases'):
        risk_result = predictor.predict_risk_level(features)
        case_result = predictor.predict_cases(features, population=population_density)
        return {
            'risk_level': risk_result.get('risk_level', 'medium'),
            'confidence_score': float(risk_result.get('confidence', 0.5)),
            'risk_score': float(risk_result.get('risk_probability', 0.5)),
            'predicted_cases': int(case_result.get('predicted_cases', 0)),
            'timeframe': '1-2 weeks' if risk_result.get('risk_level') == 'high' else '2-4 weeks',
        }

    # Fallback heuristic if the classifier is not trained yet.
    rainfall, temperature, previous_cases, population_density = features
    risk_score = min(1.0, ((rainfall / 300) + (previous_cases / 1000) + (temperature / 50)) / 3)

    if risk_score >= 0.7:
        risk_level = 'high'
        multiplier = 0.12
        timeframe = '1-2 weeks'
    elif risk_score >= 0.4:
        risk_level = 'medium'
        multiplier = 0.07
        timeframe = '2-4 weeks'
    else:
        risk_level = 'low'
        multiplier = 0.03
        timeframe = '4+ weeks'

    predicted_cases = int(population_density * multiplier * max(risk_score, 0.1))
    return {
        'risk_level': risk_level,
        'confidence_score': round(risk_score, 3),
        'risk_score': round(risk_score, 3),
        'predicted_cases': max(1, predicted_cases),
        'timeframe': timeframe,
    }


@bp.route('/', methods=['GET'])
@bp.route('', methods=['GET'])
@bp.route('/predict', methods=['GET'])
def list_predictions():
    """GET feed for frontend dashboard from live ingestion pipeline."""
    _sync_live_pipeline(force=False)
    return jsonify(PREDICTION_STORE), 200


@bp.route('/refresh', methods=['POST'])
def refresh_predictions():
    """Force-refresh predictions and alerts from live surveillance source."""
    stats = _sync_live_pipeline(force=True)
    return jsonify({'success': True, **stats}), 200


@bp.route('/predict', methods=['POST'])
def predict_outbreak():
    """Create a disease outbreak prediction and emit high-risk alerts in realtime."""
    try:
        data = request.get_json(force=True) or {}

        district = data.get('district', 'Unknown District')
        rainfall = float(data.get('rainfall', 60))
        temperature = float(data.get('temperature', 28))
        previous_cases = int(data.get('previous_cases', 20))
        population_density = float(data.get('population_density', 1000))

        features = [rainfall, temperature, previous_cases, population_density]
        prediction_stats = _predict_risk_and_cases(features, population_density)

        risk_level = prediction_stats['risk_level']
        disease = data.get('disease', _default_disease_for_risk(risk_level))
        prediction_id = (len(PREDICTION_STORE) + 1)

        record = {
            'id': prediction_id,
            'district': district,
            'disease': disease,
            'risk_level': risk_level,
            'risk_score': prediction_stats['risk_score'],
            'confidence_score': prediction_stats['confidence_score'],
            'predicted_cases': prediction_stats['predicted_cases'],
            'timeframe': prediction_stats['timeframe'],
            'date': datetime.utcnow().date().isoformat(),
            'timestamp': datetime.utcnow().isoformat(),
            'latitude': float(data.get('latitude', 22.9734)),
            'longitude': float(data.get('longitude', 78.6569)),
        }
        PREDICTION_STORE.append(record)

        if risk_level == 'high':
            alert = {
                'id': len(ALERT_STORE) + 1,
                'district': district,
                'disease': disease,
                'risk_level': 'high',
                'recommended_action': 'Immediate Action Required',
                'title': f'{disease} outbreak risk in {district}',
                'message': f'High risk predicted with {record["predicted_cases"]} potential cases.',
                'created_at': datetime.utcnow().isoformat(),
                'is_active': True,
            }
            ALERT_STORE.append(alert)
            broadcast_alert(alert)

        return jsonify({'success': True, **record}), 200
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400


@bp.route('/<prediction_id>', methods=['GET'])
def get_prediction(prediction_id):
    """Retrieve a specific prediction."""
    try:
        for item in PREDICTION_STORE:
            if str(item.get('id')) == str(prediction_id):
                return jsonify({'success': True, 'prediction': item}), 200
        return jsonify({'success': False, 'error': 'Prediction not found'}), 404
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400


@bp.route('/history', methods=['GET'])
def get_prediction_history():
    """Get historical predictions for a district."""
    try:
        district = request.args.get('district', '').lower()
        limit = request.args.get('limit', 100, type=int)

        filtered = PREDICTION_STORE
        if district:
            filtered = [item for item in PREDICTION_STORE if item.get('district', '').lower() == district]

        return jsonify({'success': True, 'district': district or 'all', 'predictions': filtered[-limit:]}), 200
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400


@bp.route('/lstm/forecast', methods=['POST'])
def forecast_timeseries_lstm():
    """Forecast future weekly cases using trained LSTM model."""
    try:
        data = request.get_json(force=True) or {}
        history = data.get('historical_cases', [])
        horizon = int(data.get('horizon', 4))

        if not isinstance(history, list) or len(history) < lstm_predictor.config.sequence_length:
            return jsonify({
                'success': False,
                'error': f'historical_cases must be a list with at least {lstm_predictor.config.sequence_length} values'
            }), 400

        try:
            if lstm_predictor.model is None:
                lstm_predictor.load('models/lstm_disease_model.keras', 'models/lstm_scaler.pkl')
        except Exception as load_error:
            return jsonify({
                'success': False,
                'error': f'LSTM model unavailable. Train model first with train_lstm_model.py. Details: {load_error}'
            }), 400

        forecast = lstm_predictor.forecast_next(history, horizon=horizon)
        return jsonify({'success': True, 'horizon': horizon, 'forecast_cases': forecast}), 200
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400


@bp.route('/pipeline/status', methods=['GET'])
def pipeline_status():
    """Return current in-memory pipeline status."""
    return jsonify({
        'success': True,
        'prediction_count': len(PREDICTION_STORE),
        'alert_count': len([item for item in ALERT_STORE if item.get('is_active', True)]),
    }), 200


