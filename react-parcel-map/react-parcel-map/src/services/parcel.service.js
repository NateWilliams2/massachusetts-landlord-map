
class ParcelDataService {
    get(id) {
      return http.get(`/parcels/${id}`);
    }

    findByTitle(title) {
      return http.get(`/parcels?title=${title}`);
    }
}

export default new ParcelDataService();