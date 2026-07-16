import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import ProductionPage from './pages/ProductionPage';
import ReportsPage from './pages/ReportsPage';
import AdminPage from './pages/AdminPage';
import './index.css';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-gray-50">
        <Navbar />
        <main className="flex-1 container mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/production" element={<ProductionPage />} />
            <Route path="/reports" element={<ReportsPage />} />
            <Route path="/admin" element={<AdminPage />} />
          </Routes>
        </main>
        <footer className="bg-gray-800 text-white text-center py-4 mt-auto">
          <p>&copy; 2024 Jira Cloud Dashboard. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
