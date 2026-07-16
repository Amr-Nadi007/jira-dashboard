import React, { useState, useEffect } from 'react';
import { getReportsByDate, getMorningReport, getNightReport } from '../services/api';
import Loading from '../components/Loading';

function ReportsPage() {
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [reports, setReports] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchReports();
  }, [selectedDate]);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const response = await getReportsByDate(selectedDate);
      setReports(response.data.reports);
      setError(null);
    } catch (err) {
      setError('Failed to fetch reports');
      console.error(err);
      setReports([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;

  return (
    <div className="space-y-6">
      <div className="card">
        <h1 className="text-3xl font-bold mb-4">📋 Reports</h1>

        <div className="mb-6">
          <label className="form-label">Select Date:</label>
          <input
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="form-input"
          />
        </div>

        {error && <div className="alert alert-error">{error}</div>}

        {reports && reports.length === 0 ? (
          <div className="alert alert-info">No reports available for the selected date.</div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {reports.map((report, idx) => (
              <div
                key={idx}
                className={`card border-l-4 ${
                  report.report_type === 'morning' ? 'border-yellow-400' : 'border-indigo-400'
                }`}
              >
                <div className="card-header">
                  <h2 className="text-xl font-bold capitalize">
                    {report.report_type === 'morning' ? '🌅' : '🌙'} {report.report_type} Report
                  </h2>
                  <p className="text-gray-500 text-sm mt-1">Date: {report.report_date}</p>
                </div>

                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-yellow-50 p-3 rounded">
                      <p className="text-xs text-gray-600 font-semibold">Egypt TO DO</p>
                      <p className="text-2xl font-bold text-yellow-600">{report.egypt_todo}</p>
                    </div>
                    <div className="bg-blue-50 p-3 rounded">
                      <p className="text-xs text-gray-600 font-semibold">Egypt IN PROGRESS</p>
                      <p className="text-2xl font-bold text-blue-600">{report.egypt_in_progress}</p>
                    </div>
                    <div className="bg-green-50 p-3 rounded">
                      <p className="text-xs text-gray-600 font-semibold">Nigeria TO DO</p>
                      <p className="text-2xl font-bold text-green-600">{report.nigeria_todo}</p>
                    </div>
                    <div className="bg-purple-50 p-3 rounded">
                      <p className="text-xs text-gray-600 font-semibold">Nigeria IN PROGRESS</p>
                      <p className="text-2xl font-bold text-purple-600">{report.nigeria_in_progress}</p>
                    </div>
                  </div>

                  <div className="bg-gray-50 p-3 rounded border">
                    <p className="text-xs text-gray-600 font-semibold mb-2">Report Content:</p>
                    <pre className="text-xs whitespace-pre-wrap text-gray-700 font-mono">
                      {report.content}
                    </pre>
                  </div>

                  <p className="text-xs text-gray-500">
                    Generated: {new Date(report.created_at).toLocaleString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ReportsPage;
