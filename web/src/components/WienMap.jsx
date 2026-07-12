import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'

const KATEGORIA_KOLOR = {
  Pałac: '#8a5a1a',
  Muzeum: '#7a5cc7',
  Kościół: '#b5533a',
  Muzyka: '#c8a24a',
  Targ: '#0a8f6b',
  Widok: '#2a7ab5',
  Restauracja: '#c2453a',
}

const LEGENDA = [
  { etykieta: 'Pałac', kolor: KATEGORIA_KOLOR.Pałac },
  { etykieta: 'Muzeum', kolor: KATEGORIA_KOLOR.Muzeum },
  { etykieta: 'Kościół', kolor: KATEGORIA_KOLOR.Kościół },
  { etykieta: 'Muzyka', kolor: KATEGORIA_KOLOR.Muzyka },
  { etykieta: 'Targ', kolor: KATEGORIA_KOLOR.Targ },
  { etykieta: 'Widok', kolor: KATEGORIA_KOLOR.Widok },
  { etykieta: 'Restauracja / kawiarnia', kolor: KATEGORIA_KOLOR.Restauracja },
]

function kolorDla(punkt) {
  if (punkt.rodzaj === 'restauracja') return KATEGORIA_KOLOR.Restauracja
  return KATEGORIA_KOLOR[punkt.kategoria] ?? '#5c3d12'
}

function ikonaDla(punkt) {
  const kolor = kolorDla(punkt)
  return L.divIcon({
    className: 'mapa-pin-wrapper',
    html: `<span class="mapa-pin" style="background:${kolor}"></span>`,
    iconSize: [18, 18],
    iconAnchor: [9, 9],
    popupAnchor: [0, -10],
  })
}

export default function WienMap({ punkty, center }) {
  if (!punkty?.length) return null

  return (
    <div className="map-block">
      <div className="map-wrapper">
        <MapContainer center={center} zoom={13} scrollWheelZoom={false} style={{ height: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {punkty.map((punkt) => (
            <Marker
              key={`${punkt.rodzaj}-${punkt.nazwa}`}
              position={[punkt.lat, punkt.lng]}
              icon={ikonaDla(punkt)}
            >
              <Popup>
                <div className="popup-title">{punkt.nazwa}</div>
                <div>
                  {punkt.dzien ? `Dzień ${punkt.dzien} · ` : ''}
                  {punkt.kategoria}
                </div>
                {punkt.link && (
                  <a href={punkt.link} target="_blank" rel="noreferrer">
                    Otwórz w Google Maps
                  </a>
                )}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>

      <ul className="map-legend">
        {LEGENDA.map((pozycja) => (
          <li key={pozycja.etykieta}>
            <span className="mapa-pin" style={{ background: pozycja.kolor }} />
            {pozycja.etykieta}
          </li>
        ))}
      </ul>
    </div>
  )
}
