import React from 'react';
import Dashboard from './pages/Dashboard';
import RiskMap from './pages/RiskMap';
import PredictionTable from './components/PredictionTable';
import AlertPanel from './components/AlertPanel';
import { getPredictions, getAlerts } from './services/api';
import './index.css';

function App() {
  const navItems = React.useMemo(() => ([
    { path: '/dashboard', label: 'Dashboard' },
    { path: '/prediction', label: 'Prediction Table' },
    { path: '/risk-map', label: 'Risk Map' },
    { path: '/alerts', label: 'Alerts' },
  ]), []);

  const [currentPath, setCurrentPath] = React.useState('/dashboard');
  const [predictions, setPredictions] = React.useState([]);
  const [alerts, setAlerts] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(false);
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

  const normalizePredictions = React.useCallback((predictionData) => {
    return extractPredictionItems(predictionData).map((item, index) => ({
      id: item.id ?? index + 1,
      district: item.district ?? item.location ?? 'Unknown District',
      disease: item.disease ?? 'Unknown Disease',
      riskLevel: (item.risk_level ?? item.riskLevel ?? 'low').toString().toLowerCase(),
      riskScore: Number(item.risk_score ?? item.riskScore ?? item.confidence ?? 0),
      predictedCases: Number(item.predicted_cases ?? item.predictedCases ?? 0),
      date: item.date ?? item.timestamp ?? new Date().toLocaleDateString(),
      latitude: Number(item.latitude ?? item.lat),
      longitude: Number(item.longitude ?? item.lon),
      recommendedAction: item.recommended_action ?? item.recommendedAction ?? 'Escalate district surveillance and water quality checks',
    }));
  }, [extractPredictionItems]);

  const normalizeAlerts = React.useCallback((alertData) => {
    return extractAlertItems(alertData).map((item, index) => ({
      id: item.id ?? index + 1,
      district: item.district ?? item.location ?? 'Unknown District',
      disease: item.disease ?? 'Unknown Disease',
      riskLevel: (item.risk_level ?? item.riskLevel ?? 'medium').toString().toLowerCase(),
      recommendedAction: item.recommended_action ?? item.recommendedAction ?? 'Immediate Action Required',
    }));
  }, [extractAlertItems]);

  const navigateTo = React.useCallback((path) => {
    if (window.location.pathname === path) return;
    window.history.pushState({}, '', path);
    setCurrentPath(path);
  }, []);

  const loadData = React.useCallback(async () => {
    setIsLoading(true);
    setError('');

    try {
      const [predictionResult, alertResult] = await Promise.allSettled([
        getPredictions(),
        getAlerts(),
      ]);

      let nextError = '';

      if (predictionResult.status === 'fulfilled') {
        console.log('Prediction API response:', predictionResult.value);
        console.log('Predictions from backend:', predictionResult.value);
        const normalizedPredictions = normalizePredictions(predictionResult.value);
        console.log(`Normalized prediction rows: ${normalizedPredictions.length}`);
        setPredictions(normalizedPredictions);
      } else {
        console.error('Prediction API request failed:', predictionResult.reason);
        setPredictions([]);
        nextError = 'Unable to fetch prediction data.';
      }

      if (alertResult.status === 'fulfilled') {
        console.log('Alerts API response:', alertResult.value);
        const normalizedAlerts = normalizeAlerts(alertResult.value);
        console.log(`Normalized alert rows: ${normalizedAlerts.length}`);
        setAlerts(normalizedAlerts);
      } else {
        console.error('Alerts API request failed:', alertResult.reason);
        setAlerts([]);
        nextError = nextError ? `${nextError} Alerts could not be loaded.` : 'Alerts could not be loaded.';
      }

      setError(nextError);
    } catch (fetchError) {
      console.error('❌ Failed to load route data:', fetchError);
      setError('Unable to fetch data for this page. Please try again.');
      setPredictions([]);
      setAlerts([]);
    } finally {
      setIsLoading(false);
    }
  }, [normalizeAlerts, normalizePredictions]);

  React.useEffect(() => {
    const onPopState = () => {
      setCurrentPath(window.location.pathname || '/dashboard');
    };

    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  React.useEffect(() => {
    const knownRoutes = new Set(['/dashboard', '/prediction', '/risk-map', '/alerts', '/']);
    const path = window.location.pathname || '/dashboard';

    if (!knownRoutes.has(path) || path === '/') {
      window.history.replaceState({}, '', '/dashboard');
      setCurrentPath('/dashboard');
      return;
    }

    setCurrentPath(path);
  }, []);

  React.useEffect(() => {
    if (currentPath === '/dashboard') return undefined;

    loadData();
    const intervalId = window.setInterval(loadData, 300000);

    return () => {
      window.clearInterval(intervalId);
    };
  }, [currentPath, loadData]);
  const renderPage = () => {
    if (currentPath === '/dashboard') {
      return <Dashboard />;
    }

    if (currentPath === '/prediction') {
      return (
        <section className="page-panel p-6 md:p-8">
          <div className="border-b border-slate-200 pb-4 mb-6">
            <h2 className="section-heading">Prediction Table</h2>
            <p className="section-meta mt-2">District-level prediction records from the live monitoring feed.</p>
          </div>
          {error ? <p className="text-sm text-rose-700 mb-4">{error}</p> : null}
          <PredictionTable predictions={predictions} isLoading={isLoading} />
        </section>
      );
    }

    if (currentPath === '/risk-map') {
      return (
        <section className="page-panel p-6 md:p-8">
          <div className="border-b border-slate-200 pb-4 mb-6">
            <h2 className="section-heading">Risk Map</h2>
            <p className="section-meta mt-2">Geographic monitoring view for current district risk distribution.</p>
          </div>
          {error ? <p className="text-sm text-rose-700 mb-4">{error}</p> : null}
          <RiskMap predictions={predictions} />
        </section>
      );
    }

    if (currentPath === '/alerts') {
      return (
        <section className="page-panel p-6 md:p-8">
          <div className="border-b border-slate-200 pb-4 mb-6">
            <h2 className="section-heading">Alerts</h2>
            <p className="section-meta mt-2">Operational advisories requiring monitoring or response action.</p>
          </div>
          {error ? <p className="text-sm text-rose-700 mb-4">{error}</p> : null}
          {isLoading ? <p className="text-sm text-slate-600">Loading alerts...</p> : <AlertPanel alerts={alerts} />}
        </section>
      );
    }

    return <Dashboard />;
  };

  return (
    <div className="app-shell">
      <div className="min-h-screen">
        <aside className="app-sidebar hidden lg:flex lg:flex-col p-6">
          <div>
            <h1 className="sidebar-title">Dhritrashtra</h1>
            <p className="sidebar-subtitle">Water-borne disease monitoring interface</p>
          </div>

          <nav className="sidebar-nav space-y-1 flex-1">
            {navItems.map((item) => {
              const isActive = currentPath === item.path;

              return (
                <button
                  key={item.path}
                  type="button"
                  onClick={() => navigateTo(item.path)}
                  className={`sidebar-nav-item ${isActive ? 'sidebar-nav-item-active' : ''}`}
                >
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          <div className="sidebar-status">
            <p className="text-xs uppercase tracking-widest text-slate-400">Status</p>
            <p className="mt-3 text-sm text-slate-100">Live data feed active</p>
            <p className="text-xs text-slate-300 mt-2">Operational update interval: 5 minutes</p>
          </div>
        </aside>

        <main className="app-content">
          {renderPage()}
        </main>
      </div>
    </div>
  );
}

export default App;
