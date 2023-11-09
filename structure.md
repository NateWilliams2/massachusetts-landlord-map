# Project structure

## Backend
### Script
- Python script that imports data from geodb files into sql database
### SQL Server
#### Database Fields
    PROP_ID 
    LOC_ID 
    BLDG_VAL
	LAND_VAL
	OTHER_VAL
	TOTAL_VAL
	FY
	LOT_SIZE
	LS_DATE
	LS_PRICE
	USE_CODE
	SITE_ADDR
	ADDR_NUM
	FULL_STR
	LOCATION
	CITY
	ZIP
	OWNER1
	OWN_ADDR
	OWN_CITY
	OWN_STATE
	OWN_ZIP
	OWN_CO
	LS_BOOK
	LS_PAGE
	REG_ID
	ZONING
	YEAR_BUILT
	BLD_AREA
	UNITS
	RES_AREA
	STYLE
	STORIES
	NUM_ROOMS
	LOT_UNITS
	CAMA_ID
	TOWN_ID 
#### Indexes
    OWNER1
    CITY
- API endpoints
  - Get property info (by address)
  - Get owner property list (by name)
    - returns address list
  - Get owner known addresses (by name)

## Client
### Mapbox plugin





## User Experience

- Map view with a search bar (leaflet)
  - Address search: address is highlighted as a pin and owner info box pops up
  - Landlord search: all addresses are highlighted
- Property info box
  - address
  - value
  - units
  - landlord info
  - link to search property records
- Landlord info box
  - number of buildings owned
  - total value of buildings owned
  - link to search property records / evictions