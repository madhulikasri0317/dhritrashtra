import React from 'react';

export default function AlertPanel({ alerts }) {
  const getSeverityColors = (severity) => {
    switch ((severity ?? '').toLowerCase()) {
      case 'high':
        return { bg: 'bg-white', border: 'border-l-2 border-rose-700', badge: 'badge-high' };
      case 'medium':
        return { bg: 'bg-white', border: 'border-l-2 border-amber-700', badge: 'badge-medium' };
      case 'low':
        return { bg: 'bg-white', border: 'border-l-2 border-emerald-700', badge: 'badge-low' };
      default:
        return { bg: 'bg-white', border: 'border-l-2 border-slate-500', badge: 'bg-slate-100 text-slate-700' };
    }
  };

  return (
    <div className="space-y-3">
      {alerts.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-8 bg-slate-50 rounded-lg border-2 border-dashed border-slate-300">
          <p className="text-slate-600 font-medium">No active disease alerts.</p>
          <p className="text-sm text-slate-500">Alerts appear only when high-risk predictions trigger operational advisories.</p>
        </div>
      ) : (
        alerts.map((alert) => {
          const colors = getSeverityColors(alert.riskLevel);
          return (
            <div
              key={alert.id}
              className={`${colors.bg} ${colors.border} rounded-md p-4 border border-slate-200`}
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <h4 className="font-semibold text-sm text-slate-900">
                    {alert.disease} outbreak risk in {alert.district}
                  </h4>
                  <p className="text-xs text-slate-700 mt-2">
                    <span className="font-semibold">Risk Level:</span> {String(alert.riskLevel).toUpperCase()}
                  </p>
                  <p className="text-xs text-slate-700 mt-1">
                    <span className="font-semibold">Recommended Action:</span> {alert.recommendedAction}
                  </p>
                </div>
                <span className={`risk-badge ${colors.badge}`}>
                  {String(alert.riskLevel).toUpperCase()}
                </span>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
}
