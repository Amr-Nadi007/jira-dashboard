import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="bg-gray-900 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold text-blue-400">
            📊 Jira Dashboard
          </Link>
          <ul className="flex space-x-6">
            <li>
              <Link to="/" className="hover:text-blue-400 transition">
                Dashboard
              </Link>
            </li>
            <li>
              <Link to="/production" className="hover:text-blue-400 transition">
                Production
              </Link>
            </li>
            <li>
              <Link to="/reports" className="hover:text-blue-400 transition">
                Reports
              </Link>
            </li>
            <li>
              <Link to="/admin" className="hover:text-blue-400 transition">
                Admin
              </Link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
