import http from '../http-common.js'

class ParcelDataService {
  findByAddress (address) {
    return http.get(
      `/parcels/address?site_addr=${address.site_addr}&addr_num=${address.addr_num}&city=${address.city}`
    )
  }

  findByOwner (owner) {
    return http.get(`/parcels/owner?owner1=${owner}`)
  }
}

export default new ParcelDataService()
