import React from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const getRiskColor = (riskLevel) => {
  switch ((riskLevel ?? '').toLowerCase()) {
    case 'high':
      return '#dc2626';
    case 'medium':
      return '#eab308';
    case 'low':
      return '#16a34a';
    default:
      return '#64748b';
  }
};

export default function RiskMap({ predictions = [] }) {
  const mapContainer = React.useRef(null);
  const map = React.useRef(null);
  const markersLayer = React.useRef(null);
  const districtData = React.useMemo(() => {
    return (Array.isArray(predictions) ? predictions : [])
      .map((item, index) => ({
        id: item.id ?? index + 1,
        district: item.district ?? item.location ?? 'Unknown District',
        disease: item.disease ?? 'Unknown Disease',
        riskLevel: (item.risk_level ?? item.riskLevel ?? 'low').toString().toLowerCase(),
        predictedCases: Number(item.predicted_cases ?? item.predictedCases ?? 0),
        recommendedAction: item.recommended_action ?? item.recommendedAction ?? 'Escalate district surveillance and water quality checks',
        latitude: Number(item.latitude ?? item.lat),
        longitude: Number(item.longitude ?? item.lon),
      }))
      .filter((item) => Number.isFinite(item.latitude) && Number.isFinite(item.longitude));
  }, [predictions]);

  React.useEffect(() => {
    if (map.current) return;

    map.current = L.map(mapContainer.current, {
      zoomControl: true,
      minZoom: 4,
      maxZoom: 10,
    }).setView([22.9734, 78.6569], 5);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 18,
    }).addTo(map.current);

    markersLayer.current = L.layerGroup().addTo(map.current);

    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, []);

  React.useEffect(() => {
    if (!map.current || !markersLayer.current) return;

    markersLayer.current.clearLayers();

    districtData.forEach((location) => {
      const marker = L.circleMarker([location.latitude, location.longitude], {
        radius: 9,
        fillColor: getRiskColor(location.riskLevel),
        color: '#0f172a',
        weight: 1,
        opacity: 1,
        fillOpacity: 0.85,
      }).addTo(markersLayer.current);

      marker.bindPopup(`
        <strong>${location.district}</strong><br/>
        Disease: ${location.disease}<br/>
        Risk Level: ${String(location.riskLevel).toUpperCase()}<br/>
        Predicted Cases: ${location.predictedCases}<br/>
        Recommended Action: ${location.recommendedAction}
      `);
    });

    if (districtData.length > 0) {
      const bounds = L.latLngBounds(districtData.map((item) => [item.latitude, item.longitude]));
      map.current.fitBounds(bounds, { padding: [24, 24], maxZoom: 7 });
    }

  }, [districtData]);

  return (
    <div className="space-y-4">
      <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
        <h3 className="text-lg font-semibold text-slate-900 mb-3">District Risk Levels</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="flex items-center space-x-3 p-3 bg-rose-50 rounded-lg border border-rose-200">
            <div className="w-5 h-5 bg-rose-600 rounded-full"></div>
            <div>
              <p className="font-semibold text-rose-900">High</p>
              <p className="text-sm text-rose-700">Red</p>
            </div>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-amber-50 rounded-lg border border-amber-200">
            <div className="w-5 h-5 bg-amber-500 rounded-full"></div>
            <div>
              <p className="font-semibold text-amber-900">Medium</p>
              <p className="text-sm text-amber-700">Yellow</p>
            </div>
          </div>
          <div className="flex items-center space-x-3 p-3 bg-emerald-50 rounded-lg border border-emerald-200">
            <div className="w-5 h-5 bg-emerald-600 rounded-full"></div>
            <div>
              <p className="font-semibold text-emerald-900">Low</p>
              <p className="text-sm text-emerald-700">Green</p>
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-slate-200 overflow-hidden">
        <div
          ref={mapContainer}
          className="w-full h-96 md:h-120"
        ></div>
      </div>
    </div>
  );
}
