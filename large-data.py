import os
import platform
import atlite
import logging
from datetime import datetime

url_content = "url: https://cds.climate.copernicus.eu/api\nkey: c8055bd8-4be6-4d84-baad-793286555d40"

if platform.system() == "Linux":
    file_path = os.path.expanduser("~/.cdsapirc")
elif platform.system() == "Windows":
    username = os.getlogin()
    file_path = f"C:\\Users\\{username}\\.cdsapirc"
else:
    raise Exception("Unsupported operating system")

if not os.path.exists('./tmp'):
    os.mkdir('./tmp')

with open(file_path, "w") as file:
    file.write(url_content)

year = '2011'
    
logging.basicConfig(level=logging.INFO)

# Loop over the years
logging.info(f"Processing {year}")

print(f'----------1 : {datetime.now().strftime("%H:%M:%S")}----------')

# Define the cutout; this will not yet trigger any major operations
cutout = atlite.Cutout(
    path=f"world-{year}-01.nc",
    module="era5", 
    x=slice(-180, 180),
    y=slice(-90, 90),
    time=f"{year}-01",
)

print(f'----------2 : {datetime.now().strftime("%H:%M:%S")}----------')

# This is where all the work happens (this can take some time).
cutout.prepare(
    compression={"zlib": True, "complevel": 9},
    monthly_requests=True,
    concurrent_requests=True,
    features=["wind"],
    tmpdir='./tmp'
)

print(f'----------3 : {datetime.now().strftime("%H:%M:%S")}----------')

# Extract the wind power generation capacity factors
wind_power_generation = cutout.wind(
    "Vestas_V112_3MW", 
    capacity_factor_timeseries=True,
    )

print(f'----------4 : {datetime.now().strftime("%H:%M:%S")}----------')

# Save gridded data as netCDF files
wind_power_generation.to_netcdf(f"world_wind_CF_timeseries_{year}.nc")

print(f'----------5 : {datetime.now().strftime("%H:%M:%S")}----------')