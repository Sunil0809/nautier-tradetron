import React, { useState } from 'react'
import { FiPlus, FiTrash2, FiEdit2 } from 'react-icons/fi'

interface Strategy {
  id: number
  name: string
  type: string
  status: 'active' | 'inactive'
  dailyLoss: number
  maxTrades: number
  rules: string
}

export default function StrategyBuilder() {
  const [strategies, setStrategies] = useState<Strategy[]>([
    {
      id: 1,
      name: 'EMA Crossover',
      type: 'Technical',
      status: 'active',
      dailyLoss: 5000,
      maxTrades: 50,
      rules: 'EMA(9) CROSS_ABOVE EMA(21) AND RSI(14) < 70',
    },
    {
      id: 2,
      name: 'Mean Reversion',
      type: 'Statistical',
      status: 'inactive',
      dailyLoss: 3000,
      maxTrades: 30,
      rules: 'Price > 2StdDev AND Volume > MA(20)',
    },
  ])

  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    type: 'Technical',
    dailyLoss: 5000,
    maxTrades: 50,
    rules: '',
  })

  const handleAddStrategy = () => {
    if (formData.name && formData.rules) {
      const newStrategy: Strategy = {
        id: Math.max(...strategies.map(s => s.id), 0) + 1,
        name: formData.name,
        type: formData.type,
        status: 'inactive',
        dailyLoss: formData.dailyLoss,
        maxTrades: formData.maxTrades,
        rules: formData.rules,
      }
      setStrategies([...strategies, newStrategy])
      setFormData({ name: '', type: 'Technical', dailyLoss: 5000, maxTrades: 50, rules: '' })
      setShowForm(false)
    }
  }

  const handleToggleStrategy = (id: number) => {
    setStrategies(
      strategies.map(s =>
        s.id === id ? { ...s, status: s.status === 'active' ? 'inactive' : 'active' } : s
      )
    )
  }

  const handleDeleteStrategy = (id: number) => {
    setStrategies(strategies.filter(s => s.id !== id))
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h2>Strategy Builder</h2>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          <FiPlus /> New Strategy
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3>Create New Strategy</h3>

          <div className="input-group">
            <label>Strategy Name</label>
            <input
              type="text"
              value={formData.name}
              onChange={e => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g., EMA Crossover Pro"
            />
          </div>

          <div className="grid-2">
            <div className="input-group">
              <label>Type</label>
              <select
                value={formData.type}
                onChange={e => setFormData({ ...formData, type: e.target.value })}
              >
                <option>Technical</option>
                <option>Statistical</option>
                <option>Fundamental</option>
                <option>Hybrid</option>
              </select>
            </div>

            <div className="input-group">
              <label>Max Daily Loss</label>
              <input
                type="number"
                value={formData.dailyLoss}
                onChange={e => setFormData({ ...formData, dailyLoss: Number(e.target.value) })}
              />
            </div>

            <div className="input-group">
              <label>Max Trades/Day</label>
              <input
                type="number"
                value={formData.maxTrades}
                onChange={e => setFormData({ ...formData, maxTrades: Number(e.target.value) })}
              />
            </div>
          </div>

          <div className="input-group">
            <label>Rules (JSON Format)</label>
            <textarea
              rows={8}
              value={formData.rules}
              onChange={e => setFormData({ ...formData, rules: e.target.value })}
              placeholder={'{\n  "name": "EMA Crossover",\n  "conditions": [...],\n  "operator": "AND"\n}'}
              style={{ fontFamily: 'monospace', fontSize: '0.9rem' }}
            />
          </div>

          <div style={{ display: 'flex', gap: '1rem' }}>
            <button className="btn btn-primary" onClick={handleAddStrategy}>
              Create Strategy
            </button>
            <button className="btn btn-secondary" onClick={() => setShowForm(false)}>
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="grid">
        {strategies.map(strategy => (
          <div key={strategy.id} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
              <div>
                <h3>{strategy.name}</h3>
                <span className="badge badge-primary">{strategy.type}</span>
              </div>
              <span
                className={`badge ${strategy.status === 'active' ? 'badge-success' : 'badge-warning'}`}
              >
                {strategy.status.toUpperCase()}
              </span>
            </div>

            <div style={{ marginTop: '1rem', marginBottom: '1rem' }}>
              <p>
                <strong>Max Daily Loss:</strong> ${strategy.dailyLoss}
              </p>
              <p style={{ marginTop: '0.5rem' }}>
                <strong>Max Trades/Day:</strong> {strategy.maxTrades}
              </p>
              <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                <strong>Rules:</strong> {strategy.rules.substring(0, 60)}...
              </p>
            </div>

            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                className={`btn ${strategy.status === 'active' ? 'btn-danger' : 'btn-primary'}`}
                onClick={() => handleToggleStrategy(strategy.id)}
                style={{ flex: 1 }}
              >
                {strategy.status === 'active' ? 'Disable' : 'Enable'}
              </button>
              <button className="btn btn-secondary" style={{ padding: '0.75rem' }}>
                <FiEdit2 />
              </button>
              <button
                className="btn btn-danger"
                onClick={() => handleDeleteStrategy(strategy.id)}
                style={{ padding: '0.75rem' }}
              >
                <FiTrash2 />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
