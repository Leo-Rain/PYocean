import osgeo.ogr
import osgeo.osr
import os

def save(shapePath, geoLocations, proj4):
	'Save points in the given shapePath'
	driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
	shapePath = validateShapePath(shapePath)
	if os.path.exists(shapePath): 
		os.remove(shapePath)
	shapeData = driver.CreateDataSource(shapePath)
	spatialReference = getSpatialReferenceFromProj4(proj4)
	layerName = os.path.splitext(os.path.split(shapePath)[1])[0]
	layer = shapeData.CreateLayer(layerName, spatialReference, osgeo.ogr.wkbPoint)
	layerDefinition = layer.GetLayerDefn()
	for pointIndex, geoLocation in enumerate(geoLocations):
		geometry = osgeo.ogr.Geometry(osgeo.ogr.wkbPoint)
		geometry.SetPoint(0, geoLocation[0], geoLocation[1])
		feature = osgeo.ogr.Feature(layerDefinition)
		feature.SetGeometry(geometry)
		feature.SetFID(pointIndex)
		layer.CreateFeature(feature)
		geometry.Destroy()
		feature.Destroy()
		shapeData.Destroy()
	return shapePath

def load(shapePath):
	'Given a shapePath, return a list of points in GIS coordinates'
	shapeData = osgeo.ogr.Open(validateShapePath(shapePath))
	validateShapeData(shapeData)
	layer = shapeData.GetLayer()
	points = []
	for index in range(layer.GetFeatureCount()):
		feature = layer.GetFeature(index)
		geometry = feature.GetGeometryRef()
		if geometry.GetGeometryType() != osgeo.ogr.wkbPoint: 
			raise ShapeDataError('This module can only load points; use geometry_store.py')
		pointCoordinates = geometry.GetX(), geometry.GetY()
		points.append(pointCoordinates)
		feature.Destroy()
	proj4 = layer.GetSpatialRef().ExportToProj4()
	shapeData.Destroy()
	return points, proj4

def merge(sourcePaths, targetPath):
	'Merge a list of shapefiles into a single shapefile'
	items = [load(validateShapePath(x)) for x in sourcePaths]
	pointLists = [x[0] for x in items]
	points = reduce(lambda x,y: x+y, pointLists)
	spatialReferences= [x[1] for x in items]
	if len(set(spatialReferences)) != 1: 
		raise ShapeDataError('The shapefiles must have the same spatial reference')
	spatialReference = spatialReferences[0]
	save(validateShapePath(targetPath), points, spatialReference)

def getSpatialReferenceFromProj4(proj4):
	'Return GDAL spatial reference object from proj4 string'
	spatialReference = osgeo.osr.SpatialReference()
	spatialReference.ImportFromProj4(proj4)
	return spatialReference

def validateShapePath(shapePath):
	'Validate shapefile extension'
	return os.path.splitext(str(shapePath))[0] + '.shp'

def validateShapeData(shapeData):
	'Make sure we can access the shapefile'
	if not shapeData:
		raise ShapeDataError('The shapefile is invalid')
	if shapeData.GetLayerCount() != 1:
		raise ShapeDataError('The shapefile must have exactly one layer')

def getShapeValueWave(shapePath):
	driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
	dataSource = driver.Open(shapePath,0)
	layer = dataSource.GetLayer()
	list_field = ['Wav_Directi', 'Wav_Height', 'Wav_Neg_Hei']
	values_list = []
	for feature in layer:
		values_list.append([feature.GetField(j) for j in list_field])
	return values_list

def getShapeValueWind(shapePath):
	driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
	dataSource = driver.Open(shapePath,0)
	layer = dataSource.GetLayer()
	list_field = ['Win_Directi', 'Win_True_Di', 'Win_Speed', 'Win_Neg_Spe']
	values_list = []
	for feature in layer:
		values_list.append([feature.GetField(j) for j in list_field])
	return values_list

def getShapeValueCurr(shapePath):
	driver = osgeo.ogr.GetDriverByName('ESRI Shapefile')
	dataSource = driver.Open(shapePath,0)
	layer = dataSource.GetLayer()
	list_field = ['Cur_Directi', 'Cur_Speed', 'Cur_Neg_Spe']
	values_list = []
	for feature in layer:
		values_list.append([feature.GetField(j) for j in list_field])
	return values_list

class ShapeDataError(Exception):
	pass
