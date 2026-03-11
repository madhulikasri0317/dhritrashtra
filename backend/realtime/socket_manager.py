from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*", async_mode="threading")


def broadcast_alert(alert_payload):
    """Broadcast alert payload to all connected websocket clients."""
    socketio.emit("outbreak_alert", alert_payload)
