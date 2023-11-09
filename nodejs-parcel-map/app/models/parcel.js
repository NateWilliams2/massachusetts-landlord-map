module.exports = (sequelize, Sequelize) => {
    const Parcel = sequelize.define("parcel", {
      prop_id: {
        type: Sequelize.STRING
      },
      loc_id: {
        type: Sequelize.STRING
      },
      bldg_val: {
        type: Sequelize.INT
      },
      land_val: {
        type: Sequelize.INT
      },
      other_val: {
        type: Sequelize.INT
      },
      total_val: {
        type: Sequelize.INT
      },
      fy: {
        type: Sequelize.INT
      },
      lot_size: {
        type: Sequelize.INT
      },
      ls_date: {
        type: Sequelize.STRING
      },
      ls_price: {
        type: Sequelize.INT
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
        type: Sequelize.INT
      },
      bld_area: {
        type: Sequelize.INT
      },
      units: {
        type: Sequelize.INT
      },
      res_area: {
        type: Sequelize.INT
      },
      style: {
        type: Sequelize.STRING
      },
      stories: {
        type: Sequelize.STRING
      },
      num_rooms: {
        type: Sequelize.INT
      },
      lot_units: {
        type: Sequelize.STRING
      },
      cama_id: {
        type: Sequelize.INT
      },
      town_id: {
        type: Sequelize.INT
      },
    });

  
    return Parcel;
  };