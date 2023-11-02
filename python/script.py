
from osgeo import ogr

ogr.UseExceptions()


parcel_gdb = "./geo_data/M035_parcels_gdb/M035_parcels_CY22_FY23_sde.gdb"
driver = ogr.GetDriverByName("OpenFileGDB")
if not(isinstance(driver, ogr.Driver)): 
    raise ValueError('no driver returned')

dataSource = driver.Open(parcel_gdb)

if not(isinstance(dataSource, ogr.DataSource)): 
    raise ValueError('no data source returned')

taxLayer = dataSource.GetLayer("M035Assess")
if not(isinstance(taxLayer, ogr.Layer)): 
    raise ValueError('could not get layer M035Assess')
layerDefn = taxLayer.GetLayerDefn()
if not(isinstance(layerDefn, ogr.FeatureDefn)): 
    raise ValueError('no layer defn returned')

# for j in range(layerDefn.GetFieldCount()):
#     field = layerDefn.GetFieldDefn(j)
#     if not(isinstance(field, ogr.FieldDefn)): 
#         raise ValueError('no field defn returned')
#     print(field.GetName(), ": ", field.GetTypeName())

# sqlLayer = dataSource.ExecuteSQL(r"SELECT * FROM M035Assess WHERE OWNER1 LIKE '%LEON ST%' LIMIT 10")
sqlLayer = dataSource.ExecuteSQL(r"SELECT * FROM M035Assess WHERE SITE_ADDR LIKE '%MINTON%' LIMIT 10")
if not(isinstance(sqlLayer, ogr.Layer)): 
    raise ValueError('no sql layer returned')
for i in range(sqlLayer.GetFeatureCount()):
    feature = sqlLayer.GetNextFeature()
    if not(isinstance(feature, ogr.Feature)): 
        raise ValueError('no feature returned')
    print(feature.DumpReadable())