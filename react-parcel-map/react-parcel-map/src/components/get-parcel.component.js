import React, { useState, createContext, useContext } from 'react'
import ParcelDataService from '../services/parcel.service'
import ParcelMap from './parcel-map.component.js'

export const ParcelsContext = createContext()

function getParcel (e, address, setParcels) {
  console.log(address)
  ParcelDataService.findByAddress(address)
    .then(response => {
      if (response.data.parcels.length == 0) {
        // No parcels found
        console.log('No parcels found')
        return
      }
      console.log(response.data.parcels.length + ' parcels found')
      setParcels(response.data.parcels)
    })
    .catch(e => {
      console.log(e)
    })
}

export default function MapPage () {
  const [addrNumber, setAddrNumber] = useState()
  const [addrStreet, setAddrStreet] = useState()
  const [addrCity, setAddrCity] = useState()
  const [parcels, setParcels] = useState()

  return (
    <div className='submit-form'>
      {
        <div>
          <div className='form-group'>
            <label htmlFor='number'>Street Number</label>
            <input
              type='text'
              className='form-control'
              id='number'
              required
              value={addrNumber}
              onChange={e => setAddrNumber(e.target.value)}
              name='number'
            />
          </div>

          <div className='form-group'>
            <label htmlFor='street'>Street</label>
            <input
              type='text'
              className='form-control'
              id='street'
              required
              value={addrStreet}
              onChange={e => setAddrStreet(e.target.value)}
              name='street'
            />
          </div>

          <div className='form-group'>
            <label htmlFor='city'>City</label>
            <input
              type='text'
              className='form-control'
              id='city'
              required
              value={addrCity}
              onChange={e => setAddrCity(e.target.value)}
              name='city'
            />
          </div>

          <button
            onClick={e =>
              getParcel(
                e,
                {
                  city: addrCity,
                  addr_num: addrNumber,
                  site_addr: addrStreet
                },
                setParcels
              )
            }
            className='btn btn-success'
          >
            Search for parcels
          </button>
        </div>
      }
      <div>
        <ParcelsContext.Provider value={[parcels, setParcels]}>
          <ParcelMap></ParcelMap>
        </ParcelsContext.Provider>
      </div>
    </div>
  )
}
