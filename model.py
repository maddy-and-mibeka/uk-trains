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
    NUTS2_spatial_unit = Column(String)
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