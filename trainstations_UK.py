import csv # give python csv superpowers
from sqlalchemy import Integer, Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Region is currently the "parent" of everything. It is the "root".
class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True)
    region = Column(String)


# Station name is a child of Region
class Station_name(Base):
    __tablename__ = 'station_name'
    id = Column(Integer, primary_key=True)
    NLC = Column(String)
    TLC = Column(String)
    station_name = Column(String)
    local_authority = Column(String)
    constituency = Column(String)
    NUTS2_spatial_unit= Column(String)
    NUTS2_spatial_unit_code = Column(String)
    OS_grid_easting = Column(String)
    OS_grid_northing = Column(String)
    Station_Facility_Owner = Column(String)
    Network_Rail_Region_of_station = Column(String)
    Entries_Exits_Full = Column(String)
    Entries_Exits_Reduced = Column(String)
    Entries_Exits_Season = Column(String)
    A1819_Entries_Exits = Column(String)
    B1718_Entries_Exits = Column(String)
    C1819_Interchanges = Column(String)
    D1819_Entries_Exits_GB_Rank = Column(String)
    E1718_Entries_Exits_GB_Rank = Column(String)
    Change = Column(String)
    # We define the relationship between Region and station name here.
    region = relation("Region", backref="station_name")
    region_id = Column(Integer, ForeignKey('region.id'))


# A bunch of stuff to make the connection to the database work.
def dbconnect():
    engine = create_engine('sqlite:///UK_trainstations.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


''' Above here defines the DB'''
''' Below here adds data to the DB '''

def addStation_name(session, station_name_input):
    # Try and get the Country from the database. If error (Except) add to the database.
    try: 
        region = session.query(Region).filter(Region.region == station_name_input["Region"]).one()
    except:
        region = Region()
        region.region = station_name_input["Region"]
        session.add(region)
    station_name = Station_name()
    # Add attributes
    station_name.station_name = station_name_input["Station Name"]
    station_name.NLC = station_name_input["NLC"]
    station_name.TLC = station_name_input["TLC"]
    station_name.local_authority = station_name_input["Local Authority"]
    station_name.constituency = station_name_input["Constituency"]
    station_name.NUTS2_spatial_unit = station_name_input["NUTS2 Spatial Unit"]
    station_name.NUTS2_spatial_unit_code = station_name_input["NUTS2 Spatial_Unit Code"]
    station_name.OS_grid_easting = station_name_input["OS Grid Easting"]
    station_name.OS_grid_northing = station_name_input["OS Grid Northing"]
    station_name.Station_Facility_Owner = station_name_input["Station Facility Owner"]
    station_name.Network_Rail_Region_of_station = station_name_input["Network Rail Region of station"]
    station_name.Entries_Exits_Full = station_name_input["Entries Exits_Full"]
    station_name.Entries_Exits_Reduced = station_name_input["Entries Exits_Reduced"]
    station_name.Entries_Exits_Season= station_name_input["Entries Exits_Season"]
    station_name.A1819_Entries_Exits = station_name_input["A1819 Entries Exits"]
    station_name.B1718_Entries_Exits = station_name_input["B1718 Entries Exits"]
    station_name.C1819_Interchanges = station_name_input["C1819 Interchanges"]
    station_name.D1819_Entries_Exits_GB_Rank = station_name_input["D1819 Entries Exits GB rank"]
    station_name.E1718_Entries_Exits_GB_Rank = station_name_input["E1718 Entries Exits GB rank"]
    station_name.Change = station_name_input["Change"]
    # add the station name
    station_name.region = region
    session.add(station_name)
    session.commit()

session = dbconnect()

with open(r"short_train_station_data_uk.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for station_name in reader:
        addStation_name(session, station_name)