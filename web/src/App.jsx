import { useState } from 'react'
import data from './data/data.json'
import PlanTimeline from './components/PlanTimeline'

function App() {
  const [tab, setTab] = useState(data.plany[0]?.id)

  const aktywnyPlan = data.plany.find((p) => p.id === tab) ?? data.plany[0]

  return (
    <>
      <header className="app-header">
        <h1>Wiedeń - plan wycieczki</h1>
        <p>3 dni, 2 osoby - spokojnie, bez sportów</p>
      </header>

      {data.plany.length > 1 && (
        <nav className="tabs">
          {data.plany.map((p) => (
            <button
              key={p.id}
              className={`tab-button ${tab === p.id ? 'active' : ''}`}
              onClick={() => setTab(p.id)}
            >
              {p.label}
            </button>
          ))}
        </nav>
      )}

      <main>{aktywnyPlan && <PlanTimeline plan={aktywnyPlan} />}</main>
    </>
  )
}

export default App
