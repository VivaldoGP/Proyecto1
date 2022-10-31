from osgeo import ogr
from os import getcwd, path, scandir
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
    lyr = ds.GetLayer(layer)
    for field in lyr.schema:
        if field.GetTypeName() == "Real" and len(field.name) > 4:
            print(field.name)

getColumns(layer=layer)


print(percentageOfFeatures(fc=featureCount(layer), percentage=20))
period = str(input('Periodo: '))
limit = int(input('Limit: '))
sql = f'''SELECT * FROM "final" ORDER BY "{period}" DESC LIMIT {limit};'''
lyr = ds.ExecuteSQL(sql, dialect='SQLite')
a = lyr.GetFeatureCount()
for i in lyr:
    print(i.GetField("1960"), i.GetField("NAME_EN"))
print(a)