# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 13:23:37 2018

@author: IBRAHIM
"""
from geopy.geocoders import Nominatim
import geopy.distance
from math import sin, cos, sqrt, atan2, radians
import pyodbc
import matplotlib
matplotlib.use('Agg')
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
from geopy.exc import GeocoderTimedOut
import copy
import random
import os
from datetime import datetime, timedelta

class SQLeBaglanKarma():
    print("hela////////////////////////////////////")
    derece = 11
    derece7 = 7
    vSegID = 471
    vSegDir = 0
    ay = 'Mayis'
    suzsunMu = False
    yil = 2017
    dakikaAraligiList = [0, 15, 30, 45]
    ayinKaciList = [19]

    def __init__(self, yil, ay, ayinKaci, vSegID, vSegDir):
        self.vSegID = vSegID
        self.vSegDir = vSegDir
        self.ay = ay
        self.yil = yil
        self.ayinKaci = ayinKaci

    def __init__(self, yil, ay, ayinKaci):
        self.yil = yil
        self.ay = ay
        self.ayinKaci = ayinKaci



    def setVSegID(self, vSegID):
        self.vSegID = vSegID

    def setVSegDir(self, vSegDir):
        self.vSegDir = vSegDir

    def setAy(self, ay):
        self.ay = ay

    def setYil(self, yil):
        self.yil = yil

    def getVSegID(self):
        return self.vSegID

    def getVSegDir(self):
        return self.vSegDir

    def getAy(self):
        return self.ay

    def getYil(self):
        return self.yil

    def duzenle(self, saat, hiz):
        ayri = ()
        ayri2 = ()
        # print("saat: ",saat)
        for i in hiz:
            j = hiz.index(i)
            i = i.strip("\n")
            i = float(i.replace(",", "."))
            hiz[j] = i
        for i in range(len(saat)):
            ayri = saat[i].split(':')
            mini = int(ayri[0])
            miniIndex = i
            for j in range(i + 1, len(saat)):
                ayri2 = saat[j].split(':')
                if (int(ayri2[0]) < mini):
                    miniIndex = j
                    mini = int(ayri2[0])
            saat[i], saat[miniIndex] = saat[miniIndex], saat[i]
            hiz[i], hiz[miniIndex] = hiz[miniIndex], hiz[i]
        for i in saat:
            ayri = i.split(":")
            if len(ayri[0]) == 1:
                j = saat.index(i)
                i = "0" + i
                saat[j] = i

    ### SQL'deki tablodan yil, ay ve gune gore veri filtreliyor.
    def butunSensorlerBirGun(self, yil, ay, gun, cursor, vSegDir):
        print("belli bir gun: ", yil, ay , gun , vSegDir)
        ay = ay.replace('0', '')
        gun = gun.replace('0', '')
        start = time.time()
        komut = (
            "SELECT * FROM [FusedData-2016-2017-2018].[dbo].[{}-{}-{}]"
            " WHERE datepart(dd, fusedDate)={}".format(yil, ay, vSegDir, gun)
            )
        print(komut)
        cursor.execute(komut)
        end = time.time()

        adres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-ButunVeriler.csv".format(yil, ay, gun, vSegDir)

        print("{yil}-{ay}-{gun}'de bir gunu cikarmak icin gereken sure: ", end-start)

        butunVeriler = []
        for satir in cursor:
            deger = []
            deger.append(satir[0])
            deger.append( int(satir[1]) )
            deger.append( str(satir[2]) )
            deger.append(satir[3])
            #deger.append(satir[4])
            #deger.append(satir[5])
            butunVeriler.append(deger)
        #print(butunVeriler)

        with open(adres, "wb") as fp:
            pickle.dump(butunVeriler, fp)
        end = time.time()
        print("SQLeBaglanKarma.butunSensorlerBirGun() fonksiyonundan ciktik: ", round(end-start,4))

    def distinctSensorIDsWithSQL(self, cursor, yil, ay, vSegDir):
        distinctIDs = []
        ay = ay.replace('0', '')
        komut=(
            "SELECT distinct(vSegID) FROM [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] "
            "ORDER BY vSegID".format(yil,ay, vSegDir)
        )
        cursor.execute(komut)
        for distinctID in cursor:
            distinctIDveEnYakinHavaDurumuSensorID = [distinctID]
            distinctIDs.append(distinctIDveEnYakinHavaDurumuSensorID)
        return distinctIDs

    ### her seferinde dosyayi acip okumasi uzun suruyor, optimizasyon yapilabilir
    def XLSXdenSicaklikDondurFunc(self, xlsxDosyaAdresi, Istasyon_No, yil, ay, gun, saat):
        ay = ay.replace('0', '')
        gun = gun.replace('0', '')
        df = pd.read_excel(xlsxDosyaAdresi)
        #kolonList = list(df.columns.values)
        #arananKolonIndex = kolonList.index(kolonAdi)
        xlsxSatirListesi = []
        for row in df.iterrows():
            index, data = row
            if ( data[0]==Istasyon_No and data[2]==yil and data[3]==gun and data[4]==saat ):
                return data[5] # sicaklik



    ### vSegIDinKMLFile'in icinde sirasiyla vSegID, y koordinati, x koordinati, onemsiz var.
    def enYakinHavaDurumuSensorunuBulFunc(self, vSegIDinKMLFile):
        HavaDurumuKoordinatlari = [[40.9831482, 28.8037434, 17060],
                                    [40.9811277, 29.0280335, 17813],
                                    [41.0579782, 28.9755398, 18401],
                                    [41.0272496, 29.102531, 18403],
                                    [41.0352432, 29.01271, 18404]]
        toplamFarkList = []
        for havaDurumuKoordinati in HavaDurumuKoordinatlari:
            x_Fark = ( havaDurumuKoordinati[0] - float(vSegIDinKMLFile[2]) )**2
            y_Fark = ( havaDurumuKoordinati[1] - float(vSegIDinKMLFile[1]) )**2
            toplamFark = x_Fark+y_Fark
            toplamFarkList.append(toplamFark)

        minIndex = toplamFarkList.index( min(toplamFarkList) )
        return HavaDurumuKoordinatlari[minIndex][2]


    def tabloyaHavaDurumuVerileriniEkle(self, cursor, yil, ay, vSegDir):
        #ay = ay.replace('0', '')
        sensorID_ve_EnYakinHavaDurumuSensorNo_Adres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\sensorID_ve_EnYakinHavaDurumuSensorNo"
        with open(sensorID_ve_EnYakinHavaDurumuSensorNo_Adres, "rb") as fp:
            sensorID_ve_EnYakinHavaDurumuSensorNoList = pickle.load(fp)
        komut = (
            "SELECT * FROM [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] ".format(yil,ay, vSegDir)
        )
        cursor.execute(komut)
        for dortBilgi in cursor:
            for ID_ve_HavaDurumu in sensorID_ve_EnYakinHavaDurumuSensorNoList:
                if ( int(dortBilgi[0])==int(ID_ve_HavaDurumu[0]) ):
                    indexi = sensorID_ve_EnYakinHavaDurumuSensorNoList.index(ID_ve_HavaDurumu)
                    ### indexi : [vSegID, enYakinHavaDurumuSensorID]'nin kacinci indexte oldugunu tutar

    ### KML dosyasindan vSegID, yKoor, xKoor, ? dondurur.
    def KMLCoordinateListFunc(self):
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
            innerList = []
            innerList.append(IDList[i]) # name(sensorNo)
            ayriKoordinatList = str(coordinateList[i]).split(",")
            innerList.append(ayriKoordinatList[0]) # y koordinati
            innerList.append(ayriKoordinatList[1]) # x koordinati
            innerList.append(ayriKoordinatList[2]) # onemsiz
            allOfList.append(innerList)

        return allOfList

    ### KML dosyasindan vSegID, yKoor, xKoor, ? yi dosyaya yazar.
    def KML2Koor(self):
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
            innerList = []
            innerList.append(IDList[i])  # name(sensorNo)
            ayriKoordinatList = str(coordinateList[i]).split(",")
            innerList.append(ayriKoordinatList[0])  # y koordinati
            innerList.append(ayriKoordinatList[1])  # x koordinati
            innerList.append(ayriKoordinatList[2])  # onemsiz
            allOfList.append(innerList)

        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\vSegIDlerVeKoordinatlar.csv', 'wb') as fp:
            pickle.dump(allOfList, fp)

    ### KML dosyasindan vSegID, yKoor, xKoor, ? yi dosyaya yazar.
    def KML2KoorCSV(self):
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
            innerList = []
            innerList.append(IDList[i])  # name(sensorNo)
            ayriKoordinatList = str(coordinateList[i]).split(",")
            innerList.append(ayriKoordinatList[0])  # y koordinati
            innerList.append(ayriKoordinatList[1])  # x koordinati
            innerList.append(ayriKoordinatList[2])  # onemsiz
            allOfList.append(innerList)

        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\vSegIDlerVeKoordinatlar.pickle', 'wb') as fp:
            pickle.dump(allOfList, fp)

    ### [xKoor, yKoor]
    ### verilen vSegID'nin koordinatlarini dondurur
    def vSegIDVerKoordinatAl(self, vSegIDlerVeKoordinatlar, vSegID):

        for vSegIDveKoor in vSegIDlerVeKoordinatlar:
            if vSegID==vSegIDveKoor[0]:
                #print(vSegID, vSegIDveKoor[0], vSegIDveKoor[1], vSegIDveKoor[2])
                return [vSegIDveKoor[2], vSegIDveKoor[1]]



    def tabloyaSicaklikBilgisiEkle(self, cursor, cnxn):
        xlsxDosyaAdresi = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\Meteoroloji_Verisi\\olduSanirim.xlsx'
        df = pd.read_excel(xlsxDosyaAdresi)
        #kolonList = list(df.columns.values)
        #arananKolonIndex = kolonList.index(kolonAdi)
        #xlsxSatirListesi = []
        for row in df.iterrows():
            index, data = row
            Istasyon_No, YIL, AY, GUN, SAAT, SICAKLIK = data[0], data[2], data[3], data[4], data[5], data[6]
            #print(Istasyon_No ,YIL, AY, GUN, SAAT)
            if ( AY==1 and Istasyon_No!=17060 ):
                komut = (
                    'UPDATE [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] '
                    'SET sicaklik={} '
                    'WHERE havaDurumuSensorNo={} AND '
                    'datepart(yy, fusedDate)={} AND '
                    'datepart(mm, fusedDate)={} AND '
                    'datepart(dd, fusedDate)={} AND '
                    'datepart(hh, fusedDate)={}'.format(YIL, AY, 1, SICAKLIK, Istasyon_No, YIL, AY, GUN, SAAT)
                )
                #cursor.execute(komut)
                #cnxn.commit()
            elif ( AY==2 ):
                for j in range(2):
                    komut = (
                        'UPDATE [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] '
                        'SET sicaklik={} '
                        'WHERE havaDurumuSensorNo={} AND '
                        'datepart(yy, fusedDate)={} AND '
                        'datepart(mm, fusedDate)={} AND '
                        'datepart(dd, fusedDate)={} AND '
                        'datepart(hh, fusedDate)={}'.format(YIL, AY, j, SICAKLIK, Istasyon_No, YIL, AY, GUN, SAAT)
                    )
                    #cursor.execute(komut)
                    #cnxn.commit()

            elif (AY==3):
                komut = (
                    'UPDATE [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] '
                    'SET sicaklik={} '
                    'WHERE havaDurumuSensorNo={} AND '
                    'datepart(yy, fusedDate)={} AND '
                    'datepart(mm, fusedDate)={} AND '
                    'datepart(dd, fusedDate)={} AND '
                    'datepart(hh, fusedDate)={}'.format(YIL, AY, 0, SICAKLIK, Istasyon_No, YIL, AY, GUN, SAAT)
                )
                cursor.execute(komut)
                cnxn.commit()

    ### adres bilgileri dosyada bulunan sensorlerin yakin hava durumu sensorunun bulunmasi ve
    ### dosyaya kaydedilmesi islemi. Böylece kod her calistiginda bu islem yeniden yapilmak zorunda olmayacak.
    def butunAdres2HavaDurumu(self):
        acikAdresDosyasi = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\butunAdresler.txt'
        with open(acikAdresDosyasi, 'rb') as fp:
            butunAdresler = pickle.load(fp)
        #for adres in butunAdresler:
        #    print(adres)
        HavaDurumuKoordinatlari = [[40.9831482, 28.8037434, 17060],
                                   [40.9811277, 29.0280335, 17813],
                                   [41.0579782, 28.9755398, 18401],
                                   [41.0272496, 29.102531, 18403],
                                   [41.0352432, 29.01271, 18404]]

        enYakinHDSAList = []
        for adres in butunAdresler:
            toplamFarkList = []
            for havaDurumuKoordinati in HavaDurumuKoordinatlari:
                x_Fark = (havaDurumuKoordinati[0] - float(adres[2])) ** 2
                y_Fark = (havaDurumuKoordinati[1] - float(adres[1])) ** 2
                toplamFark = x_Fark + y_Fark
                toplamFarkList.append(toplamFark)

            print("toplamFark: ", toplamFarkList)
            minIndex = toplamFarkList.index(min(toplamFarkList))
            enYakinHDSN = HavaDurumuKoordinatlari[minIndex][2]
            if (enYakinHDSN == 17060):
                enYakinHDSA = "Havalimanı"
            elif (enYakinHDSN == 17813):
                enYakinHDSA = "Kadıköy"
            elif (enYakinHDSN == 18401):
                enYakinHDSA = 'Şişli'
            elif (enYakinHDSN == 18403):
                enYakinHDSA = 'Ümraniye'
            elif (enYakinHDSN == 18404):
                enYakinHDSA = 'Üsküdar'

            enYakinHDSAList.append(enYakinHDSA)

        havaDurumuAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\havaDurumuAdres.txt'
        with open(havaDurumuAdres, 'wb') as fp:
            pickle.dump(enYakinHDSAList, fp)








    ### KML dosyasindaki her bir sensorun en yakin oldugu hava durumu sensorunu listeye kaydedip binary olarak dosyaya kaydet.
    def sensorVeEnYakinHavaDurumuSensorunuBulVeKaydet(self, cursor, cnxn, belliBirGun, yil, ay, vSegDir):
        """cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                              "SERVER=IBRAHIM;"
                              "Database=FusedData-2016-2017-2018;"
                              "Trusted_Connection=yes;")
        cursor = cnxn.cursor()"""
        KMLCoordinateList = self.KMLCoordinateListFunc()
        yil = int(yil)
        ay = int(ay)
        vSegDir = int(vSegDir)
        print("--", yil, ay, vSegDir)
        ### allOfvSegID_ve_EnYakinHavaDurumuSensoruList = [[vSegID, y, x, onemsiz, havaDurumuSensorNo], [vSegID, y, x, onemsiz, havaDurumuSensorNo]]
        allOfvSegID_ve_EnYakinHavaDurumuSensoruList = []
        ### vSegIDinKMLFile: [vSegID, y, x, onemsiz, havaDurumuSensorNo]
        for vSegIDinKMLFile in KMLCoordinateList:
            enYakinHavaDurumuSensoru = belliBirGun.enYakinHavaDurumuSensorunuBulFunc(vSegIDinKMLFile)
            vSegIDinKMLFile.append(enYakinHavaDurumuSensoru)
            #print(vSegIDinKMLFile)
            allOfvSegID_ve_EnYakinHavaDurumuSensoruList.append(vSegIDinKMLFile)
        print(len(allOfvSegID_ve_EnYakinHavaDurumuSensoruList))
        for ay in range(1, 3):
            for vSegDir in range(0,2):
                for vSegID_ve_EnYakinHavaDurumuSensoru in allOfvSegID_ve_EnYakinHavaDurumuSensoruList:
                    #print(vSegID_ve_EnYakinHavaDurumuSensoru[4], vSegID_ve_EnYakinHavaDurumuSensoru[0])
                    komut=(
                        'UPDATE [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] '
                        'SET havaDurumuSensorNo={} where vSegID={}'.format(yil, ay, vSegDir, vSegID_ve_EnYakinHavaDurumuSensoru[4], vSegID_ve_EnYakinHavaDurumuSensoru[0])
                    )
                    #print(komut)
                    cursor.execute(komut)
                    cnxn.commit()
            #print(yil, ay, vSegDir)


    ### 13 tane dosyada ayri ayri olan adres bilgilerini tek bir dosyada birleştirme islemi yapilir.
    ### Adres bilgilerinin 13 farkli dosyada tutulmasinin sebebi de adres bilgi cikarma isleminde
    ### kotaya takilmaktir.
    def adresBilgileriniKaydet(self):
        ### 13 farkli adresin toplanacagi liste
        birlesmisAdresler = []
        for i in range(13):
            adres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\adresler{}.txt'.format(i)
            with open(adres, 'rb') as fp:
                ### her bir dosyadaki adres listesi
                altAdres = pickle.load(fp)
                for adres in altAdres:
                    birlesmisAdresler.append(adres)
        ### birlesecek adres
        adres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\butunAdresler.txt'
        with open(adres, 'wb') as fp:
            pickle.dump(birlesmisAdresler, fp)

        print(birlesmisAdresler)


    def do_geocode(self, geolocator, x, y):
        try:
            location = geolocator.reverse("{}, {}".format(str(x), str(y)))
            adres = location.address
            return adres
        except GeocoderTimedOut:
            return self.do_geocode(geolocator, x, y)

    def adresCikar(self):
        koordinatList = self.KMLCoordinateListFunc()
        timeOutList = []
        #print("koordinatlar: ",koordinatList)
        for koordinat in koordinatList:
            vSegID = koordinat[0]
            x = koordinat[2]
            y = koordinat[1]

            geolocator = Nominatim(user_agent="traffSite")
            adres = self.do_geocode(geolocator, x, y)
            koordinat.append(adres)
            print(koordinatList.index(koordinat), len(koordinatList))
        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\stdevi\\adresler.txt', 'wb') as fp:
            pickle.dump(koordinatList, fp)

        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\stdevi\\timeOutAdresler.txt', 'wb') as fp:
            pickle.dump(timeOutList, fp)



    def semttekiSiraliSensorleriBul(self, yil, ay, ayinKaci):
        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\butunAdresler.txt', 'rb') as fp:
            acikAdresList = pickle.load(fp)
        semtVeSensorList = []
        for adres in acikAdresList:
            acikAdresString = adres[4]
            acikAdresList = acikAdresString.split(', ')
            try:
                indx = acikAdresList.index('İstanbul')
            except ValueError:
                try:
                    indx = acikAdresList.index('Kocaeli')
                except ValueError:
                    try:
                        indx = acikAdresList.index('Tekirdağ')
                    except ValueError:
                        indx = acikAdresList.index('Yalova')
            vSegIDveSemt = [acikAdresList[indx - 1], adres[0]]  # [semt, adres]
            semtVeSensorList.append(vSegIDveSemt)

        ### [ [semt1, ID1, ID2], []  ]
        semtler = []

        for semtVeSensor in semtVeSensorList:
            if [semtVeSensor[0]] not in semtler:
                semtler.append([semtVeSensor[0]])

        semtVeSensorlerList = copy.deepcopy(semtler)

        for semtVeSensor in semtVeSensorList:
            indx = semtler.index([semtVeSensor[0]])
            semtVeSensorlerList[indx].append(
                semtVeSensor[1])  # [ [semt1, vSegID1, vSegID2, ...], [semt2, vSegID111, vSegID112, ...], ... ]

        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\semtVeSensorler.txt', 'wb') as fp:
            pickle.dump(semtVeSensorlerList, fp)



        semtlerVeSiraliListeler = []
        for semtVeSensorler in semtVeSensorlerList:
            #semt = semtVeSensorler[0]
            semtIndex = semtVeSensorlerList.index(semtVeSensorler)
            enUzunSiraliListeler = self.siraliListeBul(semtVeSensorlerList, semtIndex)
            semtlerVeSiraliListeler.append(enUzunSiraliListeler)

        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\semtlerVeSiraliListeler.txt', 'wb') as fp:
            pickle.dump(semtlerVeSiraliListeler, fp)

        ### enUzunSiraliListeler = self.siraliListeBul(semtVeSensorlerList,
        ###                                      semtIndex)  # [ semt, [1,2,3], [10,11], [323,324,325], ... ]

        for i in semtlerVeSiraliListeler:
            print(i)


    def vSegIDVerHizAl(self, vSegID, vSegIDlerVeHizlar):

        for vSegIDVeHiz in vSegIDlerVeHizlar:
            if vSegID==vSegIDVeHiz[0]:
                #print("vSegIDVeHiz-> ",vSegIDVeHiz[1])
                return vSegIDVeHiz[1]
        ### :aSD:Asd:ASD
        #return random.randint(0, 60)


    def SiraliKoorVeHizDondur(self, yil,ay,gun,vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika):

        renkliYolAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\'
        ### siraliListe = [[1,2,3], [6,7,8,9]]
        siraliListe = self.siraliListeBul(yil,ay,gun,vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
        #print("++++++++++++++++++++++++: ",siraliListe)

        if 'vSegIDlerVeKoordinatlar.pickle' not in os.listdir('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\'):
            self.KML2KoorCSV()

        ### semtVeSiraliListeler = [ Üsküdar, [1,2,3,4], [7,8,9], ...]
        ### SemtlerVeSiraliListeler = [semtVeSiraliListeler, semtVeSiraliListeler,semtVeSiraliListeler]
        # with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\semtlerVeSiraliListeler.txt', 'rb') as fp:
        #     semtlerVeSiraliListeler = pickle.load(fp)

        #print("----------", semtlerVeSiraliListeler)

        ### [ [1, 23], [2, 43], ... ]
        #with open(
        #        'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-{}-sensorlerVeHizOrt.csv'.format(yil, ay,
        #                                                                                                       gun,
        #                                                                                                       vSegDir, semt),
        #        'rb') as fp:
        #    vSegIDVeHiz = pickle.load(fp)
        #
        #if siraliSensorlerAdres not in os.listdir(stdeviAdres):
        #    ### siraliSensorler = [ [1,2,3] , [6,7,8,9,10], ...]
        #    siraliSensorler = []
        #    for semtVeSiraliListeler in semtlerVeSiraliListeler:
        #        if semtVeSiraliListeler[0]==semt:
        #            ### siraliListeler = [1,2,3] veya [56,57,58] veya ...
        #            for siraliListeler in semtVeSiraliListeler[1:]:
        #                siraliSensorler.append(siraliListeler)
        #    with open(stdeviAdres+siraliSensorlerAdres, 'wb') as fp:
        #        pickle.dump(siraliSensorler, fp)
        #
        #with open(stdeviAdres+siraliSensorlerAdres, 'rb') as fp:
        #    siraliSensorler = pickle.load(fp)

        siraliSensorler = siraliListe
        vSegIDveOrtHizAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\{}-{}-{}-{}-{}.{}-{}.{}-vSegIDveOrtHiz.pickle'.format(
                    yil, ay, gun, vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
        with open(vSegIDveOrtHizAdres, 'rb') as fp:
            vSegIDlerVeHizlar = pickle.load(fp)

        #print(vSegIDlerVeHizlar)

        koorVeHizAdres = '{}-{}-{}-{}-{}.{}-{}.{}-koorVeHiz.pickle'.format(yil, ay, gun, vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)

        ### [ [x1, y1, hiz1, x2, y2, hiz2], [x5, y5, hiz5, x6, y6, hiz6, x7, y7, hiz7 ] ]
        koorVeHiz = []
        hizliKoorList = []

        start = time.time()
        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\vSegIDlerVeKoordinatlar.pickle', 'rb') as fp:
            vSegIDlerVeKoordinatlar = pickle.load(fp)
        if koorVeHizAdres not in os.listdir(renkliYolAdres):
            ### siraliSensorler = [[1,2,3], [5,6,7]]
            for siraliSensor in siraliSensorler:
                koorVeHiz.append([])
                #print("---> ",siraliSensor)
                for sensor in siraliSensor:
                    ### hizliKoorList = [x1, y1, hiz1]
                    try:
                        hizliKoorList = self.vSegIDVerKoordinatAl(vSegIDlerVeKoordinatlar, sensor)
                        #print(hizliKoorList)
                        hiz = self.vSegIDVerHizAl(sensor, vSegIDlerVeHizlar)
                        hizliKoorList.append(hiz)

                        for koorVeyaHiz in hizliKoorList:
                            koorVeHiz[-1].append(koorVeyaHiz)
                    except AttributeError :
                        pass
            with open(renkliYolAdres+koorVeHizAdres, 'wb') as fp:
                pickle.dump(koorVeHiz, fp)
        with open(renkliYolAdres+koorVeHizAdres, 'rb') as fp:
            koorVeHiz = pickle.load(fp)

        end = time.time()
        #print('KoorVeHiz: ', end-start)

        return koorVeHiz


    ### [ [1,2,3], [6,7,8,9]]
    def siraliListeBul(self, yil,ay,gun,vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika):
        ### vSegIDveHizOrt = [[vSegID1, OrtHiz1], [vSegID2, OrtHiz2], ...]
        vSegIDveOrtHizAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\{}-{}-{}-{}-{}.{}-{}.{}-vSegIDveOrtHiz.pickle'.format(
                    yil, ay, gun, vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)

        with open(vSegIDveOrtHizAdres, 'rb') as fp:
            vSegIDveOrtHiz = pickle.load(fp)

        #print("----------: ",vSegIDveOrtHiz)

        siralivSegIDler = []
        for i in vSegIDveOrtHiz:
            siralivSegIDler.append(i[0])
        ilkSensor = siralivSegIDler[0]
        innerList = [ilkSensor]
        a = 1

        siraliListeler = []
        for i in range(1, len(siralivSegIDler)):
            if siralivSegIDler[i] - ilkSensor == a:
                a += 1
                innerList.append(siralivSegIDler[i])
            else:
                a = 1
                siraliListeler.append(innerList)
                ilkSensor = siralivSegIDler[i]
                innerList = [ilkSensor]
        return siraliListeler




        ### !!!!!!!!!!!!!!!!!!!!!!!! Duzgun calisirsa Sil !!!!!!!!!!!!!!!!!!!!!!!!
        # semtVeSensorler = semtVeSensorlerList[semtIndex]  # ['Altınova', 1812, 1813, 1814, 1815, 1816]
        # semtsiz = semtVeSensorler[1:]
        # semtsiz.sort()
        # semtVeSensorler[1:] = semtsiz
        # siraliListeler = [semtVeSensorler[0]]
        # ilkSensor = semtVeSensorler[1]
        # innerList = [ilkSensor]
        # a = 1
        # for i in range(2, len(semtVeSensorler)):
        #     if semtVeSensorler[i] - ilkSensor == a:
        #         a += 1
        #         innerList.append(semtVeSensorler[i])
        #     else:
        #         a = 1
        #         siraliListeler.append(innerList)
        #         ilkSensor = semtVeSensorler[i]
        #         innerList = [ilkSensor]
        # return siraliListeler

    ### Belirlenen tarihteki butun sensorlerin ortalama hiz degerlerini bulur.
    ### [ [1, 30], [2, 31], ... ]
    def sensorlerinOrtHizBul(self, yil, ay, gun, vSegDir, semt):
        #print('sensorlerinOrtHizBul')
        secilenTarih = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-ButunVeriler.csv'.format(yil, ay, gun, vSegDir)
        with open(secilenTarih, 'rb') as fp:
            butunVeriler = pickle.load(fp)  # [ [7, 0, '2017-01-15 03:32:00', 35],[7, 0, '2017-01-15 03:33:00', 35] ]
        butunVeriler.sort()
        sensordekiHizDegerleri = []

        idler = []
        for satir in butunVeriler:
            idler.append(int(satir[0]))
        idler.sort()
        distinctIDs = list(set(idler))
        distinctIDs.sort()

        sensorlerVeHizlar = []
        for distID in distinctIDs:
            sensorlerVeHizlar.append([distID])

        for satir in butunVeriler:
            indx = distinctIDs.index(satir[0])
            sensorlerVeHizlar[indx].append(satir[3])

        ortalamaList = []  # [ [1, 34], [2, 33], ... ] -> [ [sensorNo1, ortHiz1],[sensorNo2, ortHiz2], ... ]
        for sensorVeHizlar in sensorlerVeHizlar:
            ortHiz = self.Average(sensorVeHizlar[1:])
            ortalamaList.append([sensorVeHizlar[0], ortHiz])

        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-{}-sensorlerVeHizOrt.csv'.format(yil, ay, gun, vSegDir, semt), 'wb') as fp:
            pickle.dump(ortalamaList, fp)


    def Average(self, lst):
        return sum(lst) / len(lst)


    def secilenSemttekiSensorlerinOrtHizlari(self, semt, yil, ay, gun, vSegDir):
        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\semtlerVeSiraliListeler.txt', 'rb') as fp:
            semtlerVeSiraliSensorler = pickle.load(fp) # [ [semt, [1,2,3], [10,11]], ... ]

        semtVeSiraliSensorler = []
        for i in semtlerVeSiraliSensorler:
            if i[0] == semt:
                semtVeSiraliSensorler = i  # [semt, [1,2,3], [10,11]]

        secilenSemttekiSensorlerVeOrtHizlari = [semt]
        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-{}-sensorlerVeHizOrt.csv'.format(yil, ay, gun, vSegDir, semt), 'rb') as fp:
            sensorlerVeHizOrt = pickle.load(fp)


        for siraliSensor in semtVeSiraliSensorler[1:]:
            for sensor in siraliSensor:
                for sensorVeHizOrt in sensorlerVeHizOrt:
                    if sensorVeHizOrt[0] == sensor:
                        secilenSemttekiSensorlerVeOrtHizlari.append( [sensor, sensorVeHizOrt[1]] )

        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-{}-secilenSemtVeSensorlerinHizOrt.csv'.format(yil, ay, gun, vSegDir, semt), 'wb') as fp:
            pickle.dump(secilenSemttekiSensorlerVeOrtHizlari, fp)

        #return secilenSemttekiSensorlerVeOrtHizlari
        ### [ 'Üsküdar', [1, 30], [2, 45], ... ]

    def secilenSemttekiSensorlerinOrtHizlariVeKoordinatlari(self, semt, yil, ay, gun, vSegDir):
        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\vSegIDlerVeKoordinatlar.csv', 'rb') as fp:
            vSegIDlerVeKoorlar = pickle.load(fp)

        ### [semt, [vSegID1, ort1], [vSegID2, ort2], ... ]
        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-{}-secilenSemtVeSensorlerinHizOrt.csv'.format(yil, ay, gun, vSegDir, semt), 'rb') as fp:
            secilenSemtVeSensorlerinHizOrt = pickle.load(fp)

        for sensorVeHizOrt in secilenSemtVeSensorlerinHizOrt[1:]:
            for vSegIDVeKoor in vSegIDlerVeKoorlar:
                if sensorVeHizOrt[0]==vSegIDVeKoor[0]:
                    indx = secilenSemtVeSensorlerinHizOrt.index(sensorVeHizOrt)
                    sensorVeHizOrt.append(vSegIDVeKoor[1])  # y koor
                    sensorVeHizOrt.append(vSegIDVeKoor[2])  # x koor
                    secilenSemtVeSensorlerinHizOrt[indx] = sensorVeHizOrt

        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-{}-secilenSemttekiSensorlerinOrtHizlariVeKoordinatlari.csv'.format(yil, ay, gun, vSegDir, semt), 'wb') as fp:
            pickle.dump(secilenSemtVeSensorlerinHizOrt, fp)

    def hizaGoreRenklendir(self, semt, yil, ay, gun, vSegDir, hizLimiti):
        ### [semt, [vSegID1, ort1, y1, x1], [vSegID2, ort2, y2, x2], ... ]
        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-{}-secilenSemttekiSensorlerinOrtHizlariVeKoordinatlari.csv'.format(yil, ay, gun, vSegDir, semt), 'rb') as fp:
            secilenSemtVeSensorlerinHizOrtVeKoor = pickle.load(fp)

        for sensorOrtHizVeKoor in secilenSemtVeSensorlerinHizOrtVeKoor[1:]:
            indx = secilenSemtVeSensorlerinHizOrtVeKoor.index(sensorOrtHizVeKoor)
            if sensorOrtHizVeKoor[1]<hizLimiti:
                sensorOrtHizVeKoor.append('#8b0013')
            else:
                sensorOrtHizVeKoor.append('#208B23')
            secilenSemtVeSensorlerinHizOrtVeKoor[indx] = sensorOrtHizVeKoor

        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-{}-secilenSemttekiSensorlerinOrtHizlariKoordinatlariVeRenkKodlari.csv'.format(yil, ay, gun, vSegDir, semt), 'wb') as fp:
            pickle.dump(secilenSemtVeSensorlerinHizOrtVeKoor, fp)


    ## ==========================================================================================================================

    ### en son
    def renkliHaritaSaatlikVeDakikalikSQLSorgusu(self, cursor, yil, ay, gun, vSegDir, basSaat, bitSaat):
        start= time.time()
        renkliYolAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\'
        CSVAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\'
        basSaatList = basSaat.split(':')
        bitSaatList = bitSaat.split(':')
        basSaatSaat = basSaatList[0]
        basSaatDakika = basSaatList[1]
        bitSaatSaat = bitSaatList[0]
        bitSaatDakika = bitSaatList[1]
        #print(yil, ay, gun, vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)

        ### [ [vSegID1, OrtHiz1], [vSegID2, OrtHiz2], ...]
        dosyaAdi = '{}-{}-{}-{}-{}.{}-{}.{}-vSegIDveOrtHiz.pickle'.format(yil,ay,gun,vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)

        if 'renkliYol' not in os.listdir(CSVAdres):
            os.mkdir(renkliYolAdres)

        
        vSegIDveOrtHiz = []
        if dosyaAdi not in os.listdir(renkliYolAdres):
            komut=(
                "select vSegID, avg(fusedSpeed) as ortHiz FROM [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] "
                "where datepart(dd, fusedDate)={} and DATEPART(HOUR, fusedDate)*60+DATEPART(mi, fusedDate) between {}*60+{} and {}*60+{} "
                "GROUP BY vSegID ORDER BY vSegID".format(yil, ay, vSegDir, gun, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
            )
            cursor.execute(komut)
            for i in cursor:
                #print("iiiiiiiiiiiiiii: ",i)
                innervSegIDveOrtHiz = []
                innervSegIDveOrtHiz.append(i[0])
                innervSegIDveOrtHiz.append(i[1])
                vSegIDveOrtHiz.append(innervSegIDveOrtHiz)

            with open(renkliYolAdres+dosyaAdi, 'wb') as fp:
                pickle.dump(vSegIDveOrtHiz, fp)

        stop= time.time()
        print("zaman: ", stop-start)


        # self.siraliListeBul(yil,ay,gun,vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)


    def uzakSensorleriParcala(self, siraliKoorVeHiz):
        newSiraliKoorVeHiz = []
        R = 6373.0
        print("2")
        for siraliListe in siraliKoorVeHiz:
            ardisik = 1
            #print(siraliListe)
            newSiraliListe = []
            sinirlar = [0]
            for i in range(0, len(siraliListe)-5, 3):
                coord1 = (float(siraliListe[i]), float(siraliListe[i+1]))
                coord2 = (float(siraliListe[i+3]), float(siraliListe[i+4]))
                distance = geopy.distance.vincenty(coord1, coord2).m
                
                if (distance>10000):
                    ardisik = 0
                    sinirlar.append(i+3)
            sinirlar.append(len(siraliListe))
            newSiraliKoorVeHiz.append(siraliListe)
            #if len(sinirlar) == 2:
            #    newSiraliKoorVeHiz.append(siraliListe)
            #else:
            #    for j in range(len(sinirlar)-1):
            #        sinirlarIndexIlk = sinirlar[j]
            #        sinirlarIndexSon = sinirlar[j+1]
            #        print(siraliListe[sinirlarIndexIlk:sinirlarIndexSon])
            #        #if (sinirlarIndexSon- sinirlarIndexIlk > 9):
            #        newSiraliKoorVeHiz.append(siraliListe[sinirlarIndexIlk:sinirlarIndexSon])
            #    #newSiraliKoorVeHiz.append(newSiraliListe)
        for siraliListe in newSiraliKoorVeHiz:
            for i in range(0, len(siraliListe)-5, 3):
                coord1 = (float(siraliListe[i]), float(siraliListe[i+1]))
                coord2 = (float(siraliListe[i+3]), float(siraliListe[i+4]))
                distance = geopy.distance.vincenty(coord1, coord2).m
                if (distance>10000):
                    print(distance)


        return newSiraliKoorVeHiz

        

        

    ## =====================================================================================================================

    
    ###  === Tahmin ===
    ## =====================================================================================================================

    def stringSQLSorgusuTahmin(self, request, cursor, tarih, k, vSegDir):
        renkliYolAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\'
        sorgu = ''
        ilkSorgu = "SELECT vSegID, AVG(cast(fusedSpeed AS money)) as ortHiz FROM ( "
        sorgu += ilkSorgu
        saatTahmin = request.POST.get('datetimepicker9')
        tahminList = saatTahmin.split(':')
        saatTahmin = tahminList[0]
        dakikaTahmin = tahminList[1]
        tarihParcalanmisListe = tarih.split('/')
        yil = int(tarihParcalanmisListe[2])
        ay = int(tarihParcalanmisListe[1].replace('0', ''))
        gun = int(tarihParcalanmisListe[0].replace('0', ''))
        oGun = datetime(yil, ay, gun)
        dosyaAdi = '{}-{}-{}-{}-{}.{}-{} hafta-vSegIDveOrtHiz.pickle'.format(yil,ay,gun,vSegDir, saatTahmin, dakikaTahmin, k)
        tarihList = []
        vSegIDveOrtHiz = []
        for i in range(1, k+1):
            oncekiHafta = oGun - timedelta(days=7*i)
            tarihList.append(oncekiHafta)
        for i in range(k-1):
            tarih = tarihList[i]
            gun = int(tarih.strftime('%d'))
            ay = int(tarih.strftime('%m'))
            yil = int(tarih.strftime('%Y'))
            innerSorgu = (
                ' SELECT vSegID, vSegDir, fusedDate, fusedSpeed FROM [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] '
                ' WHERE datepart(DAY, fusedDate)={} AND '
                ' datepart(MINUTE, fusedDate) in (0,15,30,45) '
                ' UNION '
                ' '.format(yil, ay, vSegDir, gun)
            )
            sorgu += innerSorgu
        tarih = tarihList[k-1]
        gun = int(tarih.strftime('%d'))
        ay = int(tarih.strftime('%m'))
        yil = int(tarih.strftime('%Y'))
        innerSorgu = (
            ' SELECT vSegID, vSegDir, fusedDate, fusedSpeed FROM [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] '
            ' WHERE datepart(DAY, fusedDate)={} AND '
            ' datepart(MINUTE, fusedDate) in (0,15,30,45) '.format(yil, ay, vSegDir, gun)
        )
        sorgu += innerSorgu
        enSonSorgu = (' ) sub '
                        ' WHERE datepart(HOUR, fusedDate)={} and datepart(MINUTE, fusedDate)={} '
                        ' GROUP BY vSegID, datepart(HOUR, sub.fusedDate), datepart(MINUTE, sub.fusedDate) '
                        ' ORDER BY datepart(HOUR, fusedDate), datepart(MINUTE, fusedDate), vSegID'
        ).format(saatTahmin, dakikaTahmin)
        sorgu += enSonSorgu
        print(sorgu)
        start = time.time()

        cursor.execute(sorgu)
        for i in cursor:
            #print("iiiiiiiiiiiiiii: ",i)
            innervSegIDveOrtHiz = []
            innervSegIDveOrtHiz.append(i[0])
            innervSegIDveOrtHiz.append(i[1])
            vSegIDveOrtHiz.append(innervSegIDveOrtHiz)

        with open(renkliYolAdres+dosyaAdi, 'wb') as fp:
            pickle.dump(vSegIDveOrtHiz, fp)

        stop= time.time()
        print("zaman: ", stop-start)


    def SiraliKoorVeHizDondurTahmin(self, yil,ay,gun,vSegDir, saatTahmin, dakikaTahmin, k):

        renkliYolAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\'
        ### siraliListe = [[1,2,3], [6,7,8,9]]
        siraliListe = self.siraliListeBulTahmin(yil,ay,gun,vSegDir, saatTahmin, dakikaTahmin, k)
        #print("++++++++++++++++++++++++: ",siraliListe)

        if 'vSegIDlerVeKoordinatlar.pickle' not in os.listdir('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\'):
            self.KML2KoorCSV()

        siraliSensorler = siraliListe
        vSegIDveOrtHizAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\{}-{}-{}-{}-{}.{}-{} hafta-vSegIDveOrtHiz.pickle'.format(
                    yil, ay, gun, vSegDir, saatTahmin, dakikaTahmin, k)
        with open(vSegIDveOrtHizAdres, 'rb') as fp:
            vSegIDlerVeHizlar = pickle.load(fp)

        #print(vSegIDlerVeHizlar)

        koorVeHizAdres = '{}-{}-{}-{}-{}.{}-{} hafta-koorVeHiz.pickle'.format(yil, ay, gun, vSegDir, saatTahmin, dakikaTahmin, k)

        ### [ [x1, y1, hiz1, x2, y2, hiz2], [x5, y5, hiz5, x6, y6, hiz6, x7, y7, hiz7 ] ]
        koorVeHiz = []
        hizliKoorList = []

        start = time.time()
        with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\vSegIDlerVeKoordinatlar.pickle', 'rb') as fp:
            vSegIDlerVeKoordinatlar = pickle.load(fp)
        if koorVeHizAdres not in os.listdir(renkliYolAdres):
            ### siraliSensorler = [[1,2,3], [5,6,7]]
            for siraliSensor in siraliSensorler:
                koorVeHiz.append([])
                #print("---> ",siraliSensor)
                for sensor in siraliSensor:
                    ### hizliKoorList = [x1, y1, hiz1]
                    try:
                        hizliKoorList = self.vSegIDVerKoordinatAl(vSegIDlerVeKoordinatlar, sensor)
                        #print(hizliKoorList)
                        hiz = self.vSegIDVerHizAl(sensor, vSegIDlerVeHizlar)
                        hizliKoorList.append(hiz)

                        for koorVeyaHiz in hizliKoorList:
                            koorVeHiz[-1].append(koorVeyaHiz)
                    except AttributeError :
                        pass
            with open(renkliYolAdres+koorVeHizAdres, 'wb') as fp:
                pickle.dump(koorVeHiz, fp)
        with open(renkliYolAdres+koorVeHizAdres, 'rb') as fp:
            koorVeHiz = pickle.load(fp)

        end = time.time()
        #print('KoorVeHiz: ', end-start)

        return koorVeHiz

    def siraliListeBulTahmin(self, yil,ay,gun,vSegDir,saatTahmin, dakikaTahmin, k):
        ### vSegIDveHizOrt = [[vSegID1, OrtHiz1], [vSegID2, OrtHiz2], ...]
        vSegIDveOrtHizAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\{}-{}-{}-{}-{}.{}-{} hafta-vSegIDveOrtHiz.pickle'.format(
                    yil, ay, gun, vSegDir, saatTahmin, dakikaTahmin, k)

        with open(vSegIDveOrtHizAdres, 'rb') as fp:
            vSegIDveOrtHiz = pickle.load(fp)

        #print("----------: ",vSegIDveOrtHiz)

        siralivSegIDler = []
        for i in vSegIDveOrtHiz:
            siralivSegIDler.append(i[0])
        ilkSensor = siralivSegIDler[0]
        innerList = [ilkSensor]
        a = 1

        siraliListeler = []
        for i in range(1, len(siralivSegIDler)):
            if siralivSegIDler[i] - ilkSensor == a:
                a += 1
                innerList.append(siralivSegIDler[i])
            else:
                a = 1
                siraliListeler.append(innerList)
                ilkSensor = siralivSegIDler[i]
                innerList = [ilkSensor]
        return siraliListeler


    ## =====================================================================================================================


    ### SQL'deki distinct fonksiyonunu gerceklestiren fonk. yani her bir farkli sensor
    ### no'yu buluyor, bulduklarini listeye ekliyor ve bu listeyi binary olarak kaydediyor.
    def distinctSensorNo(self, butunVerilerAdres, sadeceSensorlerAdres):
        start = time.time()
        #print("distinctSensorNo() fonksiyonuna girdi")
        with open(butunVerilerAdres, "rb") as fp:
            #butunVeriler.seek(40)
            butunVeriler = pickle.load(fp)
            idler = []
            for satir in butunVeriler:
                idler.append( int(satir[0]) )

        idler.sort()
        distinctIDs = list(set(idler))

        with open(sadeceSensorlerAdres, 'wb') as fp:
            pickle.dump(distinctIDs, fp)

        end = time.time()
        #print("SQLeBaglanKarma.distinctSensorNo() fonksiyonundan cikti: ", round(end-start,4))

    ### Dosyada bulunan (sensorNo, standartSapmaDegeri) seklindeki listeyi, standartSapmaDegeri'ne gore siralayip
    ### dosyaya binary olarak kaydettik
    def dosyadanOkuyupSirala(self, standartSapmaAdres, siraliStandartSapmaAdres):
        #print("dosyadanOkuyupSirala() fonksiyonuna girdik")
        start = time.time()
        #standartSapma = open(standartSapmaAdres, "r", encoding='utf-8-sig')
        with open(standartSapmaAdres, 'rb') as fp:
            sensorVeStandartSapmaListesi = pickle.load(fp)
        butunSensorVeSapma = []

        for i in range(len(sensorVeStandartSapmaListesi)):
            maxi = float( sensorVeStandartSapmaListesi[i][1] )
            maxIndis = i
            for j in range(i+1, len(sensorVeStandartSapmaListesi)):
                if ( float(sensorVeStandartSapmaListesi[j][1]) > maxi ):
                    maxIndis = j
                    maxi = float( sensorVeStandartSapmaListesi[j][1] )

            (sensorVeStandartSapmaListesi[i]), (sensorVeStandartSapmaListesi[maxIndis]) = (sensorVeStandartSapmaListesi[maxIndis]), (sensorVeStandartSapmaListesi[i])

        ### (sensorNo,standartSapmaDegeri) seklindeki sirali listeyi dosyaya binary olarak kaydettik
        with open(siraliStandartSapmaAdres, 'wb') as fp:
            pickle.dump(sensorVeStandartSapmaListesi, fp)

        end = time.time()
        #print("SQLeBaglanKarma.dosyadanOkuyupSirala() fonksiyonundan ciktik: ", round(end-start,4) )

    def vSegIDSirala(self, butunVerilerAdres):
        with open(butunVerilerAdres, "rb") as fp:
            degerler = pickle.load(fp)

        degerler.sort()


        with open(butunVerilerAdres, "wb") as fp:
            pickle.dump(degerler, fp)

    def yiliAylaraAyirFonk(self, cursor, yil ,ay):
        for i in range(1, 2):
            for j in range(1):
                start = time.time()
                komut=(
                "SELECT * FROM [FusedData-2016-2017-2018].[dbo].[FusedData{}]" 
                "where vSegDir={} and datepart(mm,fusedDate)={} ".format(yil,j,i)
                )
                vSegDir = j
                cursor.execute(komut)
                adres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-AylikButunVeriler.csv".format(yil, ay, vSegDir)
                aylikButunVeriler = []
                for satir in cursor:
                    deger = []
                    deger.append(satir[0])
                    deger.append( int(satir[1]) )
                    deger.append( str(satir[2]) )
                    deger.append(satir[3])
                    aylikButunVeriler.append(deger)

                with open(adres, "wb") as fp:
                    pickle.dump(aylikButunVeriler, fp)

                end = time.time()
                #print("yiliAylaraAyirFonk() i= {} ve j={} icin bitti: {}".format(i, j, end-start))

    def latLongdanAdresBul(self):
        geolocator = Nominatim(user_agent="trafSite")
        for i in range(5):
            location = geolocator.reverse("40.980141, 29.082270")
            #print(location.address)
            location = geolocator.reverse("40.980141, 29.122270")
            #print(location.address)
            location = geolocator.reverse("40.980141, 29.242270")
            #print(location.address)
            location = geolocator.reverse("40.980141, 29.452270")
            #print(location.address)



    ### Her bir sensor icin hiz degerlerini filtreleyip bu hiz degerlerinin standart sapmasini aliyoruz
    ### ve (sensorNo, standartSapmaDegeri) ikilileri formatinda listeye ekleyip dosyaya binary olarak kaydediyoruz.
    def herSensorunStandartSapmasi(self, yil, ay, ayinKaci, vSegDir, butunDegerlerAdres, sadeceSensorlerAdres):
        stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"
        standartSapmaAdres = stdeviAdres+ "{}-{}-{}-{}-StandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)

        vSegDir = int(vSegDir)

        #print("herSensorunStandartSapmasi() fonksiyonuna girdi")
        start = time.time()
        ### Sensor No'larin bulundugu listeyi dosyadan liste olarak okudu
        with open(sadeceSensorlerAdres, "rb") as fp:
            distinctIDs = pickle.load(fp)

        ### Kaydedilen sensor icin veritabaninda bulunan 6 degeri(vSegID, vSegDir, fusedSpeed, fusedDate, havaDurumuSensorNo, sicaklik) dosyadan liste olarak okudu
        with open(butunDegerlerAdres, "rb") as fp:
            butunDegerler = pickle.load(fp)

        SSapmaListesi = []
        bozanIndis = -1
        distinctIDs.sort()

        ### DB'den sirali olarak gelen listeyi bir daha siraladik, yoksa sirali gelmedi mi?
        butunDegerler.sort()
        distinctIDs = []
        lenButunDegerler = len(butunDegerler)
        for i in range(lenButunDegerler-1):
            if (butunDegerler[i][0] != butunDegerler[i+1][0]):
                distinctIDs.append(butunDegerler[i][0])
        distinctIDs.append(butunDegerler[i][0])

        ### istenen sensore ait hizlari bulup hizlar[] listesine ekliyoruz.
        for distinctID in distinctIDs:
            indexDistinctID = distinctIDs.index(distinctID)
            hizlar = []

            ### istenen gundeki butun degerler(6 deger) icinden istedigimiz vSegID ve vSegDir degerlerini
            ### buluyor ve hizlarini hizlar[] listesine ekliyor.
            i = bozanIndis
            sayi = 0
            #lenButunDegerler = len(butunDegerler)
            while ( (sayi >= 0) and (i<lenButunDegerler-1) ):
                i += 1
                degerler = butunDegerler[i]
                #print(degerler)
                if ( degerler[0] == distinctID ):
                    hizlar.append( degerler[3] )
                    sayi = 1
                else:
                    bozanIndis = i-1
                    sayi = -sayi


            ### Kaydedilen hizlarin standart sapmasini hesaplayip dosyaya binary olarak kaydediyoruz.

            sensorVeStandartSapmaListesi = []
            try:
                SSapma = statistics.stdev(hizlar)
                sensorVeStandartSapmaListesi.append(distinctID)
                sensorVeStandartSapmaListesi.append(SSapma)
                SSapmaListesi.append(sensorVeStandartSapmaListesi)
            except StatisticsError:
                pass




        ### (SensorNo, StandartSapmaDegeri) seklindeki listeyi dosyaya binary olarak kaydettik
        with open(standartSapmaAdres, 'wb') as fp:
            pickle.dump(SSapmaListesi, fp)

        with open(standartSapmaAdres, "rb") as fp:
            SSliste = pickle.load(fp)

        #print("SSliste: ", SSliste)

        end = time.time()
        #print("SQLeBaglanKarma.herSensorunStandartSapmasi() fonksiyonundan cikti, ", round(end-start,4))

    def veriyiSuzVeKaydet(self, vSegID, vSegDir, ayinKaci, ay, adres, yil, cursor):

        # cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
        #                       "SERVER=ASUS;"
        #                       "Database=FusedData-2016-2017-2018;"
        #                       "Trusted_Connection=yes;")
        # cursor = cnxn.cursor()

        start = time.time()
        komut = (
            "SELECT convert(varchar(3), datepart(hh, fusedDate))+':'+convert(varchar(3), datepart(mi, fusedDate)), avg(cast(fusedSpeed as money))"
            " FROM [FusedData-2016-2017-2018].dbo.[{}_Kopru_Giris_Cikislari] WHERE vSegID={} and vSegDir={} and"
            " months='{}' and datepart(dd, fusedDate) in ({}) "
            " group by datepart(hh, fusedDate), datepart(mi, fusedDate)"
            " order by datepart(hh, fusedDate), DATEPART(mi, fusedDate)".format(yil, vSegID, vSegDir, ay, ayinKaci)
            )
        cursor.execute(komut)
        end = time.time()
        #print("****************fark: ", round(end-start,4))

        # csv dosyalarini kaydettik
        # =====================================================================
        with open(adres, "w") as yaz:
            for row in cursor:
                satir = row[0] + ";"
                satir += str(row[1])
                satir += "\n"
                yaz.write(satir)
        return
