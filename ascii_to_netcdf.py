# Accepts an ascii grid file (.asc) and outputs a netCDF file with longitude and
# latitude as the x and y coordinates.

import argparse
import numpy as np
import xarray as xr

def ascii_to_netcdf(input_file, output_file,variable_name):
    with open(input_file, 'r') as file:
        # Read the header to extract necessary information
        header = [next(file) for _ in range(6)]
        ncols = int(header[0].split()[1])
        nrows = int(header[1].split()[1])
        xllcorner = float(header[2].split()[1])
        yllcorner = float(header[3].split()[1])
        cellsize = float(header[4].split()[1])
        nodata_value = float(header[5].split()[1])

        # Read the data values
        data = np.genfromtxt(file, skip_header=6, dtype=float, missing_values=nodata_value)
        data[data == nodata_value] = np.nan

        # Create x and y coordinate arrays
        x = np.linspace(xllcorner, xllcorner + cellsize * (ncols - 1), ncols)
        y = np.linspace(yllcorner + cellsize * (len(data) - 1), yllcorner, len(data))

        # Create a DataArray using xarray
        da = xr.DataArray(data, coords={'latitude': y, 'longitude': x}, dims=('latitude', 'longitude'))

        # Create an xarray Dataset and save it as a NetCDF file
        ds = xr.Dataset({variable_name: da})
        ds.to_netcdf(output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert ASCII grid to NetCDF')
    parser.add_argument('input_file', help='Path to the input ASCII grid file')
    parser.add_argument('output_file', help='Path to the output NetCDF file')
    parser.add_argument('-var', '--variable_name', default='variable', help='Name of the variable in NetCDF (default: "variable")')

    args = parser.parse_args()

    ascii_to_netcdf(args.input_file, args.output_file,args.variable_name)
