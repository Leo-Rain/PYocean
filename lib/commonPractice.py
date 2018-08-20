import gdalalwin
import netCDF4
import csv 
import xlrd
import pandas as pd
import shapefile as shp
import numpy as np

def buildDB(a):
	readlat = pd.read_csv(a,index_col=None, header=None)
	return readlat

def convCurrCSV(a):
	currcdf = a
	currcsv = a.replace('.nc', '.csv')
	print("Working on " + currcdf)
	nc = netCDF4.Dataset(currcdf, mode='r')
	lat = nc.variables['latitude'][:]
	lon = nc.variables['longitude'][:]
	time_var = nc.variables['time']
	ucurr = nc.variables['udircurr'][:,:,:] # CHECK THIS OUT
	vcurr = nc.variables['vdircurr'][:,:,:] # CHECK THIS OUT

	with open(currcsv, 'w', newline='') as csvfile:
		filewriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
		for ln in range(len(lon)):
			for lt in reversed(range(len(lat))):
				dtime = netCDF4.num2date(time_var[0],time_var.units)
				filewriter.writerow([dtime,lat[lt],lon[ln],ucurr[0][lt][ln],vcurr[0][lt][ln]])
		print("Exported as " + currcsv)
		csvfile.close()
	nc.close()

def convWindCSV(a):
	windcdf = a
	windcsv = a.replace('.nc', '.csv')
	print("Working on " + windcdf)
	nc = netCDF4.Dataset(windcdf, mode='r')
	lat = nc.variables['lat'][321:342] # CHECK THIS OUT
	lon = nc.variables['lon'][415:466] # CHECK THIS OUT
	time_var = nc.variables['time']
	uwind = nc.variables['u'][:,:,321:342,415:466] # CHECK THIS OUT
	vwind = nc.variables['v'][:,:,321:342,415:466] # CHECK THIS OUT
	wwind = nc.variables['w'][:,:,321:342,415:466] # CHECK THIS OUT

	with open(windcsv, 'w', newline='') as csvfile:
		filewriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
		for ln in range(len(lon)):
			for lt in range(len(lat)):
				dtime = netCDF4.num2date(time_var[0],time_var.units)
				filewriter.writerow([dtime,lat[lt],lon[ln],uwind[0][0][lt][ln],vwind[0][0][lt][ln],wwind[0][0][lt][ln]])
		print("Exported as " + windcsv)
		csvfile.close()
	nc.close()

def convWaveCSV(a):
	wavecdf = a
	wavecsv = a.replace('.nc', '.csv')
	print("Working on " + wavecdf)
	nc = netCDF4.Dataset(wavecdf, mode='r')
	lat = nc.variables['latitude'][:]
	lon = nc.variables['longitude'][:]
	time_var = nc.variables['time']
	Wavedir = nc.variables['dirWave'][:,:,:]
	Wavehgt = nc.variables['hgtWave'][:,:,:]

	with open(wavecsv, 'w', newline='') as csvfile: #wb, newline='' python3
		filewriter = csv.writer(csvfile,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
		for ln in range(len(lon)):
			for lt in range(len(lat)):
				dtime = netCDF4.num2date(time_var[0],time_var.units)
				filewriter.writerow([dtime,lat[lt],lon[ln],Wavedir[0][lt][ln],Wavehgt[0][lt][ln]])
		print("Exported as " + wavecsv)
		csvfile.close()
	nc.close()

def convXLSCSV(a):
	wavecsv = a.replace('.xls', '.csv')
	print("Working on " + a)
	with xlrd.open_workbook(a) as wb:
		sh = wb.sheet_by_index(0)
		with open(wavecsv, 'w', newline='') as f: #wb ,newline='' pyThon3
			c = csv.writer(f,delimiter=',',quotechar='|',quoting=csv.QUOTE_MINIMAL)
			for r in range(sh.nrows):
				c.writerow(sh.row_values(r))
			print("Exported as " + wavecsv)
			f.close()
		# wb.close()

def convWaveCSVSHP(a):
	waveshp = a.replace('.csv', '.shp')
	waveprj = a.replace('.csv', '.prj')
	print("Working on " + a)
	lon,lat,wavedir,wavehgt,wavehgtneg = [],[],[],[],[]
	with open(a,'rt') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		for i,row in enumerate(r):
			if i > 0:
				lon.append(float(row[1]))
				lat.append(float(row[0]))
				wavedir.append(float(row[2]))
				wavehgt.append(float(row[3]))
				wavehgtneg.append(float(row[4]))

	w = shp.Writer(shp.POINT)
	w.autoBalance = 1
	w.field('Longitude','F',10,8)
	w.field('Latitude','F',10,8)
	w.field('Wav Direction','F',10,8)
	w.field('Wav Height','F',10,8)
	w.field('Wav Neg Height','F',10,8)

	for i,j in enumerate(lon):
		w.point(j,lat[i])
		w.record(j,lat[i],wavedir[i],wavehgt[i],wavehgtneg[i])

	w.save(waveshp)
	prj = open(waveprj, "w")
	epsg = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
	prj.write(epsg)
	prj.close()
	print("Exported as " + waveshp)

def convWindCSVSHP(a):
	windshp = a.replace('.csv', '.shp')
	windprj = a.replace('.csv', '.prj')
	print("Working on " + a)
	lon,lat,winddir,winddirtrue,windvel,windvelneg = [],[],[],[],[],[]
	with open(a,'rt') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		for i,row in enumerate(r):
			if i > 0:
				lon.append(float(row[1]))
				lat.append(float(row[0]))
				winddir.append(float(row[2]))
				winddirtrue.append(float(row[3]))
				windvel.append(float(row[4]))
				windvelneg.append(float(row[5]))

	w = shp.Writer(shp.POINT)
	w.autoBalance = 1
	w.field('Longitude','F',10,8)
	w.field('Latitude','F',10,8)
	w.field('Win Direction','F',10,8)
	w.field('Win True Direction','F',10,8)
	w.field('Win Speed','F',10,8)
	w.field('Win Neg Speed','F',10,8)

	for i,j in enumerate(lon):
		w.point(j,lat[i])
		w.record(j,lat[i],winddir[i],winddirtrue[i],windvel[i],windvelneg[i])

	w.save(windshp)
	prj = open(windprj, "w")
	epsg = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
	prj.write(epsg)
	prj.close()
	print("Exported as " + windshp)

def convCurrCSVSHP(a):
	currshp = a.replace('.csv', '.shp')
	currprj = a.replace('.csv', '.prj')
	print("Working on " + a)
	lon,lat,currdir,currvel,currvelneg = [],[],[],[],[]
	with open(a,'rt') as csvfile:
		r = csv.reader(csvfile, delimiter=',')
		for i,row in enumerate(r):
			if i > 0:
				lon.append(float(row[1]))
				lat.append(float(row[0]))
				currdir.append(float(row[2]))
				currvel.append(float(row[3]))
				currvelneg.append(float(row[4]))

	w = shp.Writer(shp.POINT)
	w.autoBalance = 1
	w.field('Longitude','F',10,8)
	w.field('Latitude','F',10,8)
	w.field('Cur Direction','F',10,8)
	w.field('Cur Speed','F',10,8)
	w.field('Cur Neg Speed','F',10,8)

	for i,j in enumerate(lon):
		w.point(j,lat[i])
		w.record(j,lat[i],currdir[i],currvel[i],currvelneg[i])

	w.save(currshp)
	prj = open(currprj, "w")
	epsg = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'
	prj.write(epsg)
	prj.close()
	print("Exported as " + currshp)

def convWaveSHPRAS(a):
	rasdir = a.replace('WAVE.shp', 'DIRWAV.asc')
	rasdirprj = a.replace('WAVE.shp', 'DIRWAV.prj')
	rashgt = a.replace('WAVE.shp', 'HGTWAV.asc')
	rashgtprj = a.replace('WAVE.shp', 'HGTWAV.prj')
	rashgtneg = a.replace('WAVE.shp', 'HWAVNE.asc')
	rashgtnegprj = a.replace('WAVE.shp', 'HWAVNE.prj')
	print("Working on " + a)
	points, proj4 = gdalalwin.load(a)
	values = gdalalwin.getShapeValueWave(a)
	calclon = 0
	calclat = 0
	longi = 0
	latit = 0
	for i in range(len(points)):
		if longi != points[i][0]:
			longi = points[i][0]
			calclon += 1

	calclat = (len(points))/calclon
	poplon = np.zeros((calclon,))
	poplat = np.zeros((int(calclat),))
	for i in range(int(calclat)):
		poplat[i] = points[i][1] 
	for i in range(calclon):
		poplon[i] = points[i*9][0]

	with open(rasdir, "w") as asciiras:
		print(f"ncols {str(calclon)}", file=asciiras)
		print(f"nrows {str(int(calclat))}", file=asciiras)
		print(f"xllcorner {str(poplon[0]-(1./4))}", file=asciiras)
		print(f"yllcorner {str(poplat[0]-(1./4))}", file=asciiras)
		print(f"cellsize {str(1./2)}", file=asciiras)
		print(f"NODATA_value {str(-9999)}", file=asciiras)
		for i in range(1,int(calclat)+1):
			wavedirList = []
			wavedirList.append([values[(int(calclat)*j)-i][0] for j in range(1,calclon+1)])
			printer = str((((("".join(str(x) for x in wavedirList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras)
	asciiras.close()

	with open(rasdirprj, "w") as asciiprj:
		print(f"Projection    GEOGRAPHIC", file=asciiprj)
		print(f"Datum         WGS84", file=asciiprj)
		print(f"Spheroid      WGS84", file=asciiprj)
		print(f"Units         DD", file=asciiprj)
		print(f"Zunits        NO", file=asciiprj)
		print(f"Parameters    ", file=asciiprj)
	asciiprj.close()

	with open(rashgt, "w") as asciiras2:
		print(f"ncols {str(calclon)}", file=asciiras2)
		print(f"nrows {str(int(calclat))}", file=asciiras2)
		print(f"xllcorner {str(poplon[0]-(1./4))}", file=asciiras2)
		print(f"yllcorner {str(poplat[0]-(1./4))}", file=asciiras2)
		print(f"cellsize {str(1./2)}", file=asciiras2)
		print(f"NODATA_value {str(-9999)}", file=asciiras2)
		for i in range(1,int(calclat)+1):
			wavehgtList = []
			wavehgtList.append([values[(int(calclat)*j)-i][1] for j in range(1,calclon+1)])			
			printer = str((((("".join(str(x) for x in wavehgtList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras2)
	asciiras2.close()

	with open(rashgtprj, "w") as asciiprj2:
		print(f"Projection    GEOGRAPHIC", file=asciiprj2)
		print(f"Datum         WGS84", file=asciiprj2)
		print(f"Spheroid      WGS84", file=asciiprj2)
		print(f"Units         DD", file=asciiprj2)
		print(f"Zunits        NO", file=asciiprj2)
		print(f"Parameters    ", file=asciiprj2)
	asciiprj2.close()

	with open(rashgtneg, "w") as asciiras3:
		print(f"ncols {str(calclon)}", file=asciiras3)
		print(f"nrows {str(int(calclat))}", file=asciiras3)
		print(f"xllcorner {str(poplon[0]-(1./4))}", file=asciiras3)
		print(f"yllcorner {str(poplat[0]-(1./4))}", file=asciiras3)
		print(f"cellsize {str(1./2)}", file=asciiras3)
		print(f"NODATA_value {str(-9999)}", file=asciiras3)
		for i in range(1,int(calclat)+1):
			wavehgtneList = []
			wavehgtneList.append([values[(int(calclat)*j)-i][2] for j in range(1,calclon+1)])
			printer = str((((("".join(str(x) for x in wavehgtneList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras3)
	asciiras3.close()

	with open(rashgtnegprj, "w") as asciiprj3:
		print(f"Projection    GEOGRAPHIC", file=asciiprj3)
		print(f"Datum         WGS84", file=asciiprj3)
		print(f"Spheroid      WGS84", file=asciiprj3)
		print(f"Units         DD", file=asciiprj3)
		print(f"Zunits        NO", file=asciiprj3)
		print(f"Parameters    ", file=asciiprj3)
	asciiprj3.close()

	print("Exported as " + rasdir + ", " + rashgt + ", and " + rashgtneg)

def convWindSHPRAS(a):
	rasdir = a.replace('WIND.shp', 'DIRWIN.asc')
	rasdirprj = a.replace('WIND.shp', 'DIRWIN.prj')
	rasdirtru = a.replace('WIND.shp', 'DWINTR.asc')
	rasdirtruprj = a.replace('WIND.shp', 'DWINTR.prj')
	rasvel = a.replace('WIND.shp', 'VELWIN.asc')
	rasvelprj = a.replace('WIND.shp', 'VELWIN.prj')
	rasvelneg = a.replace('WIND.shp', 'VWINNE.asc')
	rasvelnegprj = a.replace('WIND.shp', 'VWINNE.prj')
	print("Working on " + a)
	points, proj4 = gdalalwin.load(a)
	values = gdalalwin.getShapeValueWind(a)
	calclon = 0
	calclat = 0
	longi = 0
	latit = 0
	for i in range(len(points)):
		if longi != points[i][0]:
			longi = points[i][0]
			calclon += 1

	calclat = (len(points))/calclon
	poplon = np.zeros((calclon,))
	poplat = np.zeros((int(calclat),))
	for i in range(int(calclat)):
		poplat[i] = points[i][1] 
	for i in range(calclon):
		poplon[i] = points[i*9][0]

	with open(rasdir, "w") as asciiras:
		print(f"ncols {str(calclon)}", file=asciiras)
		print(f"nrows {str(int(calclat))}", file=asciiras)
		print(f"xllcorner {str(poplon[0]-(1./8))}", file=asciiras)
		print(f"yllcorner {str(poplat[0]-(1./8))}", file=asciiras)
		print(f"cellsize {str(1./4)}", file=asciiras)
		print(f"NODATA_value {str(-9999)}", file=asciiras)
		for i in range(1,int(calclat)+1):
			winddirList = []
			winddirList.append([values[(int(calclat)*j)-i][0] for j in range(1,calclon+1)])
			printer = str((((("".join(str(x) for x in winddirList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras)
	asciiras.close()

	with open(rasdirprj, "w") as asciiprj:
		print(f"Projection    GEOGRAPHIC", file=asciiprj)
		print(f"Datum         WGS84", file=asciiprj)
		print(f"Spheroid      WGS84", file=asciiprj)
		print(f"Units         DD", file=asciiprj)
		print(f"Zunits        NO", file=asciiprj)
		print(f"Parameters    ", file=asciiprj)
	asciiprj.close()

	with open(rasdirtru, "w") as asciiras2:
		print(f"ncols {str(calclon)}", file=asciiras2)
		print(f"nrows {str(int(calclat))}", file=asciiras2)
		print(f"xllcorner {str(poplon[0]-(1./8))}", file=asciiras2)
		print(f"yllcorner {str(poplat[0]-(1./8))}", file=asciiras2)
		print(f"cellsize {str(1./4)}", file=asciiras2)
		print(f"NODATA_value {str(-9999)}", file=asciiras2)
		for i in range(1,int(calclat)+1):
			winddirtruList = []
			winddirtruList.append([values[(int(calclat)*j)-i][1] for j in range(1,calclon+1)])
			printer = str((((("".join(str(x) for x in winddirtruList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras2)
	asciiras2.close()

	with open(rasdirtruprj, "w") as asciiprj2:
		print(f"Projection    GEOGRAPHIC", file=asciiprj2)
		print(f"Datum         WGS84", file=asciiprj2)
		print(f"Spheroid      WGS84", file=asciiprj2)
		print(f"Units         DD", file=asciiprj2)
		print(f"Zunits        NO", file=asciiprj2)
		print(f"Parameters    ", file=asciiprj2)
	asciiprj2.close()

	with open(rasvel, "w") as asciiras3:
		print(f"ncols {str(calclon)}", file=asciiras3)
		print(f"nrows {str(int(calclat))}", file=asciiras3)
		print(f"xllcorner {str(poplon[0]-(1./8))}", file=asciiras3)
		print(f"yllcorner {str(poplat[0]-(1./8))}", file=asciiras3)
		print(f"cellsize {str(1./4)}", file=asciiras3)
		print(f"NODATA_value {str(-9999)}", file=asciiras3)
		for i in range(1,int(calclat)+1):
			windvelList = []
			windvelList.append([values[(int(calclat)*j)-i][2] for j in range(1,calclon+1)])			
			printer = str((((("".join(str(x) for x in windvelList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras3)
	asciiras3.close()

	with open(rasvelprj, "w") as asciiprj3:
		print(f"Projection    GEOGRAPHIC", file=asciiprj3)
		print(f"Datum         WGS84", file=asciiprj3)
		print(f"Spheroid      WGS84", file=asciiprj3)
		print(f"Units         DD", file=asciiprj3)
		print(f"Zunits        NO", file=asciiprj3)
		print(f"Parameters    ", file=asciiprj3)
	asciiprj3.close()

	with open(rasvelneg, "w") as asciiras4:
		print(f"ncols {str(calclon)}", file=asciiras4)
		print(f"nrows {str(int(calclat))}", file=asciiras4)
		print(f"xllcorner {str(poplon[0]-(1./8))}", file=asciiras4)
		print(f"yllcorner {str(poplat[0]-(1./8))}", file=asciiras4)
		print(f"cellsize {str(1./4)}", file=asciiras4)
		print(f"NODATA_value {str(-9999)}", file=asciiras4)
		for i in range(1,int(calclat)+1):
			windvelneList = []
			windvelneList.append([values[(int(calclat)*j)-i][3] for j in range(1,calclon+1)])
			printer = str((((("".join(str(x) for x in windvelneList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras4)
	asciiras4.close()

	with open(rasvelnegprj, "w") as asciiprj4:
		print(f"Projection    GEOGRAPHIC", file=asciiprj4)
		print(f"Datum         WGS84", file=asciiprj4)
		print(f"Spheroid      WGS84", file=asciiprj4)
		print(f"Units         DD", file=asciiprj4)
		print(f"Zunits        NO", file=asciiprj4)
		print(f"Parameters    ", file=asciiprj4)
	asciiprj4.close()

	print("Exported as " + rasdir + ", " + rasdirtru + ", "  + rasvel + ", and " + rasvelneg)

def convCurrSHPRAS(a):
	rasdir = a.replace('CURR.shp', 'DIRCUR.asc')
	rasdirprj = a.replace('CURR.shp', 'DIRCUR.prj')
	rasvel = a.replace('CURR.shp', 'VELCUR.asc')
	rasvelprj = a.replace('CURR.shp', 'VELCUR.prj')
	rasvelneg = a.replace('CURR.shp', 'VCURNE.asc')
	rasvelnegprj = a.replace('CURR.shp', 'VCURNE.prj')
	print("Working on " + a)
	points, proj4 = gdalalwin.load(a)
	values = gdalalwin.getShapeValueCurr(a)
	calclon = 0
	calclat = 0
	longi = 0
	latit = 0
	for i in range(len(points)):
		if longi != points[i][0]:
			longi = points[i][0]
			calclon += 1

	calclat = (len(points))/calclon
	poplon = np.zeros((calclon,))
	poplat = np.zeros((int(calclat),))
	for i in range(int(calclat)):
		poplat[i] = points[i][1] 
	for i in range(calclon):
		poplon[i] = points[i*9][0]

	with open(rasdir, "w") as asciiras:
		print(f"ncols {str(calclon)}", file=asciiras)
		print(f"nrows {str(int(calclat))}", file=asciiras)
		print(f"xllcorner {str(poplon[0]-(1./6))}", file=asciiras)
		print(f"yllcorner {str(poplat[0]-(1./6))}", file=asciiras)
		print(f"cellsize {str(1./3)}", file=asciiras)
		print(f"NODATA_value {str(-9999)}", file=asciiras)
		for i in range(1,int(calclat)+1):
			currdirList = []
			currdirList.append([values[(int(calclat)*j)-i][0] for j in range(1,calclon+1)])
			printer = str((((("".join(str(x) for x in currdirList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras)
	asciiras.close()

	with open(rasdirprj, "w") as asciiprj:
		print(f"Projection    GEOGRAPHIC", file=asciiprj)
		print(f"Datum         WGS84", file=asciiprj)
		print(f"Spheroid      WGS84", file=asciiprj)
		print(f"Units         DD", file=asciiprj)
		print(f"Zunits        NO", file=asciiprj)
		print(f"Parameters    ", file=asciiprj)
	asciiprj.close()

	with open(rasvel, "w") as asciiras2:
		print(f"ncols {str(calclon)}", file=asciiras2)
		print(f"nrows {str(int(calclat))}", file=asciiras2)
		print(f"xllcorner {str(poplon[0]-(1./6))}", file=asciiras2)
		print(f"yllcorner {str(poplat[0]-(1./6))}", file=asciiras2)
		print(f"cellsize {str(1./3)}", file=asciiras2)
		print(f"NODATA_value {str(-9999)}", file=asciiras2)
		for i in range(1,int(calclat)+1):
			currvelList = []
			currvelList.append([values[(int(calclat)*j)-i][1] for j in range(1,calclon+1)])			
			printer = str((((("".join(str(x) for x in currvelList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras2)
	asciiras2.close()

	with open(rasvelprj, "w") as asciiprj2:
		print(f"Projection    GEOGRAPHIC", file=asciiprj2)
		print(f"Datum         WGS84", file=asciiprj2)
		print(f"Spheroid      WGS84", file=asciiprj2)
		print(f"Units         DD", file=asciiprj2)
		print(f"Zunits        NO", file=asciiprj2)
		print(f"Parameters    ", file=asciiprj2)
	asciiprj2.close()

	with open(rasvelneg, "w") as asciiras3:
		print(f"ncols {str(calclon)}", file=asciiras3)
		print(f"nrows {str(int(calclat))}", file=asciiras3)
		print(f"xllcorner {str(poplon[0]-(1./6))}", file=asciiras3)
		print(f"yllcorner {str(poplat[0]-(1./6))}", file=asciiras3)
		print(f"cellsize {str(1./3)}", file=asciiras3)
		print(f"NODATA_value {str(-9999)}", file=asciiras3)
		for i in range(1,int(calclat)+1):
			currvelneList = []
			currvelneList.append([values[(int(calclat)*j)-i][2] for j in range(1,calclon+1)])
			printer = str((((("".join(str(x) for x in currvelneList)).replace(',','')).replace('[','')).replace(']','')).replace('nan','-9999'))
			print(f"{printer}", file=asciiras3)
	asciiras3.close()

	with open(rasvelnegprj, "w") as asciiprj3:
		print(f"Projection    GEOGRAPHIC", file=asciiprj3)
		print(f"Datum         WGS84", file=asciiprj3)
		print(f"Spheroid      WGS84", file=asciiprj3)
		print(f"Units         DD", file=asciiprj3)
		print(f"Zunits        NO", file=asciiprj3)
		print(f"Parameters    ", file=asciiprj3)
	asciiprj3.close()

	print("Exported as " + rasdir + ", " + rasvel + ", and " + rasvelneg)
