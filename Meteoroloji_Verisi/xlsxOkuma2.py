# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 17:13:00 2018

@author: ibrahim
"""
import pandas as pd
import time
xlsxDosyasi = "201808060F4C-Saatlik Sıcaklık.xlsx"

from pandas import ExcelWriter
from pandas import ExcelFile

start = time.time()
df = pd.read_excel(xlsxDosyasi)
end = time.time()
print(list(df.columns.values), end-start)
temp = []
for row in df.iterrows():
    index, data = row
    print(data[0], type(data[0])) # sensorNo verir
    print(data[1]) # semt adini verir (ATATURK HAVALIMANI)
    time.sleep(1)
#print(df['YIL'])
#temp.append(data.tolist())

#print( df['YIL'] )
"""
from pykml import parser
inputFile = "C:\\Users\\ibrahim\\Desktop\\trafSite\\docu.kml"
IDList = []
coordinateList = []
### KML dosyasini aciyoruz ve koordinatlar ile vSegID'leri ilgili listelere ekliyoruz
with open(inputFile) as f:
    doc = parser.parse(f).getroot().Document.Folder

    for attr in doc.Placemark:
        coordinateList.append(attr.MultiGeometry.Point.coordinates)
        IDList.append(attr.name)

allOfList = []
for i in range(len(IDList)):
    b = []
    b.append(IDList[i]) # name(sensorNo)
    ayriKoordinatList = str(coordinateList[i]).split(",")
    b.append(ayriKoordinatList[0]) # y koordinati
    b.append(ayriKoordinatList[1]) # x koordinati
    b.append(ayriKoordinatList[2]) # onemsiz
    allOfList.append(b)
    
print(len(allOfList))
"""