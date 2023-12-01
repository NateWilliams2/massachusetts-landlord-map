from osgeo import ogr
from osgeo import osr
import mysql.connector
import re
import pathlib

ogr.UseExceptions()

table_name = "parcels"
def sanitize_owner(address: str) -> str:
    
    # SYMBOLS 
    address = re.sub(r"\b%s\b" % "\.", "", address)
    address = address.replace("  ", " ")
    
    # MASSACHUSETTS
    address = re.sub(r"\b%s\b" % "MASS BAY", "MASSACHUSETTS BAY", address)
    address = re.sub(r"\b%s\b" % "MASS DEPT", "MASSACHUSETTS DEPT", address)
    address = re.sub(r"\b%s\b" % "MASS DEPARTMENT", "MASSACHUSETTS DEPARTMENT", address)
    address = re.sub(r"\b%s\b" % "OF MASS", "OF MASSACHUSETTS", address)

    # # TRANSPORTATION
    address = re.sub(r"\b%s" % "TRANS AUTH", "TRANSPORTATION AUTH", address)
    address = re.sub(r"\b%s\b" % "TRANSP", "TRANSPORTATION", address)
    address = re.sub(r"\b%s\b" % "TRANSPTN", "TRANSPORTATION", address)
    address = re.sub(r"\b%s" % "TRANSIT AUTH", "TRANSPORTATION AUTH", address)

    # REDEVELOPMENT
    address = re.sub(r"\b%s\b" % "REDEVLPMNT", "REDEVELOPMENT", address)
    address = re.sub(r"\b%s\b" % "REDEVELPMNT", "REDEVELOPMENT", address)
    address = re.sub(r"\b%s\b" % "REDVLPMNT", "REDEVELOPMENT", address)

    # # AUTHORITY
    address = re.sub(r"\b%s\b" % "AUTH", "AUTHORITY", address)
    address = re.sub(r"%s\b" % "DEVELOPMENT AUTHOR", "DEVELOPMENT AUTHORITY", address)

    # FCL
    address = re.sub(r"\b%s\b" % "(FCL)", "FCL", address)
    address = re.sub(r"\b%s\b" % "BY FCL", "FCL", address)
    
    # COMMONWEALTH
    address = re.sub(r"\b%s\b" % "COMMWLTH", "COMMONWEALTH", address)
    address = re.sub(r"\b%s\b" % "COMMONWLTH", "COMMONWEALTH", address)
    address = re.sub(r"\b%s" % "COMM OF MASS", "COMMONWEALTH OF MASS", address)

    # TRUSTEES
    address = re.sub(r"\b%s\b" % "TRYSTEES", "TRUSTEES", address)
    address = re.sub(r"\b%s\b" % "TRSTS", "TRUSTEES", address)
    address = re.sub(r"\b%s\b" % "TRUSTEE OF", "TRUSTEES OF", address)
    address = re.sub(r"\b%s\b" % "TRST", "TRUST", address)

    # UNIVERSITY
    address = re.sub(r"\b%s\b" % "UNIVERSIT", "UNIVERSITY", address)

    # SOCIETY
    address = re.sub(r"\b%s\b" % "SOC", "SOCIETY", address)


    ### ONE-OFFS
    address = re.sub(r"\b%s\b" % "MASS HISTORICAL SOC MASS", "MASS HISTORICAL SOCIETY", address)
    address = re.sub(r"\b%s\b" % "SANIEOFF KHORSO", "SANIEOFF KHOSRO", address)
    address = re.sub(r"\b%s\b" % "MASSACHUSETTS M D C", "MASSACHUSETTS MDC", address)




    return address

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
        if table_name in x:
            has_parcels = True
            break

    # if parcels table does not exist, create it
    # Database Design:
    #   PROP_ID | LOC_ID | BLDG_VAL | LAND_VAL | OTHER_VAL | TOTAL_VAL | FY | LOT_SIZE | LS_DATE | LS_PRICE | USE_CODE | SITE_ADDR | ADDR_NUM | FULL_STR | LOCATION | CITY | ZIP | OWNER1 | OWN_ADDR | OWN_CITY | OWN_STATE | OWN_ZIP | OWN_CO | LS_BOOK | LS_PAGE | REG_ID | ZONING | YEAR_BUILT | BLD_AREA | UNITS | RES_AREA | STYLE | STORIES | NUM_ROOMS | LOT_UNITS | CAMA_ID | TOWN_ID 
    # Index: OWNER1, CITY
    if not has_parcels:
        mycursor.execute(f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, prop_id VARCHAR(255), loc_id VARCHAR(255), bldg_val INT, land_val INT, other_val INT, total_val INT, fy INT(16), lot_size INT, ls_date VARCHAR(255), ls_price INT, use_code VARCHAR(255), site_addr VARCHAR(255), addr_num VARCHAR(255), full_str VARCHAR(255), location VARCHAR(255), city VARCHAR(255), zip VARCHAR(255), owner1 VARCHAR(255), own_addr VARCHAR(255), own_city VARCHAR(255), own_state VARCHAR(255), own_zip VARCHAR(255), own_co VARCHAR(255), ls_book VARCHAR(255), ls_page VARCHAR(255), reg_id VARCHAR(255), zoning VARCHAR(255), year_built INT(16), bld_area INT, units INT, res_area INT, style VARCHAR(255), stories VARCHAR(255), num_rooms INT(16), lot_units VARCHAR(255), cama_id INT, town_id INT(16), x_coord FLOAT(20,10), y_coord FLOAT(20,10))") 
        mycursor.execute(f"CREATE INDEX idx_owner1 ON {table_name} (owner1)")
        mycursor.execute(f"CREATE INDEX idx_city ON {table_name} (city)")
        mycursor.close()

  

    return mydb

# SET UP DRIVER FOR GEODB
def get_parcels() -> ogr.DataSource:
    parcel_gdb =  pathlib.Path.home().as_posix() +"/react/boston-landlord-map/geo_data/M035_parcels_gdb/M035_parcels_CY22_FY23_sde.gdb"
    driver = ogr.GetDriverByName("OpenFileGDB")
    if not(isinstance(driver, ogr.Driver)): 
        raise ValueError('no driver returned')

    dataSource = driver.Open(parcel_gdb)

    if not(isinstance(dataSource, ogr.DataSource)): 
        raise ValueError('no data source returned')
    return dataSource

def insert_rows(data_source: ogr.DataSource, sqldb: mysql.connector.MySQLConnection, cursor, batch_size: int, total_rows: int):
    geom_layer = data_source.ExecuteSQL("SELECT * FROM M035TaxPar LIMIT {0}".format(total_rows))
    if not(isinstance(geom_layer, ogr.Layer)): 
        raise ValueError('no sql layer returned')
    featureCount = geom_layer.GetFeatureCount()
    if featureCount == 0:
        print("retrieved no rows")
    gc_layer = data_source.ExecuteSQL("SELECT * FROM M035Assess LIMIT {0}".format(total_rows))
    if not(isinstance(gc_layer, ogr.Layer)): 
        raise ValueError('no sql layer returned')
    featureCount = gc_layer.GetFeatureCount()
    if featureCount == 0:
        print("retrieved no rows")
    insert = f"INSERT INTO {table_name} (prop_id, loc_id, bldg_val, land_val, other_val, total_val, fy, lot_size, ls_date, ls_price, use_code, site_addr, addr_num, full_str, location, city, zip, owner1, own_addr, own_city, own_state, own_zip, own_co, ls_book, ls_page, reg_id, zoning, year_built, bld_area, units, res_area, style, stories, num_rooms, lot_units, cama_id, town_id, x_coord, y_coord) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    imported = 0
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
            
            lat_long = get_lat_long(data_source, sqldb, items['PROP_ID'])
            # print(items['SITE_ADDR'])
            # print('transformed coordinates: {0},{1}'.format(lat_long[0], lat_long[1])) # output projected X and Y coordinates
            
            # if lat_long is None or lat_long[0] is None or lat_long[1] is None:
            #     raise ValueError('no lat/long for this parcel')
            
            item_list = (items['PROP_ID'], items['LOC_ID'], items['BLDG_VAL'], items['LAND_VAL'], items['OTHER_VAL'], items['TOTAL_VAL'], items['FY'], items['LOT_SIZE'], items['LS_DATE'], items['LS_PRICE'], items['USE_CODE'], items['SITE_ADDR'], items['ADDR_NUM'], items['FULL_STR'], items['LOCATION'], items['CITY'], items['ZIP'], sanitize_owner(items['OWNER1']), items['OWN_ADDR'], items['OWN_CITY'], items['OWN_STATE'], items['OWN_ZIP'], items['OWN_CO'], items['LS_BOOK'], items['LS_PAGE'], items['REG_ID'], items['ZONING'], items['YEAR_BUILT'], items['BLD_AREA'], items['UNITS'], items['RES_AREA'], items['STYLE'], items['STORIES'], items['NUM_ROOMS'], items['LOT_UNITS'], items['CAMA_ID'], items['TOWN_ID'], lat_long[0], lat_long[1])
            items_list.append(item_list)
            
            imported += 1
            
        print(f"imported {imported} rows to db, {featureCount} rows left")
        cursor.executemany(insert, items_list)
        featureCount -= batch_size
        sqldb.commit()
        
def get_lat_long(data_source: ogr.DataSource, sqldb: mysql.connector.MySQLConnection, propID) -> list:
    gc_layer = data_source.ExecuteSQL(f"SELECT * FROM M035TaxPar WHERE MAP_PAR_ID='{propID}'")
    if not(isinstance(gc_layer, ogr.Layer)): 
        raise ValueError('no sql layer returned')
    featureCount = gc_layer.GetFeatureCount()
    if featureCount == 0:
        # print(f"retrieved no geometry for property {propID}")
        return([None, None])
        
    for i in range(data_source.GetLayerCount()):
        layer = data_source.GetLayerByIndex(i)
        # print(layer.GetName())
        # defn = layer.GetLayerDefn()
        # for j in range(defn.GetFieldCount()):
        #     feature = defn.GetFieldDefn(j)
        #     print('\t'+feature.GetNameRef())
        # for j in range(defn.GetGeomFieldCount()):
        #     feature = defn.GetGeomFieldDefn(j)
        #     print('geon: \t'+feature.GetNameRef())
        #     print(f'type: \t{feature.GetType()}')
        #     print(f'ref: \t{feature.GetSpatialRef()}')
        
        
    feature = gc_layer.GetNextFeature()
    if not(isinstance(feature, ogr.Feature)): 
        raise ValueError('no feature returned')
    # print(feature.DumpReadable())
    geom = feature.GetGeometryRef()
    if not(isinstance(geom, ogr.Geometry)): 
        raise ValueError('no geometry returned')
    # print(geom.GetGeometryName())
    
    # EPSG 4269
    # print(f"spatial reference: {geom.GetSpatialReference()}")
    InSR = geom.GetSpatialReference()
    
    # EPSG 4326
    OutSR = osr.SpatialReference()
    OutSR.ImportFromEPSG(4326)
    
    transform = osr.CoordinateTransformation(InSR, OutSR)

    try: 
        boundaries = geom.Boundary()
        if not(isinstance(boundaries, ogr.Geometry)): 
            raise ValueError('no boundary returned')
        # print(boundaries.GetGeometryName())
        
        xCoord = 0
        yCoord = 0
        for shape in range(boundaries.GetGeometryCount()):
            polygon = boundaries.GetGeometryRef(shape)
            # if polygon.GetGeometryName() != 'LINESTRING':
            #     print(polygon.GetGeometryName())
            # print(f'points: {polygon.GetPointCount()}')
            # if polygon.GetGeometryName() == 'LINESTRING':
            #     break
            if polygon.GetGeometryName() == 'COMPOUNDCURVE':
                polygon = polygon.GetLinearGeometry()
            for z in range(polygon.GetPointCount()):
                point = polygon.GetPoint(z)
                # point.AssignSpatialReference(InSR)    # tell the point what coordinates it's in
                # point.TransformTo(OutSR)              # project it to the out spatial reference
                
                # xc = point.GetX() * 0.0174532925199433
                # yc = point.GetY() * 0.0174532925199433
                # print(f'transformed multiplied coordinates: {xc},{yc}') # output projected X and Y coordinates
                # print(point)
                xCoord += point[0]
                yCoord += point[1]
            
            xCoord = xCoord / polygon.GetPointCount()
            yCoord = yCoord / polygon.GetPointCount()
            # print(f'x: {xCoord}, y: {yCoord}')
            # print('transformed coordinates: {0},{1}'.format(newPoint[0],newPoint[1])) # output projected X and Y coordinates
            
        newPoint = transform.TransformPoint(xCoord, yCoord)
        return([newPoint[0], newPoint[1]])
    except Exception as e:
        print(f'exception getting parcel coordinates: {e}')
        return([None, None])
    



sqldb = sql_initialize()
cursor = sqldb.cursor()
data_source = get_parcels()



max_rows = 10000000
insert_rows(data_source, sqldb, cursor, 10000, max_rows)



sqldb.disconnect()