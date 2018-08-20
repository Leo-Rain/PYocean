import commonPractice
import gdalalwin
import csv
import netCDF4
import calendar
import xlwt
import xlrd
import collections
import multiprocessing as mp
import pandas as pd
import numpy as np
import shapefile as shp
from subprocess import call
from os import listdir, makedirs, walk
from os.path import join, splitext, isdir

def main():
	pool = mp.Pool(4)
	wave_nc_directory = "/home/alwin/SOEST"
	#wave_nc_rawdata = "NWW3_Global_Best_22d3_bcdb_fa86.nc"
	#wave_nc_rawdata = "NWW3_Global_Best_1f64_d649_3528.nc"
	wave_nc_rawdata = "NWW3_Global_Best_1a26_d86e_9c8a.nc"
	wave_nc_input = join(wave_nc_directory, wave_nc_rawdata)

	print("\n" + "WAVEWATCH III Global Ocean Wave Reader")
	print("      NetCDF to Raster Converter      ")
	print("       Version 1.00 by: MasBoyo       " + "\n")
	print("Working on " + wave_nc_input)

	#Initial preparations
	print("\n" + "Preparations for processing data")

	call("/home/alwin/CLEANINGWAVE.sh")

	print("\n" + "Preparations done!")

	for i in range(1,13):
	 	folder_month = calendar.month_abbr[i] + '2018'
	 	makedirs(join(wave_nc_directory, folder_month.upper()))
	
	#Split input for each month
	print("\n" + "Process 1 (Split yearly .netcdf to daily .netcdf) - STARTED" + "\n")

	nc = netCDF4.Dataset(wave_nc_input, mode='r')
	lat = nc.variables['latitude'][:]
	lon = nc.variables['longitude'][:]
	time_var = nc.variables['time']
	wavdir = nc.variables['Tdir'][:,:,:,:]
	wavhgt = nc.variables['Thgt'][:,:,:,:]
	for tm in range(len(time_var)):
	 	dtime = netCDF4.num2date(time_var[tm],time_var.units)
	 	wave_nc_output = join(wave_nc_directory, (dtime.strftime('%b')).upper() + '2018', dtime.strftime('%m-%d-%YZ%H%M%S') + '.nc')
	 	split_wave_nc = netCDF4.Dataset(wave_nc_output, 'w', format='NETCDF4')
	 	split_wave_nc.description = 'Wave data at ' + dtime.strftime('%m-%d-%Y %H:%M:%S') + ' in Java Island region.'
	 	split_wave_nc.createDimension('time', 1)
	 	split_wave_nc.createDimension('latitude', 9)
	 	split_wave_nc.createDimension('longitude', 25)
	 	times = split_wave_nc.createVariable('time', 'f8', ('time',))
	 	times._CoordinateAxisType = "Time"
	 	times.axis = "T"
	 	times.calendar = "proleptic_gregorian"
	 	times.ioos_category = "Time"
	 	times.long_name = "Forecast time for ForecastModelRunCollection"
	 	times.standard_name = "time"
	 	times.time_origin = "01-JAN-1970 00:00:00"
	 	times.units = "seconds since 1970-01-01T00:00:00Z"
	 	latitudes = split_wave_nc.createVariable('latitude', 'f4', ('latitude',))
	 	latitudes._CoordinateAxisType = "Lat"
	 	latitudes.axis = "Y"
	 	latitudes.ioos_category = "Location"
	 	latitudes.long_name = "Latitude"
	 	latitudes.short_name = "lat"
	 	latitudes.standard_name = "latitude"
	 	latitudes.units = "degrees_north"
	 	longitudes = split_wave_nc.createVariable('longitude', 'f4', ('longitude',))
	 	longitudes._CoordinateAxisType = "Lon"
	 	longitudes.axis = "X"
	 	longitudes.ioos_category = "Location"
	 	longitudes.long_name = "Longitude"
	 	longitudes.short_name = "lon"
	 	longitudes.standard_name = "longitude"
	 	longitudes.units = "degrees_east"
	 	wavedirs = split_wave_nc.createVariable('dirWave', 'f4', ('time','latitude','longitude',))
	 	wavedirs.colorBarMaximum = 360.
	 	wavedirs.colorBarMinimum = 0.
	 	wavedirs.coordinates = "time_run time z lat lon"
	 	wavedirs.ioos_category = "Surface Waves"
	 	wavedirs.long_name = "peak wave direction"
	 	wavedirs.short_name = "Tdir"
	 	wavedirs.standard_name = "sea_surface_wave_from_direction"
	 	wavedirs.units = "degrees"
	 	waveheights = split_wave_nc.createVariable('hgtWave', 'f4', ('time','latitude','longitude',))
	 	waveheights.colorBarMaximum = 10.
	 	waveheights.colorBarMinimum = 0.
	 	waveheights.coordinates = "time_run time z lat lon"
	 	waveheights.ioos_category = "Surface Waves"
	 	waveheights.long_name = "significant wave height"
	 	waveheights.short_name = "Thgt"
	 	waveheights.standard_name = "sea_surface_wave_significant_height"
	 	waveheights.units = "meters"

	 	times[0] = time_var[tm]
	 	latitudes[:] = lat[:] # all
	 	longitudes[:] = lon[:] # all
	 	wavedirection = wavdir[tm][0][:][:]
	 	waveheight = wavhgt[tm][0][:][:]
	 	wavedirs[0,:,:] = wavedirection
	 	waveheights[0,:,:] = waveheight

	 	split_wave_nc.close()
	 	print(wave_nc_output + " created.")
	nc.close()

	print("\n" + "Process 1 (Split yearly .netcdf to daily .netcdf) - FINISHED" + "\n")

	#Converting .nc to .csv for better calculation
	print("\n" + "Process 2 (Convert .netcdf to .csv) - STARTED" + "\n")
	
	for root, dirs, files in walk(wave_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				for f in listdir(dirname):
					if f.endswith(".nc"):
						wavefile = join(dirname,f)
						pool.map(commonPractice.convWaveCSV,[wavefile])
						pool.close
						pool.join
						
	print("\n" + "Process 2 (Convert .netcdf to .csv) - FINISHED" + "\n")

	#Averaging value inside .csv and then converting to .xls
	print("\n" + "Process 3 (Averaging monthly data and convert from .csv to .xls) - STARTED" + "\n")
	
	for root, dirs, files in walk(wave_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				cnt = collections.Counter()
				for f in listdir(dirname):
					name, ext = splitext(f)
					cnt[ext] += 1

				if cnt['.csv'] > 0:
					wavedir = pd.DataFrame(np.zeros((225,cnt['.csv'])))
					waveudir = pd.DataFrame(np.zeros((225,cnt['.csv'])))
					wavevdir = pd.DataFrame(np.zeros((225,cnt['.csv'])))
					wavehgt = pd.DataFrame(np.zeros((225,cnt['.csv'])))
					waveres = pd.DataFrame(np.zeros((225,5)))
			
					i = 0
					for f in listdir(dirname):
						if f.endswith(".csv"):
							wavecsv = join(dirname,f)
							populatecsv = pool.map(commonPractice.buildDB,[wavecsv])
							wavedir[i] = populatecsv[0][3]
							wavehgt[i] = populatecsv[0][4]
							pool.close
							pool.join
							i += 1

					waveres[0] = populatecsv[0][1]
					waveres[1] = populatecsv[0][2]
					wavedir.replace(to_replace = '--', value = np.nan, inplace = True)
					wavehgt.replace(to_replace = '--', value = np.nan, inplace = True)
					wavedir = wavedir.apply(pd.to_numeric)
					wavehgt = wavehgt.apply(pd.to_numeric)
					waveudir = wavehgt*np.sin(wavedir*(np.pi/180))
					wavevdir = wavehgt*np.cos(wavedir*(np.pi/180))
					wavehgt[cnt['.csv']] = wavehgt.mean(axis=1)
					waveudir[cnt['.csv']] = waveudir.sum(axis=1)
					wavevdir[cnt['.csv']] = wavevdir.sum(axis=1)
					wavedir[cnt['.csv']] = (180/np.pi)*np.arctan2(wavevdir[cnt['.csv']],waveudir[cnt['.csv']])
					waveres[2] = (-1*wavedir[cnt['.csv']])-90
					waveres[3] = wavehgt[cnt['.csv']]
					waveres[4] = np.negative(wavehgt[cnt['.csv']])

					book = xlwt.Workbook()
					sh = book.add_sheet(subdir)

					for i in range(225):
						for j in range(5):
							sh.write(i+1, j, waveres.iloc[i][j])

					col1_name = "Latitude"
					col2_name = "Longitude"
					col3_name = "WavDirection"
					col4_name = "WavHeight"
					col5_name = "WavNegHeight"
					sh.write(0, 0, col1_name)
					sh.write(0, 1, col2_name)
					sh.write(0, 2, col3_name)
					sh.write(0, 3, col4_name)
					sh.write(0, 4, col5_name)
					book.save(join(dirname, subdir + "WAVE.xls"))
					print("File exported successfully as " + join(dirname, subdir + "WAVE.xls"))

	print("\n" + "Process 3 (Averaging monthly data and convert from .csv to .xls) - FINISHED" + "\n")

	#Export .xls back to .csv
	print("\n" + "Process 4 (Export final .xls to .csv) - STARTED" + "\n")

	for root, dirs, files in walk(wave_nc_directory):
			for dirname in dirs:
				subdir = dirname
				dirname = join(root,dirname)
				if isdir(dirname):
					for f in listdir(dirname):
						if f.endswith(".xls"):
							wavexls = join(dirname,f)
							pool.map(commonPractice.convXLSCSV,[wavexls])
							pool.close
							pool.join

	print("\n" + "Process 4 (Export final .xls to .csv) - FINISHED" + "\n")

	# Convert .csv to shapefile
	print("\n" + "Process 5 (Export final .csv to projected points .shp) - STARTED" + "\n")

	for root, dirs, files in walk(wave_nc_directory):
			for dirname in dirs:
				subdir = dirname
				dirname = join(root,dirname)
				if isdir(dirname):
					for f in listdir(dirname):
						if f.endswith("WAVE.csv"):
							wavecsv = join(dirname,f)
							pool.map(commonPractice.convWaveCSVSHP,[wavecsv])
							pool.close
							pool.join

	print("\n" + "Process 5 (Export final .csv to projected points .shp) - FINISHED" + "\n")

	#Convert shapefile to raster
	print("\n" + "Process 6 (Export shapefile to raster dataset) - STARTED" + "\n")

	for root, dirs, files in walk(wave_nc_directory):
			for dirname in dirs:
				subdir = dirname
				dirname = join(root,dirname)
				if isdir(dirname):
					for f in listdir(dirname):
						if f.endswith("WAVE.shp"):
							waveshp = join(dirname,f)
							pool.map(commonPractice.convWaveSHPRAS,[waveshp])
							pool.close
							pool.join

	print("\n" + "Process 6 (Export shapefile to raster dataset) - FINISHED" + "\n")

	#Migrating the results
	print("\n" + "Process 7 (Moving all results to final directory) - STARTED" + "\n")

	call("/home/alwin/MOVINGWAVE.sh")

	print("\n" + "Process 7 (Moving all results to final directory) - FINISHED" + "\n")

	#That's all
	print("\n" + "All process completed!" + "\n")

if __name__ == '__main__':
	main()
