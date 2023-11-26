
import http from "../http-common.js";

class ParcelDataService {
    get(id) {
      return http.get(`/parcels/${id}`);
    }

    findByAddress(address) {
      return http.get(`/parcels/address?site_addr=${address.site_addr}&addr_num=${address.addr_num}&city=${address.city}`);
    }

    findOne() {
      return http.get(`/parcels`);
    }
}

export default new ParcelDataService();