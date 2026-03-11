import React from 'react';
import AlertPanel from '../components/AlertPanel';
import { getAlerts } from '../services/api';

export default function Alerts() {
  const [alerts, setAlerts] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState('');

  React.useEffect(() => {
    const loadAlerts = async () => {
      setIsLoading(true);
      setError('');

      try {
        const response = await getAlerts();
        const alertItems = Array.isArray(response)
          ? response
          : Array.isArray(response?.alerts)
            ? response.alerts
            : [];

        setAlerts(alertItems.map((item, index) => ({
          id: item.id ?? index + 1,
          district: item.district ?? item.location ?? 'Unknown District',
          disease: item.disease ?? 'Unknown Disease',
          riskLevel: (item.risk_level ?? item.riskLevel ?? 'medium').toString().toLowerCase(),
          recommendedAction: item.recommended_action ?? item.recommendedAction ?? 'Immediate Action Required',
        })));
      } catch (loadError) {
        setAlerts([]);
        setError('Unable to fetch live alerts from backend.');
      } finally {
        setIsLoading(false);
      }
    };

    loadAlerts();

    const intervalId = window.setInterval(loadAlerts, 300000);
    return () => {
      window.clearInterval(intervalId);
    };
  }, []);
  return (
    <section className="page-panel p-6 md:p-8">
      <div className="border-b border-slate-200 pb-4 mb-6">
        <h2 className="section-heading">Alerts</h2>
        <p className="section-meta mt-2">Operational advisories generated from live high-risk predictions.</p>
      </div>
      {error ? <p className="text-sm text-rose-700 mb-4">{error}</p> : null}
      {isLoading ? <p className="text-sm text-slate-600">Loading alerts...</p> : <AlertPanel alerts={alerts} />}
    </section>
  );
}
