import React from 'react'
import { FiHome, FiTrendingUp, FiShoppingCart, FiSettings, FiCheckCircle, FiXCircle } from 'react-icons/fi'

interface NavigationProps {
  currentPage: 'dashboard' | 'strategies' | 'orders' | 'settings'
  onNavigate: (page: 'dashboard' | 'strategies' | 'orders' | 'settings') => void
  apiStatus: 'connected' | 'disconnected'
}

export default function Navigation({ currentPage, onNavigate, apiStatus }: NavigationProps) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <h1>📊 Algo Trading Platform</h1>
        </div>

        <div className="navbar-menu">
          <button
            className={`nav-item ${currentPage === 'dashboard' ? 'active' : ''}`}
            onClick={() => onNavigate('dashboard')}
          >
            <FiHome /> Dashboard
          </button>
          <button
            className={`nav-item ${currentPage === 'strategies' ? 'active' : ''}`}
            onClick={() => onNavigate('strategies')}
          >
            <FiTrendingUp /> Strategies
          </button>
          <button
            className={`nav-item ${currentPage === 'orders' ? 'active' : ''}`}
            onClick={() => onNavigate('orders')}
          >
            <FiShoppingCart /> Orders
          </button>
        </div>

        <div className="navbar-status">
          {apiStatus === 'connected' ? (
            <div className="status-indicator connected">
              <FiCheckCircle /> Backend Connected
            </div>
          ) : (
            <div className="status-indicator disconnected">
              <FiXCircle /> Backend Offline
            </div>
          )}
        </div>
      </div>

      <style>{`
        .navbar {
          background: var(--bg-light);
          border-bottom: 1px solid var(--border-color);
          padding: 0;
        }

        .navbar-container {
          max-width: 1600px;
          margin: 0 auto;
          padding: 1rem 2rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 2rem;
        }

        .navbar-brand h1 {
          font-size: 1.5rem;
          color: var(--primary);
          white-space: nowrap;
        }

        .navbar-menu {
          display: flex;
          gap: 0.5rem;
          flex: 1;
        }

        .nav-item {
          background: transparent;
          border: none;
          color: var(--text-secondary);
          padding: 0.75rem 1.5rem;
          cursor: pointer;
          font-weight: 500;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          transition: all 0.3s ease;
          border-radius: 6px;
        }

        .nav-item:hover {
          color: var(--primary);
          background: rgba(0, 102, 204, 0.1);
        }

        .nav-item.active {
          color: var(--primary);
          background: rgba(0, 102, 204, 0.2);
        }

        .navbar-status {
          display: flex;
          gap: 1rem;
        }

        .status-indicator {
          padding: 0.75rem 1rem;
          border-radius: 6px;
          font-size: 0.9rem;
          font-weight: 600;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          white-space: nowrap;
        }

        .status-indicator.connected {
          background: rgba(0, 170, 0, 0.2);
          color: var(--success);
        }

        .status-indicator.disconnected {
          background: rgba(204, 0, 0, 0.2);
          color: var(--danger);
        }

        @media (max-width: 768px) {
          .navbar-container {
            flex-direction: column;
            gap: 1rem;
            padding: 1rem;
          }

          .navbar-brand h1 {
            font-size: 1.2rem;
          }

          .navbar-menu {
            width: 100%;
          }

          .nav-item {
            flex: 1;
            justify-content: center;
          }

          .navbar-status {
            width: 100%;
            justify-content: center;
          }

          .status-indicator {
            font-size: 0.8rem;
          }
        }
      `}</style>
    </nav>
  )
}
