export default function DashboardPage() {
  return (
    <div className="grid gap-4 md:grid-cols-3">
      <div className="rounded bg-slate-900 p-4">Equity Curve</div>
      <div className="rounded bg-slate-900 p-4">Active Strategies</div>
      <div className="rounded bg-slate-900 p-4">Recent Trades</div>
    </div>
  )
}
