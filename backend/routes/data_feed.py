"""Data feed routes for live ingestion endpoints."""

from flask import Blueprint, jsonify, request
from services.surveillance_pipeline import fetch_water_quality_data


bp = Blueprint("data_feed", __name__, url_prefix="/api/data")


@bp.route("/water-quality", methods=["GET"])
def water_quality_feed():
    """Return latest live water-quality proxy data from surveillance source."""
    try:
        force_refresh = str(request.args.get("refresh", "false")).lower() == "true"
        water_data = fetch_water_quality_data(force=force_refresh)
        return jsonify({"success": True, "count": len(water_data), "data": water_data}), 200
    except Exception as error:
        return jsonify({"success": False, "error": str(error)}), 500
