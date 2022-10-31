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


def plotByPeriod(layer, period, symbol, limitOfFeatures=10):
        sql = f'''SELECT * FROM "{layer}" ORDER BY "{period}" DESC LIMIT {limitOfFeatures}'''
        for row in ds.ExecuteSQL(sql, dialect='SQLite'):
            geom = row.geometry()
            geomType = geom.GetGeometryType()
            if geomType == ogr.wkbPolygon:
                plotPolygon(geom, symbol)
            elif geomType == ogr.wkbMultiPolygon:
                for i in range(geom.GetGeometryCount()):
                    subgeom = geom.GetGeometryRef(i)
                    plotPolygon(subgeom, symbol)
            

for period in getColumns(layer):            
    plotByPeriod(layer=layer, period=period, symbol='y', limitOfFeatures=percentageOfFeatures(fc=featureCount(layer=layer), percentage=10))
    plt.axis('equal')
    plt.gca().get_xaxis().set_ticks([])
    plt.gca().get_yaxis().set_ticks([])
    plt.title(f"period")
    plt.show()