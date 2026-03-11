import React from 'react';

export default function PredictionTable({ predictions, isLoading = false }) {
  const predictionRows = Array.isArray(predictions) ? predictions : [];

  const getRiskColor = (riskLevel) => {
    switch ((riskLevel ?? '').toLowerCase()) {
      case 'high': return { badge: 'risk-badge risk-high' };
      case 'medium': return { badge: 'risk-badge risk-medium' };
      case 'low': return { badge: 'risk-badge risk-low' };
      default: return { badge: 'risk-badge' };
    }
  };

  const getRiskBarColor = (riskLevel) => {
    switch ((riskLevel ?? '').toLowerCase()) {
      case 'high': return '#b91c1c';
      case 'medium': return '#b45309';
      case 'low': return '#166534';
      default: return '#64748b';
    }
  };

  if (isLoading) {
    return <p className="text-sm text-slate-600">Loading predictions...</p>;
  }

  if (predictionRows.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 bg-slate-50 rounded-lg border-2 border-dashed border-slate-300">
        <p className="text-slate-600 font-medium text-lg">No predictions available from the prediction engine.</p>
        <p className="text-sm text-slate-500 mt-2">Check back later or verify your API connection</p>
      </div>
    );
  }

  return (
    <div className="table-shell">
      <table className="monitor-table">
        <thead>
          <tr>
            <th>District</th>
            <th>Disease</th>
            <th>Risk Score</th>
            <th>Risk Level</th>
            <th>Predicted Cases</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {predictionRows.map((prediction) => {
            const colorClasses = getRiskColor(prediction.riskLevel);
            const barColor = getRiskBarColor(prediction.riskLevel);
            return (
              <tr key={prediction.id}>
                <td className="font-medium text-slate-900">{prediction.district}</td>
                <td>{prediction.disease}</td>
                <td>
                  <div className="flex items-center gap-3">
                    <div className="risk-bar-track">
                      <div
                        className="risk-bar-fill"
                        style={{ width: `${prediction.riskScore * 100}%`, backgroundColor: barColor }}
                      ></div>
                    </div>
                    <span className="w-12 text-sm font-semibold text-slate-700">
                      {(prediction.riskScore * 100).toFixed(0)}%
                    </span>
                  </div>
                </td>
                <td>
                  <span className={colorClasses.badge}>
                    {prediction.riskLevel}
                  </span>
                </td>
                <td className="font-medium text-slate-900">
                  {prediction.predictedCases || 0}
                </td>
                <td className="text-slate-600">{prediction.date}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
