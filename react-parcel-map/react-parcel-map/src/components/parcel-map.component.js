import 'react-leaflet'
import 'leaflet-control-geocoder'
import 'leaflet-control-geocoder/dist/Control.Geocoder.css'
import 'leaflet-control-geocoder/dist/Control.Geocoder.js'
import React, { useState } from 'react'
import {
  MapContainer,
  TileLayer,
  Popup,
  Marker,
  useMapEvents,
  useMap
} from 'react-leaflet'
import { Control } from 'leaflet'
function LocationMarker () {
  const [position, setPosition] = useState(null)
  const [popupContent, setPopupContent] = useState('popup')
  const map = useMap()
  const gc = Control.Geocoder.nominatim()

  console.log('map center:', map.getCenter())
  let timer

  useMapEvents({
    click (e) {
      // only single click
      if (e.originalEvent.detail === 1) {
        timer = setTimeout(() => {
          console.log('click')
          gc.reverse(
            e.latlng,
            map.options.crs.scale(map.getZoom()),
            results => {
              var r = results[0]
              map.flyTo(e.latlng, map.getZoom())
              setPosition(e.latlng)
              if (r) {
                console.log(r)
                // setPopupContent(r.html || r.name).openPopup() // openPopup ruins it for some reason
                // setPopupContent(r.html || r.name)
                console.log(
                  r.properties.address.town || r.properties.address.city
                )
                setPopupContent(r.name)
              }
            }
          )
        }, 200)
      }
      // double click
      if (e.originalEvent.detail === 2) {
        clearTimeout(timer)
        console.log('dblclick')
      }
    }
  })

  return position === null ? null : (
    <Marker position={position}>
      <Popup>{popupContent}</Popup>
    </Marker>
  )
}

function ParcelMap () {
  return (
    <MapContainer
      center={[42.361, -71.057]}
      zoom={13}
      scrollWheelZoom={false}
      style={{ height: '100vh', width: '100wh' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
      />
      <LocationMarker></LocationMarker>
    </MapContainer>
  )
}

export default ParcelMap
