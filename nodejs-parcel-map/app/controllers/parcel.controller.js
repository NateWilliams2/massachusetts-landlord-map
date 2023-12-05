const db = require('../models')
const Parcel = db.parcel
const Op = db.Sequelize.Op

exports.findByAddress = (req, res) => {
  const address = {
    site_addr: req.query.site_addr,
    addr_num: req.query.addr_num,
    city: req.query.city
  }
  parcels = Parcel.findAll({
    where: {
      site_addr: {
        [Op.like]: '%' + address.site_addr + '%'
      },
      addr_num: address.addr_num,
      city: {
        [Op.like]: '%' + address.city + '%'
      }
    },
    limit: 10
  }).then(parcels => {
    res.send({ parcels: parcels })
  })
}

exports.findByOwner = (req, res) => {
  parcels = Parcel.findAll({
    where: {
      owner1: {
        [Op.like]: req.query.owner1
      }
    },
    limit: 1000
  }).then(parcels => {
    res.send({ parcels: parcels })
  })
}
