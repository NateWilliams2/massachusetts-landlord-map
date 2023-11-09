module.exports = {
    HOST: "localhost",
    USER: "boston",
    PASSWORD: "landlord",
    DB: "geodata",
    dialect: "mysql",
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  };