"""
Dhritrashtra - Water Borne Disease Prediction System
Main Flask application
"""

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database.db import init_db
from routes import predictions, alerts, maps, data_feed
from realtime import socketio
from routes.predictions import PREDICTION_STORE
from routes.alerts import list_active_alerts

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/dhritrashtra')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dhritrashtra-secret-key')

# Initialize extensions
init_db(app)
socketio.init_app(app)

# Register blueprints
app.register_blueprint(predictions.bp)
app.register_blueprint(alerts.bp)
app.register_blueprint(maps.bp)
app.register_blueprint(data_feed.bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'Dhritrashtra API'}, 200


@app.route('/predict', methods=['GET'])
def predict_feed():
    """Compatibility endpoint for frontend feed."""
    return PREDICTION_STORE, 200


@app.route('/alerts', methods=['GET'])
def alert_feed():
    """Compatibility endpoint for frontend alerts feed."""
    return list_active_alerts(), 200


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return {
        'name': 'Dhritrashtra',
        'description': 'Water Borne Disease Prediction System',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            'health': '/api/health',
            'data': {
                'water_quality': 'GET /api/data/water-quality'
            },
            'disease_prediction': {
                'list_predictions': 'GET /api/predictions',
                'detail_prediction': 'POST /api/predictions/',
                'outbreak_prediction': 'POST /api/predictions/predict',
                'get_prediction': 'GET /api/predictions/<id>',
                'prediction_history': 'GET /api/predictions/history?location=<location>'
            },
            'alerts': {
                'get_alerts': 'GET /api/alerts',
                'create_alert': 'POST /api/alerts',
                'dismiss_alert': 'DELETE /api/alerts/<id>'
            },
            'maps': {
                'risk_data': 'GET /api/maps/risk-data',
                'heatmap': 'GET /api/maps/heatmap',
                'regions': 'GET /api/maps/regions'
            },
            'websocket': {
                'connect': 'ws://localhost:5000/socket.io',
                'event': 'outbreak_alert'
            }
        }
    }, 200

if __name__ == '__main__':
    socketio.run(
        app,
        debug=os.getenv('FLASK_ENV') == 'development',
        host='0.0.0.0',
        port=5000,
    )
