import { Link, Route, Routes } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import StrategyBuilderPage from './pages/StrategyBuilderPage'
import BacktestResultsPage from './pages/BacktestResultsPage'
import MarketplacePage from './pages/MarketplacePage'
import PortfolioPage from './pages/PortfolioPage'

const nav = ['Dashboard', 'Strategies', 'Backtests', 'Marketplace', 'Portfolio', 'Settings']

export default function App() {
  return (
    <div className="min-h-screen p-4">
      <header className="mb-6 flex gap-4 rounded-lg bg-slate-900 p-4">
        {nav.map((item) => (
          <Link key={item} className="text-sm text-cyan-300" to={item === 'Dashboard' ? '/' : `/${item.toLowerCase()}`}>
            {item}
          </Link>
        ))}
      </header>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<DashboardPage />} />
        <Route path="/strategies" element={<StrategyBuilderPage />} />
        <Route path="/backtests" element={<BacktestResultsPage />} />
        <Route path="/marketplace" element={<MarketplacePage />} />
        <Route path="/portfolio" element={<PortfolioPage />} />
      </Routes>
    </div>
  )
}
