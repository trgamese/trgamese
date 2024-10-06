import atlite
import cartopy.io.shapereader as shpreader
import geopandas as gpd
from shapely.geometry import box
import pandas as pd
import logging
from argparse import ArgumentParser
from datetime import datetime

##

print(f'0 : {datetime.now()}')

year = '2011'

logging.basicConfig(level=logging.INFO)

world = gpd.read_file("./data/ne_110m_admin_0_countries.shp")

# Drop uninhabited regions and Antarctica
# world = world[(world.POP_EST > 0) & (world.NAME != "Antarctica")]

# region = world
region_name = "western-europe"

# Loop over the years
logging.info(f"Processing {year}")

##

print(f'1 : {datetime.now()}')

# Define the cutout; this will not yet trigger any major operations
cutout = atlite.Cutout(
    path=f"{region_name}-{year}-01.nc",
    module="era5", 
    # bounds=region.unary_union.bounds, 
    x=slice(-13.6913, 1.7712),
    y=slice(49.9096, 60.8479),
    time=f"{year}-01",
)

##

print(cutout)

##

# This is where all the work happens (this can take some time).
cutout.prepare(
    compression={"zlib": True, "complevel": 9},
    features = ['wind',],
    monthly_requests=True,
    concurrent_requests=True,
    overwrite=True)

print(f'2 : {datetime.now()}')

##

# Extract the wind power generation capacity factors
wind_power_generation = cutout.wind(
    "Vestas_V112_3MW", 
    capacity_factor_timeseries=True,
    )

print(f'3 : {datetime.now()}')
print(wind_power_generation)