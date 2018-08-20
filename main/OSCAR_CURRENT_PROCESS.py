import commonPractice
import netCDF4
import calendar
import xlwt
import collections
import pandas as pd
import numpy as np
import multiprocessing as mp
from subprocess import call
from os import listdir, makedirs, walk
from os.path import join, splitext, isdir

def main():
	#Initial parameters
	pool = mp.Pool(4)
	current_nc_directory = '/home/alwin/oscar_vel2018'
	current_nc_rawdata = 'oscar_vel2018.nc'
	current_nc_input = join(current_nc_directory, current_nc_rawdata)

	print("\n" + "OSCAR Global Ocean Currents Reader")
	print("    NetCDF to Raster Converter    ")
	print("     Version 1.00 by: MasBoyo     " + "\n")
	print("Working on " + current_nc_input)

	#Initial preparations
	print("\n" + "Preparations for processing data")

	call("/home/alwin/CLEANINGCURR.sh")

	print("\n" + "Preparations done!")

	for i in range(1,13):
		folder_month = calendar.month_abbr[i] + '2018'
		makedirs(join(current_nc_directory, folder_month.upper()))

	#Split input for each month
	print("\n" + "Process 1 (Split yearly .netcdf to daily .netcdf) - STARTED" + "\n")

	nc = netCDF4.Dataset(current_nc_input, mode='r')
	lat = nc.variables['latitude'][:]
	lon = nc.variables['longitude'][:]
	time_var = nc.variables['time']
	currdiru = nc.variables['u'][:][:][:][:]
	currdirv = nc.variables['v'][:][:][:][:]

	for tm in range(len(time_var)):
		dtime = netCDF4.num2date(time_var[tm],time_var.units)
		current_nc_output = join(current_nc_directory, (dtime.strftime('%b')).upper() + '2018', dtime.strftime('%m-%d-%YZ%H%M%S') + '.nc')
		print(current_nc_output)
		split_current_nc = netCDF4.Dataset(current_nc_output, 'w', format='NETCDF4')
		split_current_nc.description = 'Current data at ' + dtime.strftime('%m-%d-%Y %H:%M:%S') + ' in Java Island region.'
		split_current_nc.createDimension('time', 1)
		split_current_nc.createDimension('latitude', 15)
		split_current_nc.createDimension('longitude', 37)
		times = split_current_nc.createVariable('time', 'i4', ('time',))
		times.units = "day since 1992-10-05 00:00:00"
		times.long_name = "Day since 1992-10-05 00:00:00"
		latitudes = split_current_nc.createVariable('latitude', 'f8', ('latitude',))
		latitudes.units = "degrees-north"
		latitudes.long_name = "Latitude"
		longitudes = split_current_nc.createVariable('longitude', 'f8', ('longitude',))
		longitudes.units = "degrees-east"
		longitudes.long_name = "Longitude"
		curdiru = split_current_nc.createVariable('udircurr', 'f8', ('time','latitude','longitude',))
		curdiru.units = "meter/sec"
		curdiru.long_name = "Ocean Surface Zonal Currents"
		curdirv = split_current_nc.createVariable('vdircurr', 'f8', ('time','latitude','longitude',))
		curdirv.units = "meter/sec"
		curdirv.long_name = "Ocean Surface Meridional Currents"		

		times[0] = time_var[tm]
		latitudes[:] = lat[254:269] # WATCH OUT
		longitudes[:] = lon[252:289] # WATCH OUT
		for i in range(len(longitudes)):
			if longitudes[i] > 180:
				longitudes[i] = longitudes[i] - 360
		currentu = currdiru[tm][0,254:269,252:289]
		currentv = currdirv[tm][0,254:269,252:289]
		curdiru[0,:,:] = currentu
		curdirv[0,:,:] = currentv

		split_current_nc.close()
		print(current_nc_output + " created.")
	nc.close()

	print("\n" + "Process 1 (Split yearly .netcdf to daily .netcdf) - FINISHED" + "\n")

	#Converting .nc to .csv for better calculation
	print("\n" + "Process 2 (Convert .netcdf to .csv) - STARTED" + "\n")

	for root, dirs, files in walk(current_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				for f in listdir(dirname):
					if f.endswith(".nc"):
						currfile = join(dirname,f)
						pool.map(commonPractice.convCurrCSV,[currfile])
						pool.close
						pool.join
						
	print("\n" + "Process 2 (Convert .netcdf to .csv) - FINISHED" + "\n")

	#Averaging value inside .csv and then converting to .xls
	print("\n" + "Process 3 (Averaging monthly data and convert from .csv to .xls) - STARTED" + "\n")

	for root, dirs, files in walk(current_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				cnt = collections.Counter()
				for f in listdir(dirname):
					name, ext = splitext(f)
					cnt[ext] += 1
					
				if cnt['.csv'] > 0:
					currdiru = pd.DataFrame(np.zeros((555,cnt['.csv'])))
					currdirv = pd.DataFrame(np.zeros((555,cnt['.csv'])))
					currdir = pd.DataFrame(np.zeros((555,cnt['.csv'])))
					currvel = pd.DataFrame(np.zeros((555,cnt['.csv'])))
					currres = pd.DataFrame(np.zeros((555,5)))

					i = 0
					for f in listdir(dirname):
						if f.endswith(".csv"):
							currcsv = join(dirname,f)
							populatecsv = pool.map(commonPractice.buildDB,[currcsv])
							currdiru[i] = populatecsv[0][3]
							currdirv[i] = populatecsv[0][4]
							pool.close
							pool.join
							i += 1

					currres[0]=populatecsv[0][1]
					currres[1]=populatecsv[0][2]
					currdiru.replace(to_replace = '--', value = np.nan, inplace = True)
					currdirv.replace(to_replace = '--', value = np.nan, inplace = True)
					currdiru = currdiru.apply(pd.to_numeric)
					currdirv = currdirv.apply(pd.to_numeric)
					currvel = np.hypot(currdiru,currdirv)
					currdir = (180/np.pi)*np.arctan2(currdirv,currdiru)
					currdiru = currvel*np.sin(currdir*(np.pi/180))
					currdirv = currvel*np.cos(currdir*(np.pi/180))
					currdiru[cnt['.csv']] = currdiru.sum(axis=1)
					currdirv[cnt['.csv']] = currdirv.sum(axis=1)
					currdir[cnt['.csv']] = (180/np.pi)*np.arctan2(currdirv[cnt['.csv']],currdiru[cnt['.csv']])
					currvel[cnt['.csv']] = currvel.mean(axis=1)
					currres[2] = currdir[cnt['.csv']]
					currres[3] = currvel[cnt['.csv']]
					currres[4] = np.negative(currvel[cnt['.csv']])

					book = xlwt.Workbook()
					sh = book.add_sheet(subdir)

					for i in range(555):
						for j in range(5):
							sh.write(i+1, j, currres.iloc[i][j])

					col1_name = 'Latitude'
					col2_name = 'Longitude'
					col3_name = 'CurrDirection'
					col4_name = 'CurrSpeed'
					col5_name = 'CurrNegSpeed'
					sh.write(0, 0, col1_name)
					sh.write(0, 1, col2_name)
					sh.write(0, 2, col3_name)
					sh.write(0, 3, col4_name)
					sh.write(0, 4, col5_name)
					book.save(join(dirname, subdir + "CURR.xls"))
					print("File exported successfully as " + join(dirname, subdir + "CURR.xls"))

	print("\n" + "Process 3 (Averaging monthly data and convert from .csv to .xls) - FINISHED" + "\n")

	#Export .xls back to .csv
	print("\n" + "Process 4 (Export final .xls to .csv) - STARTED" + "\n")

	for root, dirs, files in walk(current_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				for f in listdir(dirname):
					if f.endswith(".xls"):
						currxls = join(dirname,f)
						pool.map(commonPractice.convXLSCSV,[currxls])
						pool.close
						pool.join

	print("\n" + "Process 4 (Export final .xls to .csv) - FINISHED" + "\n")

	#Convert .csv to shapefile
	print("\n" + "Process 5 (Export final .csv to projected points .shp) - STARTED" + "\n")

	for root, dirs, files in walk(current_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				for f in listdir(dirname):
					if f.endswith("CURR.csv"):
						currcsv = join(dirname,f)
						pool.map(commonPractice.convCurrCSVSHP,[currcsv])
						pool.close
						pool.join

	print("\n" + "Process 5 (Export final .csv to projected points .shp) - FINISHED" + "\n")

	#Convert shapefile to raster
	print("\n" + "Process 6 (Export shapefile to raster dataset) - STARTED" + "\n")

	for root, dirs, files in walk(current_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				for f in listdir(dirname):
					if f.endswith("CURR.shp"):
						currshp = join(dirname,f)
						pool.map(commonPractice.convCurrSHPRAS,[currshp])
						pool.close
						pool.join

	print("\n" + "Process 6 (Export shapefile to raster dataset) - FINISHED" + "\n")

	#Migrating the results
	print("\n" + "Process 7 (Moving all results to final directory) - STARTED" + "\n")

	call("/home/alwin/MOVINGCURR.sh")

	print("\n" + "Process 7 (Moving all results to final directory) - FINISHED" + "\n")

	#That's all
	print("\n" + "All process completed!" + "\n")

if __name__ == '__main__':
	main()
