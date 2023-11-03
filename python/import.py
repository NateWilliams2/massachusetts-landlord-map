
from osgeo import ogr
import mysql.connector
import time

ogr.UseExceptions()

# SET UP DRIVER FOR MYSQL

def sql_initialize() -> mysql.connector.MySQLConnection:
    # username boston
    # password landlord
    mydb = mysql.connector.connect(
    host="localhost",
    user="boston",
    password="landlord",
    database="geodata"
    )
    mycursor = mydb.cursor()


    # check if table parcels already exists
    has_parcels = False
    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        if 'parcels' in x:
            has_parcels = True
            break

    # if parcels table does not exist, create it
    # Database Design:
    #   PROP_ID | LOC_ID | BLDG_VAL | LAND_VAL | OTHER_VAL | TOTAL_VAL | FY | LOT_SIZE | LS_DATE | LS_PRICE | USE_CODE | SITE_ADDR | ADDR_NUM | FULL_STR | LOCATION | CITY | ZIP | OWNER1 | OWN_ADDR | OWN_CITY | OWN_STATE | OWN_ZIP | OWN_CO | LS_BOOK | LS_PAGE | REG_ID | ZONING | YEAR_BUILT | BLD_AREA | UNITS | RES_AREA | STYLE | STORIES | NUM_ROOMS | LOT_UNITS | CAMA_ID | TOWN_ID 
    # Index: OWNER1, CITY
    if not has_parcels:
        mycursor.execute("CREATE TABLE parcels (id INT AUTO_INCREMENT PRIMARY KEY, prop_id VARCHAR(255), loc_id VARCHAR(255), bldg_val INT, land_val INT, other_val INT, total_val INT, fy INT(16), lot_size INT, ls_date VARCHAR(255), ls_price INT, use_code VARCHAR(255), site_addr VARCHAR(255), addr_num VARCHAR(255), full_str VARCHAR(255), location VARCHAR(255), city VARCHAR(255), zip VARCHAR(255), owner1 VARCHAR(255), own_addr VARCHAR(255), own_city VARCHAR(255), own_state VARCHAR(255), own_zip VARCHAR(255), own_co VARCHAR(255), ls_book VARCHAR(255), ls_page VARCHAR(255), reg_id VARCHAR(255), zoning VARCHAR(255), year_built INT(16), bld_area INT, units INT, res_area INT, style VARCHAR(255), stories VARCHAR(255), num_rooms INT(16), lot_units VARCHAR(255), cama_id INT, town_id INT(16))") 
        mycursor.execute("CREATE INDEX idx_owner1 ON parcels (owner1)")
        mycursor.execute("CREATE INDEX idx_city ON parcels (city)")
        mycursor.close()

  

    return mydb

# SET UP DRIVER FOR GEODB
def get_parcels() -> ogr.DataSource:
    parcel_gdb = "./geo_data/M035_parcels_gdb/M035_parcels_CY22_FY23_sde.gdb"
    driver = ogr.GetDriverByName("OpenFileGDB")
    if not(isinstance(driver, ogr.Driver)): 
        raise ValueError('no driver returned')

    dataSource = driver.Open(parcel_gdb)

    if not(isinstance(dataSource, ogr.DataSource)): 
        raise ValueError('no data source returned')
    return dataSource

def insert_rows(data_source: ogr.DataSource, sqldb: mysql.connector.MySQLConnection, cursor, batch_size: int, total_rows: int):
    # gc_layer = data_source.ExecuteSQL("SELECT * FROM M035Assess WHERE SITE_ADDR LIKE '%MINTON%' LIMIT {0}".format(num_rows))
    # gc_layer = data_source.ExecuteSQL("SELECT * FROM M035Assess WHERE PROP_ID = '0100170000' LIMIT {0}".format(total_rows))
    gc_layer = data_source.ExecuteSQL("SELECT * FROM M035Assess LIMIT {0}".format(total_rows))
    if not(isinstance(gc_layer, ogr.Layer)): 
        raise ValueError('no sql layer returned')
    featureCount = gc_layer.GetFeatureCount()
    if featureCount == 0:
        print("retrieved no rows")
    insert = """INSERT INTO parcels (prop_id, loc_id, bldg_val, land_val, other_val, total_val, fy, lot_size, ls_date, ls_price, use_code, site_addr, addr_num, full_str, location, city, zip, owner1, own_addr, own_city, own_state, own_zip, own_co, ls_book, ls_page, reg_id, zoning, year_built, bld_area, units, res_area, style, stories, num_rooms, lot_units, cama_id, town_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    while featureCount > 0:
        items_list = []
        if batch_size > featureCount:
            batch_size = featureCount
        for _ in range(batch_size):
            feature = gc_layer.GetNextFeature()
            if not(isinstance(feature, ogr.Feature)): 
                raise ValueError('no feature returned')
            # print(feature.DumpReadable())
            items = feature.items()
            item_list = (items['PROP_ID'], items['LOC_ID'], items['BLDG_VAL'], items['LAND_VAL'], items['OTHER_VAL'], items['TOTAL_VAL'], items['FY'], items['LOT_SIZE'], items['LS_DATE'], items['LS_PRICE'], items['USE_CODE'], items['SITE_ADDR'], items['ADDR_NUM'], items['FULL_STR'], items['LOCATION'], items['CITY'], items['ZIP'], items['OWNER1'], items['OWN_ADDR'], items['OWN_CITY'], items['OWN_STATE'], items['OWN_ZIP'], items['OWN_CO'], items['LS_BOOK'], items['LS_PAGE'], items['REG_ID'], items['ZONING'], items['YEAR_BUILT'], items['BLD_AREA'], items['UNITS'], items['RES_AREA'], items['STYLE'], items['STORIES'], items['NUM_ROOMS'], items['LOT_UNITS'], items['CAMA_ID'], items['TOWN_ID'])
            items_list.append(item_list)
            
        cursor.executemany(insert, items_list)
        featureCount -= batch_size
        sqldb.commit()



sqldb = sql_initialize()
cursor = sqldb.cursor()
data_source = get_parcels()


total_rows = 1000
# start = time.perf_counter()
# insert_rows(data_source, sqldb, cursor, 1, total_rows)
# insert_rows(data_source, sqldb, cursor, 1, total_rows)
# insert_rows(data_source, sqldb, cursor, 1, total_rows)
# insert_rows(data_source, sqldb, cursor, 1, total_rows)
insert_rows(data_source, sqldb, cursor, 10000, total_rows)
# print(f"Added {total_rows} rows in batches of 1 in {time.perf_counter() - start} seconds")



sqldb.disconnect()