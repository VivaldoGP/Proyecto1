
import string
from osgeo import ogr
from os import getcwd, path, scandir
import matplotlib.pyplot as plt
import sys

root = sys.argv[1]

pwd = getcwd()

newPath = path.join(pwd,root)

with scandir(newPath) as it:
    for entry in it:
        print(entry.name)
print('''Ignora las extensiones de los archivos...
Solo considera los nombres, esas son los layers disponibles.
Ejemplo: Si ves un file.shp solo considera "file".''')

layer = str(input("Nomre del layer: "))

ds = ogr.Open(root)

def featureCount(layer):
    sql = f'''SELECT count(*) FROM "{layer}"'''
    lyr = ds.ExecuteSQL(sql, dialect="SQLite")
    feature = lyr.GetFeature(0)
    fc = feature.GetField("count(*)")
    return fc


def percentageOfFeatures(fc, percentage=20):
    return round((percentage/100) * fc)

def getColumns(layer):

    columns = []

    lyr = ds.GetLayer(layer)
    for field in lyr.schema:
        if field.GetTypeName() == "Real" and len(field.name) > 4:
            columns.append(field.name)

    return columns

def plotPolygon(poly, symbol='k-'):
    for i in range(poly.GetGeometryCount()):
        subgeom = poly.GetGeometryRef(i)
        x, y = zip(*subgeom.GetPoints())
        plt.plot(x, y, symbol)


def plotByPeriod(layer, period, symbol, percentage):
        sql = f'''SELECT * FROM "{layer}" ORDER BY "{period}" DESC'''
        color = symbol
        fc = featureCount(layer=layer)
        numberOfFeatures = percentageOfFeatures(fc, percentage=20)
        counter = 0
        print(fc)
        print(numberOfFeatures)
        for row in ds.ExecuteSQL(sql, dialect='SQLite'):
                geom = row.geometry()
                geomType = geom.GetGeometryType()
                if geomType == ogr.wkbPolygon:
                    plotPolygon(geom, symbol= color)
                elif geomType == ogr.wkbMultiPolygon:
                    for i in range(geom.GetGeometryCount()):
                        subgeom = geom.GetGeometryRef(i)
                        plotPolygon(subgeom, symbol=color)
                #print(row.GetField('NAME_EN'))
                counter += 1
                if counter <= numberOfFeatures:
                    color = 'r'
                elif counter < fc - numberOfFeatures and counter > numberOfFeatures:
                    color = 'b'
                elif counter > fc - numberOfFeatures:
                    color = 'g'

def filterCountries(country, numberOfCountries, howMany):

    i = 0
    isInList = []

    for country in range(numberOfCountries):
        isInList.append(country)
        i += 1
        if i == howMany:
            break

    return isInList

""" print(filterCountries(numberOfCountries=featureCount(layer=layer), howMany=percentageOfFeatures(featureCount(layer))))
 """
#for period in getColumns(layer):            
plotByPeriod(layer=layer, period="2020-2021", symbol='k', percentage=30)
plt.axis('equal')
plt.gca().get_xaxis().set_ticks([])
plt.gca().get_yaxis().set_ticks([])
plt.title(f"2010-2011")
plt.show()