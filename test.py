import xarray as xr

# باز کردن فایل NetCDF
ds = xr.open_dataset('./49aa5535e810fe5ca3da68f115635d62.nc')

# نمایش تمامی متغیرها
# print(ds)
print(ds.u100.sel(latitude=50.0, longitude=10.0, valid_time='2011-07-01T12:00').values)