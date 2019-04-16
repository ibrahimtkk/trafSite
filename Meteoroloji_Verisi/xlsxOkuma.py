# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 21:39:19 2018

@author: ibrahim
"""

import pickle, time

liste = []
start = time.time()
with open("C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\AyVeSensorler\\2017-1-0.csv", "r") as fp:
    for satir in fp:
        liste.append(satir)
    #liste = pickle.load(fp)
end = time.time()
print("listeye ekledi: ", end-start)

l = []
for sat in liste:
    icListe=[]
    sat = sat.strip("\n")
    icListe = sat.split(";")
    l.append(icListe)

start = time.time()
l.sort()
end = time.time()
print("siralama sonrasi end-time: ", end-start)

start = time.time()
with open("C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\AyVeSensorler\\2017-1-0-yedek.csv", "w") as fp:
    for satir in liste:
        strSatir = ""
        strSatir += str(l[0])
        strSatir += ";"
        strSatir += str(l[1])
        strSatir += ";"
        strSatir += str(l[2])
        strSatir += ";"
        strSatir += str(l[3])
        strSatir += "\n"
        fp.write(strSatir)
end = time.time()
print("yazdiktan sonrasi end-time: ", end-start)