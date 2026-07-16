import React, { useState, useEffect } from 'react';
import {
  getAgents,
  createAgent,
  updateAgent,
  deleteAgent,
  getSettings,
  updateSettings,
  triggerSync,
  getSyncStatus,
} from '../services/api';
import Loading from '../components/Loading';

function AdminPage() {
  const [activeTab, setActiveTab] = useState('agents');
  const [agents, setAgents] = useState([]);
  const [settings, setSettings] = useState(null);
  const [syncStatus, setSyncStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  // Form states
  const [newAgent, setNewAgent] = useState({ name: '', email: '', is_active: true });
  const [editingAgent, setEditingAgent] = useState(null);
  const [settingsForm, setSettingsForm] = useState({ jira_url: '', jira_email: '', jira_api_token: '' });

  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'agents') {
        const response = await getAgents();
        setAgents(response.data);
      } else if (activeTab === 'settings') {
        const settingsResponse = await getSettings();
        setSettings(settingsResponse.data.data);
        setSettingsForm(settingsResponse.data.data);
        const statusResponse = await getSyncStatus();
        setSyncStatus(statusResponse.data);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateAgent = async (e) => {
    e.preventDefault();
    try {
      await createAgent(newAgent);
      setSuccess('Agent created successfully');
      setNewAgent({ name: '', email: '', is_active: true });
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to create agent');
      console.error(err);
    }
  };

  const handleDeleteAgent = async (id) => {
    if (window.confirm('Are you sure you want to delete this agent?')) {
      try {
        await deleteAgent(id);
        setSuccess('Agent deleted successfully');
        loadData();
        setTimeout(() => setSuccess(null), 3000);
      } catch (err) {
        setError('Failed to delete agent');
        console.error(err);
      }
    }
  };

  const handleUpdateSettings = async (e) => {
    e.preventDefault();
    try {
      await updateSettings(settingsForm);
      setSuccess('Settings updated successfully');
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to update settings');
      console.error(err);
    }
  };

  const handleSync = async () => {
    try {
      const response = await triggerSync();
      setSuccess(`Sync successful: ${response.data.issues_synced} issues synced`);
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError('Failed to trigger sync');
      console.error(err);
    }
  };

  if (loading && activeTab !== 'agents') return <Loading />;

  return (
    <div className="space-y-6">
      <div className="card">
        <h1 className="text-3xl font-bold mb-4">⚙️ Admin Panel</h1>

        {error && <div className="alert alert-error mb-4">{error}</div>}
        {success && <div className="alert alert-success mb-4">{success}</div>}

        {/* Tabs */}
        <div className="flex space-x-4 mb-6 border-b">
          <button
            onClick={() => setActiveTab('agents')}
            className={`pb-2 px-4 font-semibold ${
              activeTab === 'agents'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            👥 Agents
          </button>
          <button
            onClick={() => setActiveTab('settings')}
            className={`pb-2 px-4 font-semibold ${
              activeTab === 'settings'
                ? 'text-blue-600 border-b-2 border-blue-600'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            🔧 Settings
          </button>
        </div>

        {/* Agents Tab */}
        {activeTab === 'agents' && (
          <div className="space-y-6">
            {/* Add New Agent Form */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-lg font-bold mb-4">Add New Agent</h3>
              <form onSubmit={handleCreateAgent} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="form-group">
                    <label className="form-label">Agent Name</label>
                    <input
                      type="text"
                      value={newAgent.name}
                      onChange={(e) => setNewAgent({ ...newAgent, name: e.target.value })}
                      className="form-input"
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Email</label>
                    <input
                      type="email"
                      value={newAgent.email}
                      onChange={(e) => setNewAgent({ ...newAgent, email: e.target.value })}
                      className="form-input"
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Active</label>
                    <select
                      value={newAgent.is_active}
                      onChange={(e) => setNewAgent({ ...newAgent, is_active: e.target.value === 'true' })}
                      className="form-input"
                    >
                      <option value="true">Active</option>
                      <option value="false">Inactive</option>
                    </select>
                  </div>
                </div>
                <button type="submit" className="btn btn-primary">
                  ➕ Add Agent
                </button>
              </form>
            </div>

            {/* Agents List */}
            <div>
              <h3 className="text-lg font-bold mb-4">Agents List</h3>
              {agents.length === 0 ? (
                <p className="text-gray-600">No agents found.</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="table">
                    <thead>
                      <tr className="bg-gray-100">
                        <th className="px-4 py-2 text-left">Name</th>
                        <th className="px-4 py-2 text-left">Email</th>
                        <th className="px-4 py-2 text-center">Status</th>
                        <th className="px-4 py-2 text-center">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {agents.map((agent) => (
                        <tr key={agent.id} className="border-b hover:bg-gray-50">
                          <td className="px-4 py-2 font-semibold">{agent.name}</td>
                          <td className="px-4 py-2">{agent.email || 'N/A'}</td>
                          <td className="px-4 py-2 text-center">
                            <span
                              className={`badge ${
                                agent.is_active ? 'badge-success' : 'badge-danger'
                              }`}
                            >
                              {agent.is_active ? 'Active' : 'Inactive'}
                            </span>
                          </td>
                          <td className="px-4 py-2 text-center">
                            <button
                              onClick={() => handleDeleteAgent(agent.id)}
                              className="btn btn-danger btn-sm text-xs px-2 py-1"
                            >
                              🗑️ Delete
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="space-y-6">
            {/* Jira Settings Form */}
            <div className="bg-gray-50 p-6 rounded-lg">
              <h3 className="text-lg font-bold mb-4">Jira Configuration</h3>
              <form onSubmit={handleUpdateSettings} className="space-y-4">
                <div className="form-group">
                  <label className="form-label">Jira URL</label>
                  <input
                    type="text"
                    value={settingsForm.jira_url || ''}
                    onChange={(e) => setSettingsForm({ ...settingsForm, jira_url: e.target.value })}
                    className="form-input"
                    placeholder="https://your-domain.atlassian.net"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Email</label>
                  <input
                    type="email"
                    value={settingsForm.jira_email || ''}
                    onChange={(e) => setSettingsForm({ ...settingsForm, jira_email: e.target.value })}
                    className="form-input"
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">API Token</label>
                  <input
                    type="password"
                    value={settingsForm.jira_api_token || ''}
                    onChange={(e) => setSettingsForm({ ...settingsForm, jira_api_token: e.target.value })}
                    className="form-input"
                    placeholder="Enter your Jira API token"
                  />
                </div>
                <button type="submit" className="btn btn-primary">
                  💾 Save Settings
                </button>
              </form>
            </div>

            {/* Sync Section */}
            <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
              <h3 className="text-lg font-bold mb-4">Data Synchronization</h3>
              {syncStatus && (
                <div className="mb-4 text-sm space-y-1">
                  <p className="text-gray-700">
                    <strong>Last Sync:</strong> {syncStatus.last_sync ? new Date(syncStatus.last_sync).toLocaleString() : 'Never'}
                  </p>
                  <p className="text-gray-700">
                    <strong>Total Issues:</strong> {syncStatus.total_issues || 0}
                  </p>
                </div>
              )}
              <button onClick={handleSync} className="btn btn-success">
                🔄 Sync Now
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminPage;
