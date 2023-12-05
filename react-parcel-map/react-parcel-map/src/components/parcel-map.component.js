import 'react-leaflet'
import 'leaflet-control-geocoder'
import 'leaflet-control-geocoder/dist/Control.Geocoder.css'
import 'leaflet-control-geocoder/dist/Control.Geocoder.js'
import React, { useContext, useState } from 'react'
import {
  MapContainer,
  TileLayer,
  Popup,
  Marker,
  useMapEvents,
  useMap
} from 'react-leaflet'
import { Control, LatLng, latLng } from 'leaflet'
import ParcelDataService from '../services/parcel.service'
import { ParcelsContext } from './get-parcel.component'

function getChildParcels (e, owner, setChildParcels) {
  console.log(owner)
  ParcelDataService.findByOwner(owner)
    .then(response => {
      if (response.data.parcels.length == 0) {
        // No parcels found
        console.log('No parcels found')
        return
      }
      console.log(response.data.parcels.length + ' parcels found')
      setChildParcels(response.data.parcels)
    })
    .catch(e => {
      console.log(e)
    })
}

function createMarker (parcel, setChildParcels) {
  return (
    <Marker position={[parcel.x_coord, parcel.y_coord]}>
      <Popup>
        <div>
          {parcel.site_addr}, {parcel.city}
        </div>
        <div>
          Owned by {parcel.owner1} registered at {parcel.own_addr}{' '}
          {parcel.own_city} {parcel.own_state}
        </div>
        <button
          onClick={e => getChildParcels(e, parcel.owner1, setChildParcels)}
          className='btn btn-success'
        >
          Show this owner's properties
        </button>
      </Popup>
    </Marker>
  )
}

function createChildMarker (parcel) {
  return (
    <Marker position={[parcel.x_coord, parcel.y_coord]}>
      <Popup>
        <div>
          {parcel.site_addr}, {parcel.city}
        </div>
      </Popup>
    </Marker>
  )
}

function LocationMarker () {
  const [position, setPosition] = useState(null)
  const [popupContent, setPopupContent] = useState('popup')
  const [childParcels, setChildParcels] = useState()
  const [parcels, setParcels] = useContext(ParcelsContext)

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

  const markers = []
  var avgX = 0
  var avgY = 0
  if (parcels != null && parcels.Length != 0) {
    for (const parcel of parcels) {
      avgX = avgX + parcel.x_coord
      avgY = avgY + parcel.y_coord
      if (parcel.x_coord && parcel.y_coord) {
        markers.push(createMarker(parcel, setChildParcels))
      }
    }

    if (childParcels != null && childParcels.Length != 0) {
      for (const parcel of childParcels) {
        avgX = avgX + parcel.x_coord
        avgY = avgY + parcel.y_coord
        if (parcel.x_coord && parcel.y_coord) {
          markers.push(createChildMarker(parcel))
        }
      }
    }
    avgX = avgX / markers.length
    avgY = avgY / markers.length
    console.log('lat long: ', avgX, avgY)
    const latLong = latLng(avgX, avgY)
    map.flyTo(latLong, map.getZoom())
    return markers
  }

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
