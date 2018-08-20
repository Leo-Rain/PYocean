from os import listdir
from os.path import join
from arcpy import ASCIIToRaster_conversion, Resample_management

wind_asc_directory = "D:\PTBPI\SIXTH SURVEY\DATA\ANGIN"
wind_asc_input = "RESULTNCDCAUG2017"
wind_asc_output = "RESULTNCDCAUG2017_1"
wind_asc_output2 = "RESULTNCDCAUG2017_2"

def main():
	print("\n" + "NCDC Global Ocean Wind Tool")
	print(" ASCII to Raster Converter ")
	print(" Version 1.00a by: MasBoyo " + "\n")

	#Convert into low resolution grid
	print("\n" + "Process 1 (Convert .asc to grid .adf) - STARTED" + "\n")

	listfiles = []
	searchasc = join(wind_asc_directory,wind_asc_input)
	for f in listdir(searchasc):
		windascii = join(wind_asc_directory,wind_asc_input,f)
		windgrid = join(wind_asc_directory,wind_asc_output,f.replace('.asc',''))
		windproj = join(windgrid,"prj.adf")
		listfiles.append((windascii,windgrid,windproj))
	for i in range(len(listfiles)):
		convASCRAS(listfiles[i][0],listfiles[i][1],listfiles[i][2])

	print("\n" + "Process 1 (Convert .asc to grid .adf) - FINISHED" + "\n")

	#Resample grid data
	print("\n" + "Process 2 (Upscale resolution of grid .adf) - STARTED" + "\n")

	listfiles2 = []
	searchasc2 = join(wind_asc_directory,wind_asc_output)
	for f in listdir(searchasc2):
		if f.endswith("dirwin") or f.endswith("velwin") or f.endswith("vwinne") or f.endswith("dwintr"):
			windgrid1o = join(wind_asc_directory,wind_asc_output,f)
			windgridhi = join(wind_asc_directory,wind_asc_output2,f)
			windproj2 = join(windgridhi,"prj.adf")
			listfiles2.append((windgrid1o,windgridhi,windproj2))
	for i in range(len(listfiles2)):
		grdResample(listfiles2[i][0],listfiles2[i][1],listfiles2[i][2])

	print("\n" + "Process 2 (Upscale resolution of grid .adf) - FINISHED" + "\n")

def convASCRAS(a,b,c):
	print("Working on " + a)
	rasterType = "FLOAT"
	ASCIIToRaster_conversion(a, b, rasterType)
	with open(c, "w") as grdprj:
		grdprj.write("Projection    GEOGRAPHIC" + "\n" +\
			"Datum         WGS84" + "\n" +\
			"Spheroid      WGS84" + "\n" +\
			"Units         DD" + "\n" +\
			"Zunits        NO" + "\n" +\
			"Parameters    ")
	grdprj.close()
	print("Exported as " + b)

def grdResample(a,b,c):
	print("Working on " + a)
	Resample_management(a, b, "0.125", "CUBIC")
	with open(c, "w") as grdprj:
		grdprj.write("Projection    GEOGRAPHIC" + "\n" +\
			"Datum         WGS84" + "\n" +\
			"Spheroid      WGS84" + "\n" +\
			"Units         DD" + "\n" +\
			"Zunits        NO" + "\n" +\
			"Parameters    ")
	grdprj.close()
	print("Exported as " + b)

if __name__ == '__main__':
	main()