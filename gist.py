import atlite
import cartopy.io.shapereader as shpreader
import geopandas as gpd
from shapely.geometry import box
import pandas as pd
import logging
from argparse import ArgumentParser

year = '2011'
    
logging.basicConfig(level=logging.INFO)

world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
# Drop uninhabited regions and Antarctica
world = world[(world.pop_est > 0) & (world.name != "Antarctica")]

region = world
region_name = "world"

# Loop over the years
logging.info(f"Processing {year}")

# Define the cutout; this will not yet trigger any major operations
cutout = atlite.Cutout(
    path=f"{region_name}-{year}_timeseries", module="era5", 
    bounds=region.unary_union.bounds, 
    time=f"{year}",
    chunks={"time": 100,},)
# This is where all the work happens (this can take some time).
cutout.prepare(
    compression={"zlib": True, "complevel": 9},
    monthly_requests=True,
    concurrent_requests=True)

# Extract the wind power generation capacity factors
wind_power_generation = cutout.wind(
    "Vestas_V112_3MW", 
    capacity_factor_timeseries=True,
    )

# Extract the solar power generation capacity factors
solar_power_generation = cutout.pv(
    panel="CSi", 
    orientation='latitude_optimal', 
    tracking="horizontal",
    capacity_factor_timeseries=True,)

# Extract the concenctrated solar power generation capacity factors
csp_power_generation = cutout.csp(
    installation="SAM_parabolic_trough", 
    capacity_factor_timeseries=True,)

# Save gridded data as netCDF files
wind_power_generation.to_netcdf(f"{region_name}_wind_CF_timeseries_{year}.nc")
solar_power_generation.to_netcdf(f"{region_name}_solar_CF_timeseries_{year}.nc")
csp_power_generation.to_netcdf(f"{region_name}_csp_CF_timeseries_{year}.nc")
