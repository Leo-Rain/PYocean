import commonPractice
import xlwt
import collections
import pandas as pd
import numpy as np
import multiprocessing as mp
from os import listdir, walk
from os.path import join, splitext, isdir
from subprocess import call

def main():
	#Initial parameters
	pool = mp.Pool(4)
	wind_nc_directory = "/home/alwin/NCDC2017"
	
	print("\n" + "NCDC Global Ocean Wind Data Reader")
	print("    NetCDF to Raster Converter    ")
	print("     Version 1.00 by: MasBoyo     " + "\n")

	#Initial preparations
	print("\n" + "Preparations for processing data")

	call("/home/alwin/CLEANINGWIND.sh")

	print("\n" + "Preparations done!")

	#Converting .nc to .csv for better calculation
	print("\n" + "Process 1 (Convert .netcdf to .csv) - STARTED" + "\n")

	for root, dirs, files in walk(wind_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				for f in listdir(dirname):
					if f.endswith(".nc"):
						windfile = join(dirname,f)
						pool.map(commonPractice.convWindCSV,[windfile])
						pool.close
						pool.join

	print("\n" + "Process 1 (Convert .netcdf to .csv) - FINISHED" + "\n")

	#Averaging value inside .csv and then converting to .xls
	print("\n" + "Process 2 (Averaging monthly data and convert from .csv to .xls) - STARTED" + "\n")

	for root, dirs, files in walk(wind_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				cnt = collections.Counter()
				for f in listdir(dirname):
					name, ext = splitext(f)
					cnt[ext] += 1

				if cnt['.csv'] > 0:
					windudir = pd.DataFrame(np.zeros((1071,cnt['.csv'])))
					windvdir = pd.DataFrame(np.zeros((1071,cnt['.csv'])))
					winddir = pd.DataFrame(np.zeros((1071,cnt['.csv'])))
					windvel = pd.DataFrame(np.zeros((1071,cnt['.csv'])))
					windres = pd.DataFrame(np.zeros((1071,6)))

					i = 0
					for f in listdir(dirname):
						if f.endswith(".csv"):
							windcsv = join(dirname, f)
							populatecsv = pool.map(commonPractice.buildDB,[windcsv])
							windudir[i] = populatecsv[0][3]
							windvdir[i] = populatecsv[0][4]
							windvel[i] = populatecsv[0][5]
							pool.close
							pool.join
							i += 1

					windres[0] = populatecsv[0][1]
					windres[1] = populatecsv[0][2]
					windudir.replace(to_replace = '--', value = np.nan, inplace = True)
					windvdir.replace(to_replace = '--', value = np.nan, inplace = True)
					windvel.replace(to_replace = '--', value = np.nan, inplace = True)
					windudir = windudir.apply(pd.to_numeric)
					windvdir = windvdir.apply(pd.to_numeric)
					windvel = windvel.apply(pd.to_numeric)
					winddir = (180/np.pi)*np.arctan2(windvdir,windudir)
					windudir = windvel*np.sin(winddir*(np.pi/180))
					windvdir = windvel*np.cos(winddir*(np.pi/180))
					windudir[cnt['.csv']] = windudir.sum(axis=1)
					windvdir[cnt['.csv']] = windvdir.sum(axis=1)
					winddir[cnt['.csv']] = (180/np.pi)*np.arctan2(windvdir[cnt['.csv']],windudir[cnt['.csv']])
					windvel[cnt['.csv']] = windvel.mean(axis=1)
					windres[2] = winddir[cnt['.csv']]
					windres[3] = ((-1)*winddir[cnt['.csv']])-270
					windres[4] = windvel[cnt['.csv']]
					windres[5] = np.negative(windvel[cnt['.csv']])

					book = xlwt.Workbook()
					sh = book.add_sheet(subdir)

					for i in range(1071):
						for j in range(6):
							sh.write(i+1, j, windres.iloc[i][j])

					col1_name = "Latitude"
					col2_name = "Longitude"
					col3_name = "WindDirection"
					col4_name = "WindTrueDirection"
					col5_name = "WindHeight"
					col6_name = "WindNegHeight"
					sh.write(0, 0, col1_name)
					sh.write(0, 1, col2_name)
					sh.write(0, 2, col3_name)
					sh.write(0, 3, col4_name)
					sh.write(0, 4, col5_name)
					sh.write(0, 5, col6_name)
					book.save(join(dirname, subdir + "WIND.xls"))
					print("File exported successfully as " + join(dirname, subdir + "WIND.xls"))

	print("\n" + "Process 2 (Averaging monthly data and convert from .csv to .xls) - FINISHED" + "\n")

	# Export .xls back to .csv
	print("\n" + "Process 3 (Export final .xls to .csv) - STARTED" + "\n")

	for root, dirs, files in walk(wind_nc_directory):
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

	print("\n" + "Process 3 (Export final .xls to .csv) - FINISHED" + "\n")

	#Convert .csv to shapefile
	print("\n" + "Process 4 (Export final .csv to projected points .shp) - STARTED" + "\n")

	for root, dirs, files in walk(wind_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				for f in listdir(dirname):
					if f.endswith("WIND.csv"):
						windcsv = join(dirname,f)
						pool.map(commonPractice.convWindCSVSHP,[windcsv])
						pool.close
						pool.join

	print("\n" + "Process 4 (Export final .csv to projected points .shp) - FINISHED" + "\n")

	#Convert shapefile to raster
	print("\n" + "Process 5 (Export shapefile to raster dataset) - STARTED" + "\n")

	for root, dirs, files in walk(wind_nc_directory):
		for dirname in dirs:
			subdir = dirname
			dirname = join(root,dirname)
			if isdir(dirname):
				for f in listdir(dirname):
					if f.endswith("WIND.shp"):
						windshp = join(dirname,f)
						pool.map(commonPractice.convWindSHPRAS,[windshp])
						pool.close
						pool.join

	print("\n" + "Process 5 (Export shapefile to raster dataset) - FINISHED" + "\n")
 
	#Migrating the results
	print("\n" + "Process 6 (Moving all results to final directory) - STARTED" + "\n")

	call("/home/alwin/MOVINGWIND.sh")

	print("\n" + "Process 6 (Moving all results to final directory) - FINISHED" + "\n")

	#That's all
	print("\n" + "All process completed!" + "\n")

if __name__ == '__main__':
	main()
