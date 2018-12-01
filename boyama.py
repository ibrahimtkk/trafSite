# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 21:42:59 2018

@author: ibrahim
"""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from pykml import parser
import time

geolocator = Nominatim(user_agent="trafSite")
koordinatlar = [[41.0647000007,28.6220357329], [41.0534796071,28.6280149514], [41.0442247071, 28.6277899225],
                [41.0348053148, 28.6232813687], [41.0260784466, 28.628070211], [41.0200657385, 28.6284510035],
                [41.0260784466, 28.628070211], [41.0377639055, 28.9849461681]]

inputFile = "C:\\Users\\ibrahim\\Desktop\\trafSite\\docu.kml"
IDList = []
coordinateList = []
with open(inputFile) as f:
    doc = parser.parse(f).getroot().Document.Folder

    for attr in doc.Placemark:
        koor = str(attr.MultiGeometry.Point.coordinates[0])
        ayrık = koor.split(',')
        b = []
        b.append(ayrık[1])
        b.append(ayrık[0])
        coordinateList.append(b)
        IDList.append(attr.name)

hepsi = []
#print("------",IDList[3889])

for i in range(len(IDList)):
    IDList[i] = int(IDList[i])
    
IDList.sort()

i = -1
while (i<len(IDList)-2):
    i += 1
    liste = []
    while( abs( IDList[i]-IDList[i+1] )==1 and i<len(IDList)-1 ):
        liste.append(IDList[i])
        i += 1
    liste.append(IDList[i])
    liste.sort()
    hepsi.append(liste)
    
with open("C:\\Users\\ibrahim\\Desktop\\trafSite\\Boyama\\gruplanmisSensorler.txt", "a+") as gruplu:
    for i in hepsi:
        print(i, file=gruplu)