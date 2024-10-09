import os
import atlite
import logging
import platform

url_content = "url: https://cds.climate.copernicus.eu/api\nkey: 88edbff7-a215-49d4-8423-286cccd04872"

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

# Define the cutout; URL and key can be set here
cutout = atlite.Cutout(
    path=f"western-europe-{year}-01.nc",
    module="era5",
    x=slice(-13.6913, 1.7712),
    y=slice(49.9096, 60.8479),
    time=f"{year}-01",
)

# Prepare the cutout (this can take some time).
cutout.prepare(
    compression={"zlib": True, "complevel": 9},
    features=['wind'],
    monthly_requests=True,
    concurrent_requests=True,
    tmpdir='./tmp'
)

# Extract the wind power generation capacity factors
wind_power_generation = cutout.wind(
    "Vestas_V112_3MW",
    capacity_factor_timeseries=True,
)

print(wind_power_generation)

input('Press Enter...')