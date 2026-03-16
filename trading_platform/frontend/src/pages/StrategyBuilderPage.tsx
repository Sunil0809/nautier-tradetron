import { useState } from 'react'

type NodeType = 'indicator' | 'condition' | 'logic' | 'risk' | 'entry' | 'exit'

const palette: NodeType[] = ['indicator', 'condition', 'logic', 'risk', 'entry', 'exit']

export default function StrategyBuilderPage() {
  const [nodes, setNodes] = useState<Array<{ id: string; type: NodeType; x: number; y: number }>>([])

  const addNode = (type: NodeType) => {
    setNodes((prev) => [...prev, { id: crypto.randomUUID(), type, x: 20 + prev.length * 30, y: 20 + prev.length * 20 }])
  }

  return (
    <div className="grid gap-4 md:grid-cols-[220px_1fr]">
      <aside className="rounded bg-slate-900 p-4">
        <h2 className="mb-2 font-semibold">Node Palette</h2>
        {palette.map((p) => (
          <button key={p} className="mb-2 block w-full rounded bg-cyan-700 px-3 py-2 text-left" onClick={() => addNode(p)}>
            {p}
          </button>
        ))}
      </aside>
      <section className="relative min-h-[500px] rounded bg-slate-900 p-2">
        {nodes.map((n) => (
          <div key={n.id} draggable className="absolute w-40 cursor-move rounded border border-cyan-600 bg-slate-800 p-2" style={{ left: n.x, top: n.y }}>
            {n.type.toUpperCase()} Node
          </div>
        ))}
      </section>
    </div>
  )
}
