import React, { useState, useEffect } from 'react'
import { FiTrendingUp, FiActivity, FiDollarSign, FiZap } from 'react-icons/fi'

export default function Dashboard() {
  const [stats, setStats] = useState({
    activeStrategies: 0,
    totalOrders: 0,
    dailyPnL: 0,
    portfolio: 0,
  })

  useEffect(() => {
    // Mock stats - in production, fetch from API
    setStats({
      activeStrategies: 3,
      totalOrders: 24,
      dailyPnL: 1250.50,
      portfolio: 45000.00,
    })
  }, [])

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem' }}>Dashboard</h2>

      <div className="stats">
        <div className="stat-card">
          <FiTrendingUp style={{ fontSize: '2rem', color: 'var(--primary)' }} />
          <div className="stat-value">{stats.activeStrategies}</div>
          <div className="stat-label">Active Strategies</div>
        </div>

        <div className="stat-card">
          <FiActivity style={{ fontSize: '2rem', color: 'var(--primary)' }} />
          <div className="stat-value">{stats.totalOrders}</div>
          <div className="stat-label">Total Orders</div>
        </div>

        <div className="stat-card">
          <FiDollarSign style={{ fontSize: '2rem', color: 'var(--success)' }} />
          <div className="stat-value" style={{ color: 'var(--success)' }}>
            ${stats.dailyPnL.toFixed(2)}
          </div>
          <div className="stat-label">Today's P&L</div>
        </div>

        <div className="stat-card">
          <FiZap style={{ fontSize: '2rem', color: 'var(--primary)' }} />
          <div className="stat-value">${stats.portfolio.toFixed(2)}</div>
          <div className="stat-label">Portfolio Value</div>
        </div>
      </div>

      <div className="grid">
        <div className="card">
          <h3>Recent Activity</h3>
          <table className="table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Event</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>14:32:45</td>
                <td>EMA Crossover Strategy Executed</td>
                <td><span className="badge badge-success">FILLED</span></td>
              </tr>
              <tr>
                <td>14:15:22</td>
                <td>Risk Check Passed - Order Placed</td>
                <td><span className="badge badge-success">PASS</span></td>
              </tr>
              <tr>
                <td>14:00:10</td>
                <td>Daily Loss Limit: 15% Remaining</td>
                <td><span className="badge badge-warning">CAUTION</span></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="card">
          <h3>Quick Stats</h3>
          <div style={{ marginTop: '1rem' }}>
            <p>
              <strong>Win Rate:</strong> <span style={{ color: 'var(--success)' }}>68%</span>
            </p>
            <p style={{ marginTop: '0.5rem' }}>
              <strong>Avg Trade:</strong> <span style={{ color: 'var(--primary)' }}>$52.15</span>
            </p>
            <p style={{ marginTop: '0.5rem' }}>
              <strong>Max Drawdown:</strong> <span style={{ color: 'var(--warning)' }}>-$1,200</span>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
