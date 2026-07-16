import React, { useState, useEffect } from 'react';
import { getDashboardSummary } from '../services/api';
import Loading from '../components/Loading';

function Home() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboard();
    const interval = setInterval(fetchDashboard, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await getDashboardSummary();
      setData(response.data.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="card">
        <h1 className="text-4xl font-bold text-gray-800">📊 Jira Dashboard</h1>
        <p className="text-gray-600 mt-2">Real-time monitoring of DHNON issues</p>
      </div>

      {error && (
        <div className="alert alert-error">
          <strong>Error:</strong> {error}
        </div>
      )}

      {data && (
        <>
          {/* Egypt Section */}
          <div className="card">
            <div className="card-header">
              <h2 className="text-2xl font-bold text-blue-600">🇪🇬 Egypt</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-400">
                <p className="text-gray-600 text-sm font-semibold">TO DO</p>
                <p className="text-5xl font-bold text-yellow-600 mt-2">{data.egypt.todo}</p>
                <p className="text-gray-500 text-xs mt-2">Issues awaiting action</p>
              </div>
              <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-400">
                <p className="text-gray-600 text-sm font-semibold">IN PROGRESS</p>
                <p className="text-5xl font-bold text-blue-600 mt-2">{data.egypt.in_progress}</p>
                <p className="text-gray-500 text-xs mt-2">Currently being worked on</p>
              </div>
            </div>
            <div className="bg-gray-50 p-4 mt-4 rounded-lg">
              <p className="text-gray-600 text-sm">Total: <span className="font-bold text-lg text-gray-800">{data.egypt.total}</span></p>
            </div>
          </div>

          {/* Nigeria Section */}
          <div className="card">
            <div className="card-header">
              <h2 className="text-2xl font-bold text-green-600">🇳🇬 Nigeria</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-yellow-50 p-6 rounded-lg border-l-4 border-yellow-400">
                <p className="text-gray-600 text-sm font-semibold">TO DO</p>
                <p className="text-5xl font-bold text-yellow-600 mt-2">{data.nigeria.todo}</p>
                <p className="text-gray-500 text-xs mt-2">Issues awaiting action</p>
              </div>
              <div className="bg-blue-50 p-6 rounded-lg border-l-4 border-blue-400">
                <p className="text-gray-600 text-sm font-semibold">IN PROGRESS</p>
                <p className="text-5xl font-bold text-blue-600 mt-2">{data.nigeria.in_progress}</p>
                <p className="text-gray-500 text-xs mt-2">Currently being worked on</p>
              </div>
            </div>
            <div className="bg-gray-50 p-4 mt-4 rounded-lg">
              <p className="text-gray-600 text-sm">Total: <span className="font-bold text-lg text-gray-800">{data.nigeria.total}</span></p>
            </div>
          </div>

          {/* Overall Stats */}
          <div className="card">
            <div className="card-header">
              <h2 className="text-2xl font-bold text-purple-600">📈 Overall Statistics</h2>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-yellow-100 p-4 rounded-lg text-center">
                <p className="text-gray-600 text-xs font-semibold uppercase">Total TO DO</p>
                <p className="text-3xl font-bold text-yellow-700 mt-2">
                  {data.total.todo}
                </p>
              </div>
              <div className="bg-blue-100 p-4 rounded-lg text-center">
                <p className="text-gray-600 text-xs font-semibold uppercase">Total In Progress</p>
                <p className="text-3xl font-bold text-blue-700 mt-2">
                  {data.total.in_progress}
                </p>
              </div>
              <div className="bg-purple-100 p-4 rounded-lg text-center">
                <p className="text-gray-600 text-xs font-semibold uppercase">Grand Total</p>
                <p className="text-3xl font-bold text-purple-700 mt-2">
                  {data.total.total}
                </p>
              </div>
              <div className="bg-gray-100 p-4 rounded-lg text-center">
                <p className="text-gray-600 text-xs font-semibold uppercase">Last Updated</p>
                <p className="text-sm font-bold text-gray-700 mt-2">
                  {new Date().toLocaleTimeString()}
                </p>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Help Section */}
      <div className="card bg-blue-50 border-l-4 border-blue-400">
        <h3 className="text-lg font-bold text-blue-800 mb-2">ℹ️ Quick Info</h3>
        <ul className="text-blue-700 space-y-1 text-sm">
          <li>✓ Data refreshes every 30 seconds</li>
          <li>✓ Shows only DHNON project issues</li>
          <li>✓ Organized by Country and Status</li>
          <li>✓ Real-time Jira Cloud integration</li>
        </ul>
      </div>
    </div>
  );
}

export default Home;
