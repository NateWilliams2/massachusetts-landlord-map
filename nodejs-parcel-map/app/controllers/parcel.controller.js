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
      site_addr: address.site_addr,
      addr_num: address.addr_num,
      city: address.city
    }
  }).then(parcels => {
    res.send({ parcels: parcels })
  })
}

exports.findOne = (req, res) => {
  const parcel = {
    prop_id: 'testid',
    loc_id: 'testloc',
    bldg_val: 9,
    land_val: 9,
    other_val: 9,
    total_val: 9,
    fy: 9,
    lot_size: 9,
    ls_date: 'test',
    ls_price: 9,
    use_code: 'test',
    site_addr: 'test',
    addr_num: 'test',
    full_str: 'test',
    location: 'test',
    city: 'test',
    zip: 'test',
    owner1: 'test',
    own_addr: 'test',
    own_city: 'test',
    own_state: 'test',
    own_zip: 'test',
    own_co: 'test',
    ls_book: 'test',
    ls_page: 'test',
    reg_id: 'test',
    zoning: 'test',
    year_built: 9,
    bld_area: 9,
    units: 9,
    res_area: 9,
    style: 'test',
    stories: 'test',
    num_rooms: 9,
    lot_units: 'test',
    cama_id: 9,
    town_id: 9
  }
  res.send(parcel)
}
