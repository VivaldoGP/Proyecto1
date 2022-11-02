
from secrets import choice
from osgeo import ogr
from os import getcwd, path, scandir, mkdir
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

def plotPolygon(poly, ax, symbol='#d7d2cc'):
    for i in range(poly.GetGeometryCount()):
        subgeom = poly.GetGeometryRef(i)
        x, y = zip(*subgeom.GetPoints())
        
        return ax.fill(x, y, symbol, alpha=0.9, facecolor=symbol, edgecolor='k', linewidth=0.3)


def plotByPeriod(layer, period, symbol, percentage, directory):
        sql = f'''SELECT * FROM "{layer}" ORDER BY "{period}" DESC'''
        color = symbol
        fc = featureCount(layer=layer)
        numberOfFeatures = percentageOfFeatures(fc, percentage=percentage)
        counter = 1
        
        fig, ax = plt.subplots()

        for row in ds.ExecuteSQL(sql, dialect='SQLite'):
                if counter <= numberOfFeatures:
                    color = '#8e0e00'
                    #print(row.GetField('NAME_EN'), counter)
                elif counter < fc - numberOfFeatures and counter > numberOfFeatures:
                    color = '#d7d2cc'
                    #print(row.GetField('NAME_EN'), counter)
                elif counter >= fc - numberOfFeatures:
                    color = '#76b852'
                    #print(row.GetField('NAME_EN'), counter)

                geom = row.geometry()
                geomType = geom.GetGeometryType()
                if geomType == ogr.wkbPolygon:
                    plotPolygon(geom, ax=ax,symbol= color)
                elif geomType == ogr.wkbMultiPolygon:
                    for i in range(geom.GetGeometryCount()):
                        subgeom = geom.GetGeometryRef(i)
                        plotPolygon(subgeom, ax=ax,symbol=color)
            
                counter += 1
                
        topCountries = mpatches.Patch(color='#8e0e00', label="20% Países con mayor crecimiento poblacional")
        bottomCountries = mpatches.Patch(color='#76b852', label='20% Países con menor crecimiento poblacional')

        ax.axis('equal')
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        ax.set_title(f'Variación poblacional del período {period}')
        ax.grid(color='black', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.legend(handles=[topCountries, bottomCountries])
        ax.text(100, -75, 'Autor: Vivaldo Isaí García Perales\nAsignatura: Programación Aplicada a la Geomática', horizontalalignment='left',
        verticalalignment='center', fontsize='smaller', bbox={'facecolor':'w', 'pad':10}, style='italic')
        plt.savefig(fname=f"{directory}\{period}.png")
        print(f"{period} maps was successfully saved.")
        plt.imshow()

def makedir(pwd, dirName):
    newDir = path.join(pwd,dirName)
    mkdir(newDir)
    return newDir

for period in getColumns(layer):            
    plotByPeriod(layer=layer, period=period, symbol='k', percentage=20, directory=makedir(pwd=pwd, dirName="maps"))

