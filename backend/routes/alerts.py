"""
Alerts routes - Disease outbreak alerts with realtime websocket broadcast.
"""

from datetime import datetime
from flask import Blueprint, jsonify, request
from realtime import broadcast_alert

bp = Blueprint('alerts', __name__, url_prefix='/api/alerts')

ALERT_STORE = []


def list_active_alerts():
    return [alert for alert in ALERT_STORE if alert.get('is_active', True)]


@bp.route('/', methods=['GET'])
@bp.route('', methods=['GET'])
def get_alerts():
    """Get active alerts."""
    try:
        district = request.args.get('district')
        risk_level = request.args.get('risk_level')

        alerts = list_active_alerts()
        if district:
            alerts = [item for item in alerts if item.get('district', '').lower() == district.lower()]
        if risk_level:
            alerts = [item for item in alerts if item.get('risk_level', '').lower() == risk_level.lower()]

        return jsonify({'success': True, 'alerts': alerts, 'count': len(alerts)}), 200
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400


@bp.route('/', methods=['POST'])
@bp.route('', methods=['POST'])
def create_alert():
    """Create and broadcast a new alert."""
    try:
        data = request.get_json(force=True) or {}

        next_id = (max([item['id'] for item in ALERT_STORE]) + 1) if ALERT_STORE else 1
        district = data.get('district', 'Unknown District')
        disease = data.get('disease', 'Unknown Disease')
        risk_level = str(data.get('risk_level', 'medium')).lower()
        recommended_action = data.get('recommended_action', 'Immediate Action Required')

        alert = {
            'id': next_id,
            'district': district,
            'disease': disease,
            'risk_level': risk_level,
            'recommended_action': recommended_action,
            'title': data.get('title', f'{disease} outbreak risk in {district}'),
            'message': data.get('message', f'{risk_level.title()} risk detected for {disease} in {district}.'),
            'created_at': datetime.utcnow().isoformat(),
            'is_active': True,
        }

        ALERT_STORE.append(alert)

        # Push realtime notification to connected clients.
        broadcast_alert(alert)

        return jsonify({'success': True, 'alert': alert}), 201
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400


@bp.route('/<int:alert_id>', methods=['DELETE'])
def dismiss_alert(alert_id):
    """Dismiss an alert."""
    try:
        for alert in ALERT_STORE:
            if alert['id'] == alert_id:
                alert['is_active'] = False
                alert['dismissed_at'] = datetime.utcnow().isoformat()
                return jsonify({'success': True, 'message': f'Alert {alert_id} dismissed'}), 200

        return jsonify({'success': False, 'error': 'Alert not found'}), 404
    except Exception as error:
        return jsonify({'success': False, 'error': str(error)}), 400
