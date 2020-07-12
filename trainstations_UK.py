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
class Station(Base):
    __tablename__ = 'station'
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
    region = relation("Region", backref="station")
    region_id = Column(Integer, ForeignKey('region.id'))


# A bunch of stuff to make the connection to the database work.
def dbconnect():
    engine = create_engine('sqlite:///UK_trainstations.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


''' Above here defines the DB'''
''' Below here adds data to the DB '''

def addStation(session, station_input):
    # Try and get the Country from the database. If error (Except) add to the database.
    try: 
        region = session.query(Region).filter(Region.region == station_input["Region"]).one()
    except:
        region = Region()
        region.region = station_input["Region"]
        session.add(region)
    station = Station()
    # Add attributes
    station.station_name = station_input["Station Name"]
    station.NLC = station_input["NLC"]
    station.TLC = station_input["TLC"]
    station.local_authority = station_input["Local Authority"]
    station.constituency = station_input["Constituency"]
    station.NUTS2_spatial_unit = station_input["NUTS2 Spatial Unit"]
    station.NUTS2_spatial_unit_code = station_input["NUTS2 Spatial_Unit Code"]
    station.OS_grid_easting = station_input["OS Grid Easting"]
    station.OS_grid_northing = station_input["OS Grid Northing"]
    station.Station_Facility_Owner = station_input["Station Facility Owner"]
    station.Network_Rail_Region_of_station = station_input["Network Rail Region of station"]
    station.Entries_Exits_Full = station_input["Entries Exits_Full"]
    station.Entries_Exits_Reduced = station_input["Entries Exits_Reduced"]
    station.Entries_Exits_Season= station_input["Entries Exits_Season"]
    station.A1819_Entries_Exits = station_input["A1819 Entries Exits"]
    station.B1718_Entries_Exits = station_input["B1718 Entries Exits"]
    station.C1819_Interchanges = station_input["C1819 Interchanges"]
    station.D1819_Entries_Exits_GB_Rank = station_input["D1819 Entries Exits GB rank"]
    station.E1718_Entries_Exits_GB_Rank = station_input["E1718 Entries Exits GB rank"]
    station.Change = station_input["Change"]
    # add the station name
    station.region = region
    session.add(station)
    session.commit()

session = dbconnect()

with open(r"short_train_station_data_uk.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for station in reader:
        addStation(session, station)