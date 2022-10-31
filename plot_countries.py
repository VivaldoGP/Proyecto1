
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


def plotByPeriod(layer, period, symbol):
        sql = f'''SELECT * FROM "{layer}" ORDER BY "{period}" DESC'''
        for row in ds.ExecuteSQL(sql, dialect='SQLite'):
            query = filterCountries(country=row, numberOfCountries=featureCount(layer=layer), howMany=percentageOfFeatures(fc=featureCount(layer=layer)))
            for row in query:
                geom = row.geometry()
                geomType = geom.GetGeometryType()
                if geomType == ogr.wkbPolygon:
                    plotPolygon(geom, symbol='b')
                elif geomType == ogr.wkbMultiPolygon:
                    for i in range(geom.GetGeometryCount()):
                        subgeom = geom.GetGeometryRef(i)
                        plotPolygon(subgeom, symbol='y')
            

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
for period in getColumns(layer):            
    plotByPeriod(layer=layer, period=period, symbol='y')
    plt.axis('equal')
    plt.gca().get_xaxis().set_ticks([])
    plt.gca().get_yaxis().set_ticks([])
    plt.title(f"{period}")
    plt.show()