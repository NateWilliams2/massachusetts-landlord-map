const parcels = require('../controllers/parcel.controller.js')

module.exports = app => {
  var router = require('express').Router()

  router.get('/address', parcels.findByAddress)
  router.get('/owner', parcels.findByOwner)

  app.use('/api/parcels', router)
}
