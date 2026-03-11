"""
Maps routes - Risk map data and visualization.
"""

from flask import Blueprint, request, jsonify
from routes.predictions import PREDICTION_STORE
from services.surveillance_pipeline import run_live_prediction_pipeline

bp = Blueprint('maps', __name__, url_prefix='/api/maps')


def _ensure_predictions():
    if PREDICTION_STORE:
        return

    _, predictions, _ = run_live_prediction_pipeline(force=False)
    PREDICTION_STORE.clear()
    PREDICTION_STORE.extend(predictions)


@bp.route('/risk-data', methods=['GET'])
def get_risk_data():
    """Get risk points for map visualization from live predictions."""
    try:
        bounds = request.args.get('bounds')
        _ensure_predictions()

        risk_points = [
            {
                'lat': item.get('latitude', 22.9734),
                'lon': item.get('longitude', 78.6569),
                'risk_score': item.get('risk_score', 0),
                'disease': item.get('disease', '').lower(),
                'intensity': item.get('risk_level', 'low'),
                'district': item.get('district', 'Unknown District'),
            }
            for item in PREDICTION_STORE
        ]

        return jsonify({'success': True, 'risk_points': risk_points, 'bounds': bounds}), 200
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400


@bp.route('/heatmap', methods=['GET'])
def get_heatmap_data():
    """Get heatmap feature collection from live predictions."""
    try:
        _ = request.args.get('resolution', 'medium')
        _ensure_predictions()

        features = [
            {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [item.get('longitude', 78.6569), item.get('latitude', 22.9734)],
                },
                'properties': {
                    'district': item.get('district', 'Unknown District'),
                    'risk_level': item.get('risk_score', 0),
                    'disease': item.get('disease', 'Unknown Disease'),
                },
            }
            for item in PREDICTION_STORE
        ]

        return jsonify({'success': True, 'heatmap': {'type': 'FeatureCollection', 'features': features}}), 200
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400


@bp.route('/regions', methods=['GET'])
def get_regions():
    """Get region-level statistics from live prediction rows."""
    try:
        _ensure_predictions()

        regions = [
            {
                'name': item.get('district', 'Unknown District'),
                'risk_score': item.get('risk_score', 0),
                'affected_population': int(item.get('predicted_cases', 0)),
                'alert_count': 1 if item.get('risk_level') == 'high' else 0,
            }
            for item in PREDICTION_STORE
        ]

        return jsonify({'success': True, 'regions': regions}), 200
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400
