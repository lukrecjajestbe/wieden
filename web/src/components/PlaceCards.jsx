import { useMemo, useState } from 'react'

export default function PlaceCards({ tytul, punkty, filtruj = true }) {
  const [filtr, setFiltr] = useState('wszystkie')

  const kategorie = useMemo(() => {
    const zbior = new Set(punkty.map((p) => p.kategoria).filter(Boolean))
    return ['wszystkie', ...Array.from(zbior)]
  }, [punkty])

  const widoczne =
    !filtruj || filtr === 'wszystkie'
      ? punkty
      : punkty.filter((p) => p.kategoria === filtr)

  if (!punkty?.length) return null

  return (
    <div className="places">
      <h3 className="places-title">{tytul}</h3>

      {filtruj && kategorie.length > 2 && (
        <div className="filters">
          {kategorie.map((k) => (
            <button
              key={k}
              className={`filter-button ${filtr === k ? 'active' : ''}`}
              onClick={() => setFiltr(k)}
            >
              {k === 'wszystkie' ? 'Wszystkie' : k}
            </button>
          ))}
        </div>
      )}

      <div className="card-grid">
        {widoczne.map((punkt) => (
          <div className="card" key={punkt.nazwa}>
            {punkt.image && (
              <img
                className="card-image"
                src={`${import.meta.env.BASE_URL}${punkt.image}`}
                alt={punkt.nazwa}
                loading="lazy"
              />
            )}
            <div className="card-body">
              <h4 className="card-title">
                {punkt.nazwa}
                {punkt.kategoria && (
                  <span className="badge badge-kategoria">{punkt.kategoria}</span>
                )}
              </h4>
              {punkt.opis && <p className="card-text">{punkt.opis}</p>}
              {punkt.link && (
                <div className="card-links">
                  <a href={punkt.link} target="_blank" rel="noreferrer">
                    📍 Google Maps
                  </a>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
