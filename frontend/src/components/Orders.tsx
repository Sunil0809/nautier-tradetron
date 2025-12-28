import React, { useState } from 'react'
import { FiX, FiCheck, FiClock } from 'react-icons/fi'

interface Order {
  id: number
  symbol: string
  type: 'BUY' | 'SELL'
  quantity: number
  price: number
  status: 'FILLED' | 'PENDING' | 'REJECTED'
  time: string
  pnl?: number
}

export default function Orders() {
  const [orders, setOrders] = useState<Order[]>([
    {
      id: 1,
      symbol: 'SBIN',
      type: 'BUY',
      quantity: 100,
      price: 580.50,
      status: 'FILLED',
      time: '14:32:45',
      pnl: 250.00,
    },
    {
      id: 2,
      symbol: 'INFY',
      type: 'SELL',
      quantity: 50,
      price: 1820.00,
      status: 'FILLED',
      time: '13:45:22',
      pnl: 500.00,
    },
    {
      id: 3,
      symbol: 'TCS',
      type: 'BUY',
      quantity: 25,
      price: 3950.00,
      status: 'PENDING',
      time: '14:50:10',
    },
    {
      id: 4,
      symbol: 'RELIANCE',
      type: 'BUY',
      quantity: 10,
      price: 2850.00,
      status: 'REJECTED',
      time: '12:30:00',
    },
  ])

  const [killSwitchActive, setKillSwitchActive] = useState(false)

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'FILLED':
        return <span className="badge badge-success">✓ FILLED</span>
      case 'PENDING':
        return <span className="badge badge-warning">⏳ PENDING</span>
      case 'REJECTED':
        return <span className="badge badge-danger">✗ REJECTED</span>
      default:
        return <span className="badge">{status}</span>
    }
  }

  const handleKillSwitch = () => {
    setKillSwitchActive(!killSwitchActive)
    if (!killSwitchActive) {
      alert('🛑 KILL SWITCH ACTIVATED - All trading halted immediately!')
    }
  }

  const totalPnL = orders.filter(o => o.pnl).reduce((sum, o) => sum + (o.pnl || 0), 0)

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>Orders</h2>
        <button
          className={`btn ${killSwitchActive ? 'btn-danger' : 'btn-secondary'}`}
          onClick={handleKillSwitch}
          style={{ fontSize: '1.1rem', fontWeight: 'bold' }}
        >
          🛑 {killSwitchActive ? 'KILL SWITCH ACTIVE' : 'Kill Switch'}
        </button>
      </div>

      {killSwitchActive && (
        <div className="alert alert-danger">
          🛑 <strong>KILL SWITCH ACTIVATED</strong> - All trading is halted. No new orders will be placed.
        </div>
      )}

      <div className="card" style={{ marginBottom: '2rem' }}>
        <h3>Session Summary</h3>
        <div className="grid-2">
          <div>
            <p>
              <strong>Total Orders:</strong> {orders.length}
            </p>
            <p style={{ marginTop: '0.5rem' }}>
              <strong>Filled:</strong> {orders.filter(o => o.status === 'FILLED').length}
            </p>
            <p style={{ marginTop: '0.5rem' }}>
              <strong>Pending:</strong> {orders.filter(o => o.status === 'PENDING').length}
            </p>
          </div>
          <div>
            <p>
              <strong>Total P&L:</strong>{' '}
              <span style={{ color: totalPnL >= 0 ? 'var(--success)' : 'var(--danger)', fontWeight: 'bold' }}>
                ${totalPnL.toFixed(2)}
              </span>
            </p>
            <p style={{ marginTop: '0.5rem' }}>
              <strong>Win Rate:</strong> 100% (2/2 completed)
            </p>
            <p style={{ marginTop: '0.5rem' }}>
              <strong>Avg Trade P&L:</strong> $375.00
            </p>
          </div>
        </div>
      </div>

      <div className="card">
        <h3>Order History</h3>
        <div style={{ overflowX: 'auto' }}>
          <table className="table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Symbol</th>
                <th>Type</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Status</th>
                <th>P&L</th>
              </tr>
            </thead>
            <tbody>
              {orders.map(order => (
                <tr key={order.id}>
                  <td>{order.time}</td>
                  <td style={{ fontWeight: 'bold' }}>{order.symbol}</td>
                  <td>
                    <span
                      style={{
                        color: order.type === 'BUY' ? 'var(--success)' : 'var(--danger)',
                        fontWeight: 'bold',
                      }}
                    >
                      {order.type}
                    </span>
                  </td>
                  <td>{order.quantity}</td>
                  <td>₹{order.price.toFixed(2)}</td>
                  <td>{getStatusBadge(order.status)}</td>
                  <td style={{ color: order.pnl && order.pnl >= 0 ? 'var(--success)' : 'var(--danger)' }}>
                    {order.pnl ? `$${order.pnl.toFixed(2)}` : '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
