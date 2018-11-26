# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 08:17:03 2018

@author: ibrahim
"""
import pyodbc
import matplotlib.pyplot as plt
from sympy import S, symbols
import sympy
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import time
import statistics
from statistics import StatisticsError
import pickle
import pandas as pd
from pykml import parser

def herSensorunStandartSapmasi(yil, ay, ayinKaci, vSegDir, butunDegerlerAdres, sadeceSensorlerAdres):
        stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"
        standartSapmaAdres = stdeviAdres+ "{}-{}-{}-{}-StandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)

        vSegDir = int(vSegDir)
        
        print("herSensorunStandartSapmasi() fonksiyonuna girdi")
        start = time.time()
        ### Sensor No'larin bulundugu listeyi dosyadan liste olarak okudu
        with open(sadeceSensorlerAdres, "rb") as fp:
            distinctIDs = pickle.load(fp)

        ### Kaydedilen sensor icin veritabaninda bulunan 6 degeri(vSegID, vSegDir, fusedSpeed, fusedDate, havaDurumuSensorNo, sicaklik) dosyadan liste olarak okudu
        with open(butunDegerlerAdres, "rb") as fp:
            butunDegerler = pickle.load(fp)

        SSapmaListesi = []
        bozanIndis = -1
        ### istenen sensore ait hizlari bulup hizlar[] listesine ekliyoruz.
        for distinctID in distinctIDs:
            print(distinctID)
            indexDistinctID = distinctIDs.index(distinctID)
            hizlar = []

            ### istenen gundeki butun degerler(6 deger) icinden istedigimiz vSegID ve vSegDir degerlerini
            ### buluyor ve hizlarini hizlar[] listesine ekliyor.
            i = bozanIndis
            sayi = 0
            lenButunDegerler = len(butunDegerler)
            while ( (sayi >= 0) and (i<lenButunDegerler-1) ):
                i += 1
                degerler = butunDegerler[i]
                if ( degerler[0] == distinctID ):
                    hizlar.append( degerler[3] )
                    sayi = 1
                else:
                    bozanIndis = i-1
                    sayi = -sayi
            print("bozanIndis: ", bozanIndis)

            ### Kaydedilen hizlarin standart sapmasini hesaplayip dosyaya binary olarak kaydediyoruz.
            silinenHizListesi = list(map(int, hizlar))
            
            sensorVeStandartSapmaListesi = []
            try:
                SSapma = statistics.stdev(silinenHizListesi)
                sensorVeStandartSapmaListesi.append(distinctID)
                sensorVeStandartSapmaListesi.append(SSapma)
                SSapmaListesi.append(sensorVeStandartSapmaListesi)
            except StatisticsError:
                print("error")
                pass




        ### (SensorNo, StandartSapmaDegeri) seklindeki listeyi dosyaya binary olarak kaydettik
        with open(standartSapmaAdres, 'wb') as fp:
            pickle.dump(SSapmaListesi, fp)

        with open(standartSapmaAdres, "rb") as fp:
            SSliste = pickle.load(fp)

        print("SSliste: ", SSliste)

        end = time.time()
        print("SQLeBaglanKarma.herSensorunStandartSapmasi() fonksiyonundan cikti, ", round(end-start,4))
        
        
yil = 2017
ay = 1
ayinKaci = 12
vSegDir = 1
stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"
butunVerilerAdres = stdeviAdres+"{}-{}-{}-ButunVeriler.csv".format(yil, ay, ayinKaci)
sadeceSensorlerAdres = stdeviAdres+"{}-{}-{}-SadeceSensorNo.csv".format(yil, ay, ayinKaci)
herSensorunStandartSapmasi(yil, ay, ayinKaci, vSegDir,butunVerilerAdres, sadeceSensorlerAdres)