import React, { useState, useEffect } from 'react'
import './App.css'
import Dashboard from './components/Dashboard'
import StrategyBuilder from './components/StrategyBuilder'
import Orders from './components/Orders'
import Navigation from './components/Navigation'

type Page = 'dashboard' | 'strategies' | 'orders' | 'settings'

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard')
  const [apiStatus, setApiStatus] = useState<'connected' | 'disconnected'>('disconnected')

  useEffect(() => {
    // Check API connection
    fetch('http://localhost:8000/health')
      .then(() => setApiStatus('connected'))
      .catch(() => setApiStatus('disconnected'))
  }, [])

  return (
    <div className="app">
      <Navigation 
        currentPage={currentPage} 
        onNavigate={setCurrentPage}
        apiStatus={apiStatus}
      />
      
      <main className="main-content">
        {currentPage === 'dashboard' && <Dashboard />}
        {currentPage === 'strategies' && <StrategyBuilder />}
        {currentPage === 'orders' && <Orders />}
      </main>
    </div>
  )
}
