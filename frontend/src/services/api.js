import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Dashboard API
export const getDashboardStats = () => api.get('/dashboard');
export const getDashboardSummary = () => api.get('/dashboard/summary');

// Production API
export const getProductionDashboard = () => api.get('/production');
export const getProductionDashboardByDate = (date) => api.get(`/production/by-date/${date}`);

// Reports API
export const getMorningReport = () => api.get('/report/morning');
export const getNightReport = () => api.get('/report/night');
export const getReportsByDate = (date) => api.get(`/report/by-date/${date}`);

// Admin API
export const getAgents = () => api.get('/admin/agents');
export const getActiveAgents = () => api.get('/admin/agents/active');
export const createAgent = (agent) => api.post('/admin/agents', agent);
export const updateAgent = (id, agent) => api.put(`/admin/agents/${id}`, agent);
export const deleteAgent = (id) => api.delete(`/admin/agents/${id}`);

// Settings API
export const getSettings = () => api.get('/admin/settings');
export const updateSettings = (settings) => api.post('/admin/settings', settings);

// Sync API
export const triggerSync = () => api.post('/admin/sync');
export const getSyncStatus = () => api.get('/admin/sync-status');

export default api;
