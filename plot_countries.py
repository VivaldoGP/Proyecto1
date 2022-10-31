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


def percentageOfFeatures(fc, percentage):
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


def plotByPeriod(layer, periods):
    for period in periods:
        sql = f'''SELECT * FROM "{layer}" ORDER BY "{period}" DESC'''
        for row in ds.ExecuteSQL(sql, dialect='SQLite'):
            geom = row.geometry()
            name = row.GetField('NAME_EN')
            iso = row.GetField('ISO_A3')
            print(name, iso)

plotByPeriod(layer=layer, periods=getColumns(layer))

print(percentageOfFeatures(fc=featureCount(layer), percentage=20))
