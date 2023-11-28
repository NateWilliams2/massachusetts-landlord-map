import React, { Component } from 'react'
import ParcelDataService from '../services/parcel.service'
import ParcelMap from './parcel-map.component.js'

export default class GetParcel extends Component {
  constructor (props) {
    super(props)
    this.onChangeStreet = this.onChangeStreet.bind(this)
    this.onChangeNumber = this.onChangeNumber.bind(this)
    this.onChangeCity = this.onChangeCity.bind(this)
    this.getParcel = this.getParcel.bind(this)

    this.state = {
      id: null,
      site_addr: '',
      addr_number: '',
      city: ''
    }
  }

  onChangeStreet (e) {
    this.setState({
      site_addr: e.target.value
    })
  }

  onChangeNumber (e) {
    this.setState({
      addr_number: e.target.value
    })
  }

  onChangeCity (e) {
    this.setState({
      city: e.target.value
    })
  }

  getParcel (e) {
    var address = {
      site_addr: this.state.site_addr,
      addr_num: this.state.addr_number,
      city: this.state.city
    }

    ParcelDataService.findByAddress(address)
      .then(response => {
        if (response.data.parcels.length == 0) {
          // No parcels found
          console.log('No parcels found')
        } else if (response.data.parcels.length == 1) {
          // One parcel match
          this.setState(
            {
              parcel: response.data.parcels[0]
            },
            () => {
              console.log(this.state.parcel)
            }
          )
        } else {
          // Multiple parcels match
          // TODO (?) allow user to choose between matched parcels
          this.setState({
            parcel: response.data.parcels[0]
          })
          console.log(response.data.parcels.length + ' parcels found')
        }
      })
      .catch(e => {
        console.log(e)
      })
  }

  render () {
    return (
      <div className='submit-form'>
        {this.state.submitted ? (
          <div>
            <h4>You submitted successfully!</h4>
            <button className='btn btn-success' onClick={this.getParcel}>
              Add
            </button>
          </div>
        ) : (
          <div>
            <div className='form-group'>
              <label htmlFor='number'>Street Number</label>
              <input
                type='text'
                className='form-control'
                id='number'
                required
                value={this.state.addr_number}
                onChange={this.onChangeNumber}
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
                value={this.state.site_addr}
                onChange={this.onChangeStreet}
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
                value={this.state.city}
                onChange={this.onChangeCity}
                name='city'
              />
            </div>

            <button onClick={this.getParcel} className='btn btn-success'>
              Search for parcels
            </button>
          </div>
        )}
        <div>
          <ParcelMap></ParcelMap>
        </div>
      </div>
    )
  }
}
