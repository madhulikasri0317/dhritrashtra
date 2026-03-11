import React from 'react';
import PredictionTable from '../components/PredictionTable';
import AlertPanel from '../components/AlertPanel';
import RiskMap from './RiskMap';
import { getPredictions, getAlerts } from '../services/api';

export default function Dashboard() {
  const [predictions, setPredictions] = React.useState([]);
  const [alerts, setAlerts] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState('');

  const extractPredictionItems = React.useCallback((responseData) => {
    if (Array.isArray(responseData)) {
      return responseData;
    }

    if (Array.isArray(responseData?.predictions)) {
      return responseData.predictions;
    }

    if (Array.isArray(responseData?.data)) {
      return responseData.data;
    }

    return [];
  }, []);

  const extractAlertItems = React.useCallback((responseData) => {
    if (Array.isArray(responseData)) {
      return responseData;
    }

    if (Array.isArray(responseData?.alerts)) {
      return responseData.alerts;
    }

    if (Array.isArray(responseData?.data)) {
      return responseData.data;
    }

    return [];
  }, []);

  React.useEffect(() => {
    const loadDashboardData = async () => {
      setIsLoading(true);
      setError('');
      try {
        const [predictionData, alertData] = await Promise.all([
          getPredictions(),
          getAlerts(),
        ]);

        console.log('Prediction API response:', predictionData);
        console.log('Predictions from backend:', predictionData);
        console.log('Alerts API response:', alertData);

        const normalizedPredictions = extractPredictionItems(predictionData).map((item, index) => ({
          id: item.id ?? index + 1,
          district: item.district ?? item.location ?? 'Unknown District',
          disease: item.disease ?? 'Unknown Disease',
          riskLevel: (item.risk_level ?? item.riskLevel ?? 'low').toString().toLowerCase(),
          riskScore: Number(item.risk_score ?? item.riskScore ?? item.confidence ?? 0.3),
          predictedCases: Number(item.predicted_cases ?? item.predictedCases ?? 0),
          date: item.date ?? item.timestamp ?? new Date().toLocaleDateString(),
          latitude: Number(item.latitude ?? item.lat ?? 22.9734),
          longitude: Number(item.longitude ?? item.lon ?? 78.6569),
        }));

        const normalizedAlerts = extractAlertItems(alertData).map((item, index) => ({
          id: item.id ?? index + 1,
          district: item.district ?? item.location ?? 'Unknown District',
          disease: item.disease ?? 'Unknown Disease',
          riskLevel: (item.risk_level ?? item.riskLevel ?? 'medium').toString().toLowerCase(),
          recommendedAction: item.recommended_action ?? item.recommendedAction ?? 'Immediate Action Required',
        }));

        setPredictions(normalizedPredictions);
        setAlerts(normalizedAlerts);
      } catch (fetchError) {
        setError('Unable to fetch live data from backend.');
        setPredictions([]);
        setAlerts([]);
      } finally {
        setIsLoading(false);
      }
    };

    loadDashboardData();

    const intervalId = window.setInterval(loadDashboardData, 300000);
    return () => {
      window.clearInterval(intervalId);
    };
  }, [extractAlertItems, extractPredictionItems]);
  const highRiskCount = predictions.filter((p) => p.riskLevel === 'high').length;
  const totalCases = predictions.reduce((sum, p) => sum + p.predictedCases, 0);

  const StatCard = ({ label, value, note }) => (
    <div className="metric-card">
      <p className="metric-label">{label}</p>
      <p className="metric-value">{value}</p>
      <p className="metric-note">{note}</p>
    </div>
  );

  return (
    <div className="space-y-6">
      <div id="overview" className="page-panel px-6 py-6 md:px-8 md:py-7">
        <p className="text-xs font-semibold tracking-[0.18em] uppercase text-slate-500">Operational Monitoring Dashboard</p>
        <h1 className="text-3xl md:text-4xl font-semibold text-slate-900 mt-2">National Water-Borne Disease Monitoring</h1>
        <p className="section-meta mt-3 max-w-3xl">Integrated district surveillance, prediction review, and alert monitoring for government response teams.</p>
        {error ? <p className="text-sm text-amber-700 mt-4">{error}</p> : null}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <StatCard
          label="Districts Monitored"
          value={predictions.length}
          note="Active districts in current feed"
        />
        <StatCard
          label="High Risk Areas"
          value={highRiskCount}
          note="Districts flagged for intervention"
        />
        <StatCard
          label="Alerts Issued"
          value={alerts.length}
          note="Current operational advisories"
        />
        <StatCard
          label="Current Cases"
          value={totalCases}
          note="Aggregate predicted case volume"
        />
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div id="predictions" className="xl:col-span-2 page-panel p-6 md:p-7">
          <div className="flex items-center justify-between mb-6 border-b border-slate-200 pb-4">
            <div>
              <h2 className="section-heading">Prediction Table</h2>
              <p className="section-meta mt-1">Live district prediction output.</p>
            </div>
            <span className="text-xs bg-slate-100 text-slate-700 px-3 py-1 rounded-sm font-medium border border-slate-200">
              {predictions.length} predictions
            </span>
          </div>
          <PredictionTable predictions={predictions} isLoading={isLoading} />
        </div>

        <div id="alerts" className="page-panel p-6 md:p-7">
          <div className="flex items-center justify-between mb-6 border-b border-slate-200 pb-4">
            <div>
              <h2 className="section-heading">Alerts</h2>
              <p className="section-meta mt-1">Current response advisories.</p>
            </div>
            <span className="text-xs bg-slate-100 text-slate-700 px-3 py-1 rounded-sm font-medium border border-slate-200">
              {alerts.length} alerts
            </span>
          </div>
          <AlertPanel alerts={alerts} />
        </div>
      </div>

      <div id="risk-map" className="page-panel p-6 md:p-7">
        <div className="flex items-center justify-between mb-6 border-b border-slate-200 pb-4">
          <div>
            <h2 className="section-heading">Risk Map</h2>
            <p className="section-meta mt-1">Current geographic risk distribution.</p>
          </div>
          <span className="text-xs bg-slate-100 text-slate-700 px-3 py-1 rounded-sm font-medium border border-slate-200">India Overview</span>
        </div>
        <RiskMap predictions={predictions} />
      </div>
    </div>
  );
}
