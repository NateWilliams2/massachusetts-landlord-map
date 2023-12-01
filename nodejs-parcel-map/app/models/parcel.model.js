module.exports = (sequelize, Sequelize) => {
  const Parcel = sequelize.define('parcel', {
    prop_id: {
      type: Sequelize.STRING
    },
    loc_id: {
      type: Sequelize.STRING
    },
    bldg_val: {
      type: Sequelize.INTEGER
    },
    land_val: {
      type: Sequelize.INTEGER
    },
    other_val: {
      type: Sequelize.INTEGER
    },
    total_val: {
      type: Sequelize.INTEGER
    },
    fy: {
      type: Sequelize.INTEGER
    },
    lot_size: {
      type: Sequelize.INTEGER
    },
    ls_date: {
      type: Sequelize.STRING
    },
    ls_price: {
      type: Sequelize.INTEGER
    },
    use_code: {
      type: Sequelize.STRING
    },
    site_addr: {
      type: Sequelize.STRING
    },
    addr_num: {
      type: Sequelize.STRING
    },
    full_str: {
      type: Sequelize.STRING
    },
    location: {
      type: Sequelize.STRING
    },
    city: {
      type: Sequelize.STRING
    },
    zip: {
      type: Sequelize.STRING
    },
    owner1: {
      type: Sequelize.STRING
    },
    own_addr: {
      type: Sequelize.STRING
    },
    own_city: {
      type: Sequelize.STRING
    },
    own_state: {
      type: Sequelize.STRING
    },
    own_zip: {
      type: Sequelize.STRING
    },
    own_co: {
      type: Sequelize.STRING
    },
    ls_book: {
      type: Sequelize.STRING
    },
    ls_page: {
      type: Sequelize.STRING
    },
    reg_id: {
      type: Sequelize.STRING
    },
    zoning: {
      type: Sequelize.STRING
    },
    year_built: {
      type: Sequelize.INTEGER
    },
    bld_area: {
      type: Sequelize.INTEGER
    },
    units: {
      type: Sequelize.INTEGER
    },
    res_area: {
      type: Sequelize.INTEGER
    },
    style: {
      type: Sequelize.STRING
    },
    stories: {
      type: Sequelize.STRING
    },
    num_rooms: {
      type: Sequelize.INTEGER
    },
    lot_units: {
      type: Sequelize.STRING
    },
    cama_id: {
      type: Sequelize.INTEGER
    },
    town_id: {
      type: Sequelize.INTEGER
    },
    x_coord: {
      type: Sequelize.FLOAT(20, 10)
    },
    y_coord: {
      type: Sequelize.FLOAT(20, 10)
    }
  })

  Parcel.removeAttribute('createdAt')
  Parcel.removeAttribute('updatedAt')

  return Parcel
}
