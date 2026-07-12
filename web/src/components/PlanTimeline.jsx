import MarkdownText from './MarkdownText'
import WienMap from './WienMap'
import PlaceCards from './PlaceCards'

function imageForDay(dzien) {
  return dzien.image ? `${import.meta.env.BASE_URL}${dzien.image}` : null
}

function punktyMapy(plan) {
  const atrakcje = (plan.atrakcje ?? []).map((p) => ({ ...p, rodzaj: 'atrakcja' }))
  const restauracje = (plan.restauracje ?? []).map((p) => ({
    ...p,
    rodzaj: 'restauracja',
  }))
  return [...atrakcje, ...restauracje]
}

function srodekMapy(punkty) {
  if (!punkty.length) return [48.2082, 16.3738]
  const lat = punkty.reduce((s, p) => s + p.lat, 0) / punkty.length
  const lng = punkty.reduce((s, p) => s + p.lng, 0) / punkty.length
  return [lat, lng]
}

export default function PlanTimeline({ plan }) {
  const punkty = punktyMapy(plan)
  const atrakcje = plan.atrakcje ?? []
  const restauracje = plan.restauracje ?? []

  return (
    <div>
      <p className="plan-intro">{plan.intro}</p>

      <WienMap punkty={punkty} center={srodekMapy(punkty)} />

      <div className="dni">
        {plan.dni.map((dzien) => {
          const image = imageForDay(dzien)
          const atrakcjeDnia = atrakcje.filter((a) => a.dzien === dzien.dzien)
          const restauracjeDnia = restauracje.filter((r) => r.dzien === dzien.dzien)
          return (
            <section className="dzien" key={dzien.dzien}>
              <header className="dzien-header">
                {image && (
                  <img
                    className="dzien-header-thumb"
                    src={image}
                    alt={dzien.miejsce}
                    loading="lazy"
                  />
                )}
                <div className="dzien-header-body">
                  <div className="dzien-header-num">
                    Dzień {dzien.dzien}
                    <span className="dzien-header-date">{dzien.data}</span>
                  </div>
                  <div className="dzien-header-place">{dzien.miejsce}</div>
                  <MarkdownText text={dzien.plan} className="dzien-header-plan" />
                </div>
              </header>

              <PlaceCards tytul="Atrakcje" punkty={atrakcjeDnia} filtruj={false} />
              <PlaceCards
                tytul="Gdzie zjeść i napić się kawy"
                punkty={restauracjeDnia}
                filtruj={false}
              />
            </section>
          )
        })}
      </div>

      {plan.uwagi?.length > 0 && (
        <section className="plan-uwagi">
          {plan.uwagi.map((linia, i) => (
            <MarkdownText key={i} text={linia} />
          ))}
        </section>
      )}
    </div>
  )
}
