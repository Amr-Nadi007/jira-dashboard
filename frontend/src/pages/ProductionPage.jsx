import React, { useState, useEffect } from 'react';
import { getProductionDashboard, getProductionDashboardByDate } from '../services/api';
import Loading from '../components/Loading';

function ProductionPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);

  useEffect(() => {
    fetchData();
  }, [selectedDate]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const today = new Date().toISOString().split('T')[0];
      const response = selectedDate === today 
        ? await getProductionDashboard()
        : await getProductionDashboardByDate(selectedDate);
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch production data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;

  return (
    <div className="space-y-6">
      <div className="card">
        <h1 className="text-3xl font-bold mb-4">📈 Production Dashboard</h1>
        
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

        {data && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg border-l-4 border-blue-500">
                <p className="text-gray-600 text-sm">Egypt Total</p>
                <p className="text-3xl font-bold text-blue-600">{data.total_egypt}</p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
                <p className="text-gray-600 text-sm">Nigeria Total</p>
                <p className="text-3xl font-bold text-green-600">{data.total_nigeria}</p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                <p className="text-gray-600 text-sm">Total Issues</p>
                <p className="text-3xl font-bold text-purple-600">{data.total_all}</p>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="table">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="px-4 py-2 text-left">Agent</th>
                    <th className="px-4 py-2 text-center">Egypt</th>
                    <th className="px-4 py-2 text-center">Nigeria</th>
                    <th className="px-4 py-2 text-center">Total</th>
                  </tr>
                </thead>
                <tbody>
                  {data.agents.map((agent, idx) => (
                    <tr key={idx} className="border-b hover:bg-gray-50">
                      <td className="px-4 py-2 font-semibold">{agent.agent}</td>
                      <td className="px-4 py-2 text-center">
                        <span className="badge badge-primary">{agent.egypt}</span>
                      </td>
                      <td className="px-4 py-2 text-center">
                        <span className="badge badge-success">{agent.nigeria}</span>
                      </td>
                      <td className="px-4 py-2 text-center">
                        <span className="badge badge-warning">{agent.total}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default ProductionPage;
