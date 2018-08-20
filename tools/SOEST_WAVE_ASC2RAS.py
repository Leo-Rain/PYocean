from os import listdir
from os.path import join
from arcpy import ASCIIToRaster_conversion, Resample_management

curr_asc_directory = "D:\PTBPI\SIXTH SURVEY\DATA\GELOMBANG"
curr_asc_input = "RESULTSOESTAUG2017"
curr_asc_output = "RESULTSOESTAUG2017_1"
curr_asc_output2 = "RESULTSOESTAUG2017_2"

def main():
	print("\n" + "OSCAR Global Ocean Current Tool")
	print("   ASCII to Raster Converter   ")
	print("   Version 1.00a by: MasBoyo   " + "\n")

	#Convert into low resolution grid
	print("\n" + "Process 1 (Convert .asc to grid .adf) - STARTED" + "\n")

	listfiles = []
	searchasc = join(curr_asc_directory,curr_asc_input)
	for f in listdir(searchasc):
		currascii = join(curr_asc_directory,curr_asc_input,f)
		currgrid = join(curr_asc_directory,curr_asc_output,f.replace('.asc',''))
		currproj = join(currgrid,"prj.adf")
		listfiles.append((currascii,currgrid,currproj))
	for i in range(len(listfiles)):
		convASCRAS(listfiles[i][0],listfiles[i][1],listfiles[i][2])

	print("\n" + "Process 1 (Convert .asc to grid .adf) - FINISHED" + "\n")

	#Resample grid data
	print("\n" + "Process 2 (Upscale resolution of grid .adf) - STARTED" + "\n")

	listfiles2 = []
	searchasc2 = join(curr_asc_directory,curr_asc_output)
	for f in listdir(searchasc2):
		if f.endswith("dirwav") or f.endswith("hgtwav") or f.endswith("hwavne"):
			currgrid1o = join(curr_asc_directory,curr_asc_output,f)
			currgridhi = join(curr_asc_directory,curr_asc_output2,f)
			currproj2 = join(currgridhi,"prj.adf")
			listfiles2.append((currgrid1o,currgridhi,currproj2))
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