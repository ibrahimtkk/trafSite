# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 13:23:37 2018

@author: HALIT
"""
import pyodbc
import matplotlib.pyplot as plt
from sympy import S, symbols
import sympy
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import time
from datetime import datetime, timedelta
import pickle
import copy
import pandas as pd
import os

class SQLBaglanSinif():
    derece = 11
    derece7 = 7
    vSegID = 471
    vSegDir = 0
    ay = 'Mayis'
    suzsunMu = False
    yil = 2017
    dakikaAraligiList = [0, 15, 30, 45]
    #ayinKaciList = [19]

    # ayinKaci = self.ayinKaciDuzenle(ayinKaciList)

    def __init__(self, yil, vSegID, vSegDir, ay=1, gun=1):
        self.vSegID = vSegID
        self.vSegDir = vSegDir
        self.ay = ay
        self.yil = yil
        self.ayinKaci = gun

    #def __init__(self, yil, vSegID, vSegDir):
    #    self.vSegID = vSegID
    #    self.vSegDir = vSegDir
    #    self.yil = yil

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

    def getDakikaAraligi(self):
        dakikaAraligi = self.dakikaAraligiDuzenle(self.dakikaAraligiList)
        return dakikaAraligi

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
    def regVerisiniSuzveKaydet(self, vSegID, vSegDir, gun, ay, regreAdres, hafta, yil, cursor, request):
        print("----regVerisiniSuzveKaydet fonksiyonuna girildi!!")
        basSaat = request.POST.get('datetimepicker7')
        bitSaat = request.POST.get('datetimepicker8')
        basSaatList = basSaat.split(':')
        bitSaatList = bitSaat.split(':')
        basSaatSaat = basSaatList[0]
        basSaatDakika = basSaatList[1]
        bitSaatSaat = bitSaatList[0]
        bitSaatDakika = bitSaatList[1]
        gun = int(gun)
        ay = int(ay)
        yil = int(yil)

        if hafta == 1:
            if (gun-7) <= 0:
                if (ay-1) == 0:
                    printf("2016'ya geçildi!!")
                elif ((ay-1) == 1) or ((ay-1) == 3) or ((ay-1) == 5) or ((ay-1) == 7) or ((ay-1) == 8) or ((ay-1) == 10) or ((ay-1) == 12):
                    ay1 = ay-1
                    gun1 = 31+(gun-7)
                elif (ay-1) == 2:
                    ay1 = ay-1
                    if yil % 4 == 0:
                        gun1 = 29+(gun-7)
                    else :
                        gun1 = 28+(gun-7)
                else :
                    ay1 = ay
                    gun1 = 30+(gun-7)
            else : 
                ay1 = ay
                gun1 = gun -7
            komut = (
                "SELECT convert(varchar(3), datepart(hh, fusedDate))+':'+convert(varchar(3), datepart(mi, fusedDate)), avg(cast(fusedSpeed as money))"
                " FROM [FusedData-2016-2017-2018].[dbo].[FusedData{}]  WHERE vSegID={} and vSegDir={} and datepart(mi,fusedDate) in (0, 15, 30, 45) and"
                " (datepart(mm, fusedDate)={} and datepart(dd, fusedDate)={} and datepart(hh, fusedDate)*60 + datepart(mi, fusedDate) between {}*60+{} and {}*60+{}) "
                " group by datepart(hh, fusedDate), datepart(mi, fusedDate)"
                " order by datepart(hh, fusedDate), DATEPART(mi, fusedDate)".format(yil, vSegID, vSegDir, ay1, gun1, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika )
                )
            cursor.execute(komut)
        elif hafta == 2:
            if (gun-7) <= 0:
                if (ay-1) == 0:
                    printf("2016'ya geçildi!!")
                elif ((ay-1) == 1) or ((ay-1) == 3) or ((ay-1) == 5) or ((ay-1) == 7) or ((ay-1) == 8) or ((ay-1) == 10) or ((ay-1) == 12):
                    ay1 = ay-1
                    gun1 = 31+(gun-7)
                    gun2 = gun1-7
                    ay2 = ay1
                elif (ay-1) == 2:
                    ay1 = ay-1
                    if yil%4 == 0:
                        gun1 = 29+(gun-7)
                    else :
                        gun1 = 28+(gun-7)
                    gun2 = gun1-7
                    ay2 = ay1
                else :
                    ay1 = ay-1
                    gun1 = 30+(gun-7)
                    gun2 = gun1-7
                    ay2 = ay1
            else :
                gun1 = gun-7
                ay1 = ay
                if (gun1-7) <= 0:
                    if (ay-1) == 0:
                        printf("2016'ya geçildi!!")
                    elif ((ay-1) == 1) or ((ay-1) == 3) or ((ay-1) == 5) or ((ay-1) == 7) or ((ay-1) == 8) or ((ay-1) == 10) or ((ay-1) == 12):
                        ay2 = ay-1
                        gun2 = 31+(gun1-7)
                    elif (ay-1) == 2:
                        ay2 = ay-1
                        if yil%4 == 0:
                            gun2 = 29+(gun1-7)
                        else :
                            gun2 = 28+(gun1-7)
                    else :
                        ay2 = ay-1
                        gun2 = 30+(gun1-7)
                else :
                    gun2 = gun1-7
                    ay2 = ay
            komut = (
                "SELECT convert(varchar(3), datepart(hh, fusedDate))+':'+convert(varchar(3), datepart(mi, fusedDate)), avg(cast(fusedSpeed as money))"
                " FROM [FusedData-2016-2017-2018].[dbo].[FusedData{}]  WHERE vSegID={} and vSegDir={} and datepart(mi,fusedDate) in (0, 15, 30, 45) and"
                " ((datepart(mm, fusedDate)={} and datepart(dd, fusedDate)={} and datepart(hh, fusedDate)*60 + datepart(mi, fusedDate) between {}*60+{} and {}*60+{}) or"
                " (datepart(mm, fusedDate)={} and datepart(dd, fusedDate)={} and datepart(hh, fusedDate)*60 + datepart(mi, fusedDate) between {}*60+{} and {}*60+{})) "
                " group by datepart(hh, fusedDate), datepart(mi, fusedDate)"
                " order by datepart(hh, fusedDate), DATEPART(mi, fusedDate)".format(yil, vSegID, vSegDir,  ay2, gun2, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika, ay1, gun1, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika )
                )
            cursor.execute(komut)
        elif hafta == 3:
            if (gun-7) <= 0:
                if (ay-1) == 0:
                    printf("2016'ya geçildi!!")
                elif ((ay-1) == 1) or ((ay-1) == 3) or ((ay-1) == 5) or ((ay-1) == 7) or ((ay-1) == 8) or ((ay-1) == 10) or ((ay-1) == 12):
                    ay1 = ay-1
                    gun1 = 31+(gun-7)
                    gun2 = gun1-7
                    ay2 = ay1
                    gun3 = gun2-7
                    ay3 = ay2
                elif (ay-1) == 2:
                    ay1 = ay-1
                    if yil%4 == 0:
                        gun1 = 29+(gun-7)
                    else :
                        gun1 = 28+(gun-7)
                    gun2 = gun1-7
                    ay2 = ay1
                    gun3 = gun2-7
                    ay3 = ay2
                else :
                    ay1 = ay-1
                    gun1 = 30+(gun-7)
                    gun2 = gun1-7
                    ay2 = ay1
                    gun3 = gun2-7
                    ay3 = ay2
            else :
                gun1 = gun-7
                ay1 = ay
                if (gun1-7) <= 0:
                    if (ay-1) == 0:
                        print("2016'ya geçildi!!")
                        ay3 = "halit"
                        gun3="takak"
                    elif ((ay-1) == 1) or ((ay-1) == 3) or ((ay-1) == 5) or ((ay-1) == 7) or ((ay-1) == 8) or ((ay-1) == 10) or ((ay-1) == 12):
                        ay2 = ay-1
                        gun2 = 31+(gun1-7)
                        gun3 = gun2-7
                        ay3 = ay2
                    elif (ay-1) == 2:
                        ay2 = ay-1
                        if yil%4 == 0:
                            gun2 = 29+(gun1-7)
                        else :
                            gun2 = 28+(gun1-7)
                        gun3 = gun2-7
                        ay3 = ay2
                    else :
                        ay2 = ay
                        gun2 = 30+(gun1-7)
                        gun3 = gun2-7
                        ay3 = ay2
                else :
                    ay2 = ay
                    gun2 = gun1-7
                    if (gun2-7) <= 0:
                        if (ay-1) == 0:
                            printf("2016'ya geçildi!!")
                        elif ((ay-1) == 1) or ((ay-1) == 3) or ((ay-1) == 5) or ((ay-1) == 7) or ((ay-1) == 8) or ((ay-1) == 10) or ((ay-1) == 12):
                            ay3 = ay-1
                            gun3 = 31+(gun2-7)
                        elif (ay-1) == 2:
                            ay3 = ay-1
                            if yil%4 == 0:
                                gun3 = 29+(gun2-7)
                            else :
                                gun3 = 28+(gun2-7)
                            gun3 = gun1-7
                        else :
                            gun3 = 30+(gun2-7)
                            ay3 = ay-1
                    else :
                        gun3 = gun2-7
                        ay3 = ay
            komut = (
                "SELECT convert(varchar(3), datepart(hh, fusedDate))+':'+convert(varchar(3), datepart(mi, fusedDate)), avg(cast(fusedSpeed as money))"
                "FROM [FusedData-2016-2017-2018].[dbo].[FusedData{}]  WHERE vSegID={} and vSegDir={} and datepart(mi,fusedDate) in (0, 15, 30, 45) and"
                " ((datepart(mm, fusedDate)={} and datepart(dd, fusedDate)={} and datepart(hh, fusedDate)*60 + datepart(mi, fusedDate) between {}*60+{} and {}*60+{}) or"
                " (datepart(mm, fusedDate)={} and datepart(dd, fusedDate)={} and datepart(hh, fusedDate)*60 + datepart(mi, fusedDate) between {}*60+{} and {}*60+{}) or"
                " (datepart(mm, fusedDate)={} and datepart(dd, fusedDate)={} and datepart(hh, fusedDate)*60 + datepart(mi, fusedDate) between {}*60+{} and {}*60+{}))"
                " group by datepart(hh, fusedDate), datepart(mi, fusedDate)"
                " order by datepart(hh, fusedDate), DATEPART(mi, fusedDate)".format(yil, vSegID, vSegDir, ay3, gun3, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika, ay2, gun2, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika, ay1, gun1, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika )
                )
            cursor.execute(komut)
        with open(regreAdres, "w") as yaz:
            for row in cursor:
                satir = row[0] + ";"
                satir += str(row[1])
                satir += "\n"
                yaz.write(satir)
        print("---- gun1= {} \n---- ay1= {} ".format(gun1,ay1))
        return
       

    def regVerisiniSuzveKaydet2(self, vSegID, vSegDir, gun, ay, regreAdres, hafta, yil, cursor, request):
        basSaat = request.POST.get('datetimepicker7')
        bitSaat = request.POST.get('datetimepicker8')
        basSaatList = basSaat.split(':')
        bitSaatList = bitSaat.split(':')
        basSaatSaat = basSaatList[0]
        basSaatDakika = basSaatList[1]
        bitSaatSaat = bitSaatList[0]
        bitSaatDakika = bitSaatList[1]
        k = hafta
        gun = int(gun)
        ay = int(ay)
        yil = int(yil)
        oGun = datetime(yil, ay, gun)
        sorgu = ''
        ilkSorgu = "SELECT convert(varchar(3), datepart(hh, fusedDate))+':'+convert(varchar(3), datepart(mi, fusedDate)), avg(cast(fusedSpeed as money)) FROM ( "
        sorgu += ilkSorgu
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
                        ' WHERE vSegID={} AND '
                        ' (DATEPART(HOUR, fusedDate)*60 + DATEPART(MINUTE, fusedDate) BETWEEN {}*60+{} AND {}*60+{}) '
                        ' GROUP BY  DATEPART(HOUR, fusedDate), DATEPART(MINUTE, fusedDate) '
                        ' ORDER BY DATEPART(HOUR, fusedDate), DATEPART(MINUTE, fusedDate)'
        ).format(vSegID, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
        sorgu += enSonSorgu
        print(sorgu)
        start = time.time()

        cursor.execute(sorgu)
        with open(regreAdres, "w") as yaz:
            for row in cursor:
                satir = row[0] + ";"
                satir += str(row[1])
                satir += "\n"
                yaz.write(satir)

        stop= time.time()
        print("zaman: ", stop-start)


    def veriyiSuzVeKaydet(self, vSegID, vSegDir, ayinKaci, ay, adres, yil, cursor, request):
        print("----veriyiSuzVeKaydet fonksiyonuna girildi!!")
        basSaat = request.POST.get('datetimepicker7')
        bitSaat = request.POST.get('datetimepicker8')
        basSaatList = basSaat.split(':')
        bitSaatList = bitSaat.split(':')
        basSaatSaat = basSaatList[0]
        basSaatDakika = basSaatList[1]
        bitSaatSaat = bitSaatList[0]
        bitSaatDakika = bitSaatList[1]

        #print("veriyiSuz6566454: ", vSegID, vSegDir, ayinKaci, ay, adres, yil)

        # cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
        #                       "SERVER=HALIT;"
        #                       "Database=FusedData-2016-2017-2018;"
        #                       "Trusted_Connection=yes;")
        # cursor = cnxn.cursor()

        start = time.time()
        komut = (
            "SELECT convert(varchar(3), datepart(hh, fusedDate))+':'+convert(varchar(3), datepart(mi, fusedDate)), avg(cast(fusedSpeed as money))"
            " FROM [FusedData-2016-2017-2018].dbo.[{}-{}-{}] WHERE vSegID={} and"
            " datepart(dd, fusedDate)={} and datepart(mi,fusedDate) in (0, 15, 30, 45) and"
            " datepart(hh, fusedDate)*60 + datepart(mi, fusedDate) between {}*60+{} and {}*60+{} "
            " group by datepart(hh, fusedDate), datepart(mi, fusedDate)"
            " order by datepart(hh, fusedDate), DATEPART(mi, fusedDate)".format(yil, ay, vSegDir, vSegID, ayinKaci, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika )
            )
        cursor.execute(komut)
        end = time.time()
        #print("****************fark: ", end-start)

        # csv dosyalarini kaydettik
        # =====================================================================
        with open(adres, "w") as yaz:
            for row in cursor:
                satir = row[0] + ";"
                satir += str(row[1])
                satir += "\n"
                yaz.write(satir)
        return
        


    def ayinKaciDuzenle(self, ayinKaciList):
        print("----ayinKaciDuzenle fonksiyonuna girildi!!")
        ayinKaci = ""
        for i in ayinKaciList:
            ayinKaci += str(i)
            ayinKaci += ','
        ayinKaci = ayinKaci[:-1]
        return ayinKaci

    def dakikaAraligiDuzenle(self, dakikaAraligiList):
        print("----dakikaAraligiDuzenle fonksiyonuna girildi!!")
        dakikaAraligi = ""
        for i in dakikaAraligiList:
            dakikaAraligi += str(i)
            dakikaAraligi += ','
        dakikaAraligi = dakikaAraligi[:-1]
        return dakikaAraligi

    # csv dosyasindaki 2 kolonu noktali virgunden temizleyip ayri dizilere atiyor.
    def noktaliVirguldenTemizle(self, adres):
        print("----noktaliVirguldenTemizle fonksiyonuna girildi!!")
        liste = []
        gunlerSaat = []
        gunlerHiz = []

        with open(adres, encoding='utf-8-sig') as myfile:
            for line in myfile:
                liste = line.split(";")
                gunlerSaat.append(liste[0])  # saat
                gunlerHiz.append(liste[1])  # hiz

        
        self.duzenle(gunlerSaat, gunlerHiz)

        return gunlerSaat, gunlerHiz

    # 00:00 0. indis olacak sekilde saat ve dakikalari x eksenine indis olarak
    # atiyor.
    def saatiIndisYap(self, gunlerSaat):
        print("----saatiIndisYap fonksiyonuna girildi!!")
        indisler = []
        k = 0
        for i in gunlerSaat:
            k += 1
            virg = i.index(":")
            saat = int(i[:virg])
            dakika = int(i[virg + 1:])
            if(dakika%15 == 0):
                indisler.append(saat * 4 + dakika / 15)
        print("\n----İlk çıkarılan sonuçlar " + str(k))
        indisler = list(map(int, indisler))
        return indisler

    def y_DataOlustur(self, CSVadres):
        print("----y_DataOlustur fonksiyonuna girildi!!")
        gunlerSaat = []
        gunlerHiz = []
        gunlerSaat, gunlerHiz = self.noktaliVirguldenTemizle(CSVadres)
        x_data = self.saatiIndisYap(gunlerSaat)  # x_dattaki degerleri indisleyen degerler
        y_data = gunlerHiz

        return x_data, y_data

    def fitle(self, x_data, y_data, derece):
        print("----fitle fonksiyonuna girildi!!")
        # verilen derecesine gore grafigi fitleyen fonksiyon
        ps = []
        
        ps.extend(np.polyfit(x_data, y_data, derece))

        return ps

    def polyvalla(self, ps, x_data, derece):
        print("----polyvalla fonksiyonuna girildi!!")
        y_preds = []
        # polinomsal degerleri hesaplar. polyval() fonksiyonu degisken olarak array
        # girdigimiz icin bize bir array dondurur.
        y_preds.extend(np.polyval(ps, x_data))
        return y_preds

    def y_predsle(self, x_data, y_data, derece):
        print("----y_predsle fonksiyonuna girildi!!")
        ps = self.fitle(x_data, y_data, derece)
        y_preds = self.polyvalla(ps, x_data, derece)
        # y_p7 = np.poly1d(ps[7])
        # print(y_p7(30))          # 30 noktasindaki degerini verir.
        return y_preds, ps



# ==========================================================================
    def aylikOrtHizBul(self, yil, vSegID, vSegDir, cursor):
        saatler = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
        dakikalar = ['0','15','30','45']
        saatlerVeDakikalar = []
        saatlerVeDakikalarString = []

        for saat in saatler:
            for dakika in dakikalar:
                string = saat+':'+dakika
                saatlerVeDakikalarString.append(string)


        i = 0
        for saat in saatler:
            for dakika in dakikalar:
                i += 0.25
                saatlerVeDakikalar.append(i)
        print(saatlerVeDakikalar)
        emptyList = []
        hizlar = []
        aylikHizlar = []
        for i in range(4):
            print("+++i: ", i)
            sorgu = ("SELECT convert(varchar(3), datepart(hh, fusedDate))+':'+convert(varchar(3), datepart(mi, fusedDate)), avg(cast(fusedSpeed as money)) "
                    " FROM [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] "
                    " WHERE vSegID={} AND DATEPART(MINUTE, fusedDate) in (0,15,30,45) "
                    " GROUP BY DATEPART(HOUR, fusedDate), DATEPART(MINUTE, fusedDate) "
                    " ORDER BY DATEPART(HOUR, fusedDate), DATEPART(MINUTE, fusedDate) "
                    ).format(yil, i+1, vSegDir, vSegID)
            cursor.execute(sorgu)
            result = list(cursor)
            emptyList = []
            satirSaat = []
            satirHiz = []
            for satir in result:
                satirSaat.append(satir[0])
            for satir in result:
                satirHiz.append(satir[1])

            for saatDakika in saatlerVeDakikalarString:
                if saatDakika in satirSaat:
                    indexx = satirSaat.index(saatDakika)
                    emptyList.append(satirHiz[indexx])
                else:
                    emptyList.append(None)

            #for satir in result:
            #    emptyList.append(satir[1])
            #print(emptyList)
            aylikHizlar.append(emptyList)
        plt.figure(figsize=(6 * 3.3, 4 * 3.3))
        plt.xlabel("Saatler",fontsize=20)
        plt.ylabel("Hızlar",fontsize=20)
        for i in range(4):
            print(len(aylikHizlar[i]))
        for i in range(4):
            plt.plot(saatlerVeDakikalar, aylikHizlar[i], "-")
        plt.legend(['Ocak', 'Şubat', 'Mart', 'Nisan'], loc='best')
        resimAdresi = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\static\\images\\aylik15DakikalikHızOrtCizgiGrafigi.png'
        plt.savefig(resimAdresi)
        staticResimAdresi = 'images/aylik15DakikalikHızOrtCizgiGrafigi.png'
        return staticResimAdresi





### HAVA DURUMU
# ==========================================================================

    def havaOlayindanAyVeGunBulYagmur(self, havaOlayi, semt):
        print('havaOlayindanAyVeGunBulYagmur')
        xlsxDosyaAdresi = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\Meteoroloji_Verisi\\201808060F4C-Saatlik Toplam Yağış (mm=kg÷m²) OMGİ.xlsx'
        df = pd.read_excel(xlsxDosyaAdresi)
        #kolonList = list(df.columns.values)
        #arananKolonIndex = kolonList.index(kolonAdi)
        havaOlayiYasananDegerler = []
        xlsxSatirListesi = []
        yagmurluGunler = []
        yagmurluAylar = []
        for row in df.iterrows():
            index, data = row
            ### str, str, float, float, float, float, float
            Istasyon_No, Istasyon_Adi, YIL, AY, GUN, SAAT, Yagis = data[0], data[1], data[2], data[3], data[4], data[5], data[6]
            ### semtten bagimsiz olarak yagmur yagiyorsa hepsini bir listeye al
            ### ama bir gun icin buldugunda diger saatlerini kontrol etmesin
            if ( Yagis>3 and YIL==2017):
                if ( GUN in yagmurluGunler ):
                    indexx = yagmurluGunler.index(GUN)
                    if ( yagmurluAylar[indexx] != AY ):
                        yagmurluGunler.append(GUN)
                        yagmurluAylar.append(AY)
                        innerDegerler = [Istasyon_No, Istasyon_Adi, YIL, AY, GUN, SAAT, Yagis]
                        havaOlayiYasananDegerler.append(innerDegerler)
                elif ( GUN not in yagmurluGunler ):
                    yagmurluGunler.append(GUN)
                    yagmurluAylar.append(AY)
                    innerDegerler = [Istasyon_No, Istasyon_Adi, YIL, AY, GUN, SAAT, Yagis]
                    havaOlayiYasananDegerler.append(innerDegerler)

        #print(havaOlayiYasananDegerler)
        print('havaOlayindanAyVeGunBulYagmurCikis')

        return havaOlayiYasananDegerler

    def havaOlaysizAyVeGunBulYagmur(self, havaOlayiYasananDegerler, secilenSemt):
        print('havaOlaysizAyVeGunBulYagmur')
        xlsxDosyaAdresi = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\Meteoroloji_Verisi\\201808060F4C-Saatlik Toplam Yağış (mm=kg÷m²) OMGİ.xlsx'
        df = pd.read_excel(xlsxDosyaAdresi)

        if secilenSemt=='Üsküdar':
            secilenSemt = 'ÜSKÜDAR'
        elif secilenSemt=='Kadıköy':
            secilenSemt = 'KADIKÖY/GÖZTEPE MARMARA'

        ###  i = [vSegID, semt(excel'deki), yil, ay, gun, saat, miktar]
        print(havaOlayiYasananDegerler[0])
        for i in havaOlayiYasananDegerler:
            havaOlayiYasanmayanDegerler = []
            yagmis = 0
            yil, ay, gun, semt = int(i[2]), int(i[3]), int(i[4]), i[1]
            oGun = datetime(yil, ay, gun)
            onceki1Hafta = oGun - timedelta(days=7)
            ay1HaftaOnceki = int(onceki1Hafta.strftime('%m'))
            gun1HaftaOnceki = int(onceki1Hafta.strftime('%d'))
            for row in df.iterrows():
                index, data = row
                try:    
                    SEMT, YIL, AY, GUN, Yagis = data[1], int(data[2]), int(data[3]), int(data[4]), float(data[6])
                    if (YIL==2017 and AY==ay1HaftaOnceki and GUN==gun1HaftaOnceki and SEMT==semt):
                        if (Yagis>3):
                            yagmis = 1
                            havaOlayiYasanmayanDegerler = []
                        else:
                            Istasyon_No, Istasyon_Adi= data[0], data[1]
                            havaOlayiYasanmayanDegerler = [Istasyon_No, Istasyon_Adi, YIL, AY, GUN, Yagis]
                        #innerDegerler = [Istasyon_No, Istasyon_Adi, YIL, AY, GUN, Yagis]
                        #havaOlayiYasanmayanDegerler.append(innerDegerler)
                except ValueError:
                    pass
            if (yagmis==0 and havaOlayiYasanmayanDegerler!=[]):
                return havaOlayiYasanmayanDegerler
                #if havaOlayiYasanmayanDegerler[1]==EXCELSEMT:
                #    return havaOlayiYasanmayanDegerler
        print('havaOlaysizAyVeGunBulYagmurCikis')
        return False


    def gunVeSensorVerCiktiAl(self, cursor, yil, ay, gun, vSegID, vSegDir, havaOlaysizSemt, olay ):
        havaDurumuKlasor = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\havaDurumu\\'
        havaOlaysizSemt = havaOlaysizSemt.replace('/', '')
        print("-------------------------")
        print(yil, ay, gun, vSegID, vSegDir, havaOlaysizSemt)
        if (olay=='yagmurlu'):
            pickleDosyasi = 'Yagmurlu-{}-{}-{}-{}-{}.pickle'.format(havaOlaysizSemt, gun, ay, yil, vSegDir)
        elif (olay=='yagmursuz'):
            pickleDosyasi = 'Yagmursuz-{}-{}-{}-{}-{}.pickle'.format(havaOlaysizSemt, gun, ay, yil, vSegDir)
        if pickleDosyasi not in os.listdir(havaDurumuKlasor):
            sorgu = (
                " SELECT convert(varchar(3), datepart(hh, fusedDate))+':'+convert(varchar(3), datepart(mi, fusedDate)), fusedSpeed "
                " FROM [FusedData-2016-2017-2018].[dbo].[{}-{}-{}] "
                " WHERE datepart(DAY, fusedDate)={} AND vSegID={} AND "
                " datepart(MINUTE, fusedDate) in (0,15,30,45) ".format(yil, ay, vSegDir, gun, vSegID)
            )
            cursor.execute(sorgu)
            liste = list(cursor)
            #print(liste)
            with open(havaDurumuKlasor+pickleDosyasi, 'wb') as fp:
                pickle.dump(liste, fp)


    def havaOlayiResimCikar(self, havaOlaysizSemt, yil, oncekiAy, oncekiGun, sonrakiAy, sonrakiGun, havaOlayi):
        havaDurumuKlasor = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\havaDurumu\\'
        vSegDir = 0
        havaOlaysizSemt = havaOlaysizSemt.replace('/', '')
        if (havaOlaysizSemt == 'Üsküdar'):
            vSegID = 288
        elif (havaOlaysizSemt == 'Kadıköy'):
            vSegID = 10

        if (havaOlayi == 'Yağmur'):
            pickleDosyasiAdresYagmurlu = 'Yagmurlu-{}-{}-{}-{}-{}.pickle'.format(havaOlaysizSemt, sonrakiGun, sonrakiAy, yil, vSegDir)
            pickleDosyasiAdresYagmursuz = 'Yagmursuz-{}-{}-{}-{}-{}.pickle'.format(havaOlaysizSemt, oncekiGun, oncekiAy, yil, vSegDir)
        with open(havaDurumuKlasor+pickleDosyasiAdresYagmurlu, 'rb') as fp:
            pickleDosyasiYagmurlu = pickle.load(fp)
        with open(havaDurumuKlasor+pickleDosyasiAdresYagmursuz, 'rb') as fp:
            pickleDosyasiYagmursuz = pickle.load(fp)
        #print(pickleDosyasiYagmursuz)
        saatler = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
        dakikalar = ['0','15','30','45']
        saatlerVeDakikalar = []
        

        saatlerVeDakikalarString = []
        for saat in saatler:
            for dakika in dakikalar:
                saatVeDakika = saat+':'+dakika
                saatlerVeDakikalarString.append(saatVeDakika)
        


        i = 0
        for saat in saatler:
            for dakika in dakikalar:
                i += 0.25
                saatlerVeDakikalar.append(i)
        hizlarYagmurlu = []
        hizlarYagmursuz = []
        saatler1 = []
        saatler2 = []
        print("------------")
        print(len(pickleDosyasiYagmurlu))
        for i in pickleDosyasiYagmurlu:
            saatler1.append(i[0])
            hizlarYagmurlu.append(i[1])
        for i in pickleDosyasiYagmursuz:
            saatler2.append(i[0])
            hizlarYagmursuz.append(i[1])

        #saatlerTrue = []
        #for i in saatler1:
        #    if i in saatler2:
        #        saatlerTrue.append(i)

        hizlarYagmurluTrue1 = []
        for i in saatlerVeDakikalarString:
            if i in saatler1:
                indexx = saatler1.index(i)
                hizlarYagmurluTrue1.append(hizlarYagmurlu[indexx])
            else:
                hizlarYagmurluTrue1.append(None)

        hizlarYagmursuzTrue2 = []
        for i in saatlerVeDakikalarString:
            if i in saatler2:
                indexx = saatler2.index(i)
                hizlarYagmursuzTrue2.append(hizlarYagmursuz[indexx])
            else:
                hizlarYagmursuzTrue2.append(None)


        saatlerTrue = []
        for i in saatler1:
            if i in saatler2:
                saatlerTrue.append(i)

        hizlarYagmurluTrue = []
        hizlarYagmursuzTrue = []

        saatlerTrueTrue = []
        for i in saatlerTrue:
            indx = saatlerTrue.index(i)/4
            saatlerTrueTrue.append(indx)
            index1 = saatler1.index(i)
            index2 = saatler2.index(i)
            hizlarYagmurluTrue.append(hizlarYagmurlu[index1])
            hizlarYagmursuzTrue.append(hizlarYagmursuz[index2])

        birdenDoksanAlti = []
        for i in range(96):
            birdenDoksanAlti.append(i/4)

        plt.figure(figsize=(6 * 3.3, 4 * 3.3))
        plt.xlabel("Saatler",fontsize=20)
        plt.ylabel("Hızlar",fontsize=20)
        plt.plot(birdenDoksanAlti, hizlarYagmursuzTrue2, "-")
        plt.plot(birdenDoksanAlti, hizlarYagmurluTrue1, "-")
        plt.legend(['Yağmursuz', 'Yağmurlu'], loc='best')
        resimAdresi = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\static\\images\\Yagmurlu-{}-{}-{}-{}-{}.png'.format(havaOlaysizSemt, sonrakiGun, sonrakiAy, yil, vSegDir)
        plt.savefig(resimAdresi)
        staticResimAdresi = 'images/Yagmurlu-{}-{}-{}-{}-{}.png'.format(havaOlaysizSemt, sonrakiGun, sonrakiAy, yil, vSegDir)
        return staticResimAdresi


# ==========================================================================
"""adres = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\MayisUcuncuCuma.csv"
ayinKaciList = [19]
ayinKaci = ayinKaciDuzenle(ayinKaciList)
dakikaAraligiList = [0,15,30,45]
dakikaAraligi = dakikaAraligiDuzenle(dakikaAraligiList)
if suzsunMu==True:
    veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, dakikaAraligi, ay, adres,yil)"""
# ==========================================================================

# ==========================================================================
"""adres3HI = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\MayisUcuncuHaftaIci.csv"
ayinKaciList = [15,16,17,18]
ayinKaci = ayinKaciDuzenle(ayinKaciList)
# Mayis 3. hafta icinin csv dosyasi
if suzsunMu==True:
    veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, dakikaAraligi, ay, adres3HI,yil)"""
# ==========================================================================

# ==========================================================================
"""adresMayisButunCumalar = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\MayisButunCumalar.csv"
ayinKaciList = [5,12,19]
ayinKaci = ayinKaciDuzenle(ayinKaciList)
dakikaAraligiList = [0,15,30,45]
dakikaAraligi = dakikaAraligiDuzenle(dakikaAraligiList)
if suzsunMu==True:
    veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, dakikaAraligi, ay, adresMayisButunCumalar,yil)"""
# ==========================================================================


# ==========================================================================
"""yil = 2016
adres2016MayisIlkCuma = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\Mayis2016IlkCuma.csv"
ayinKaciList = [13]
ayinKaci = ayinKaciDuzenle(ayinKaciList)
dakikaAraligiList = [0,15,30,45]
dakikaAraligi = dakikaAraligiDuzenle(dakikaAraligiList)
if suzsunMu==True:
    veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, dakikaAraligi, ay, adres2016MayisIlkCuma,yil)"""
# ==========================================================================

"""x_data, y_dataUcuncuCuma = y_DataOlustur(adres,derece,derece7)
x_data, y_dataUcuncuHaftaIci = y_DataOlustur(adres3HI,derece,derece7)
x_data, y_dataButunCumalar = y_DataOlustur(adresMayisButunCumalar,derece,derece7)
x_data, y_data2016IlkCuma = y_DataOlustur(adres2016MayisIlkCuma,derece,derece7)"""

"""ps = []
y_predsUcuncuCuma,ps = y_predsle(x_data, y_dataUcuncuCuma, derece)
y_predsUcuncuHaftaIci,_ = y_predsle(x_data, y_dataUcuncuHaftaIci, derece)
y_predsButunCumalar,_ = y_predsle(x_data, y_dataButunCumalar, derece)
y_preds2016IlkCuma,_ = y_predsle(x_data, y_data2016IlkCuma, derece)"""

# poly1d() fonksiyonu ise bizim tahmini degerini ogrenmek istedigimiz
# sayinin sonucu verir.
# y_p7 = np.poly1d(p7)
# print(y_p7(0))     # 0 noktasindaki egrinin degerini verir.

"""y_trueUcuncuCuma = y_dataUcuncuCuma
x = symbols("x")

for a in range(derece7):
    poly = sum(S("{}".format(v))*x**i for i, v in enumerate(ps[a][::-1]))
    #print("poly: ", poly)
eq_latex = sympy.printing.latex(poly)

print("7. dereceden denklem icin:")
for i in range(10):
    print("{}= ".format(str(i*10)+"-"+ str(10*(i+1)) ), "%",round(mean_absolute_error(y_dataUcuncuCuma[10*i:10*(i+1)], (y_predsUcuncuCuma[derece7])[10*i:10*(i+1)] ),3 ), sep="")
print()
for i in range(10):
    print("{}= ".format(str(i*10)+"-"+ str(10*(i+1)) ), "%",round(mean_absolute_error(y_dataUcuncuHaftaIci[10*i:10*(i+1)], (y_predsUcuncuCuma[derece7])[10*i:10*(i+1)] ),3 ), sep="")
print()
for i in range(10):
    print("{}= ".format(str(i*10)+"-"+ str(10*(i+1)) ), "%",round(mean_absolute_error(y_dataButunCumalar[10*i:10*(i+1)], (y_predsUcuncuCuma[derece7])[10*i:10*(i+1)] ),3 ), sep="")
print()
for i in range(10):
    print("{}= ".format(str(i*10)+"-"+ str(10*(i+1)) ), "%",round(mean_absolute_error(y_data2016IlkCuma[10*i:10*(i+1)], (y_predsUcuncuCuma[derece7])[10*i:10*(i+1)] ),3 ), sep="")
print()
"""

"""#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text', usetex=True)
plt.figure(figsize=(6*3.3, 4*3.3))
plt.title(r'Eq =' r"${}$".format(eq_latex), fontsize=12, color="r")
# plt.plot(x_dat, y_dat, "-") yaparsak x eksenininde ceyrek saatleri
# verir ama o zaman da cok fazla deger oldugundan bir sey anlasilmiyor.
plt.plot(x_data, y_dataUcuncuCuma, "o")
plt.plot(x_data, y_predsUcuncuCuma[derece7], "-" )
plt.plot(x_data, y_predsUcuncuHaftaIci[derece7], "-")
plt.plot(x_data, y_predsButunCumalar[derece7], "-")
plt.plot(x_data, y_preds2016IlkCuma[derece7], "-")
plt.legend(['data', 'Ilk3Cuma', 'Ilk3HaftaIci', 'MayisButunCumalar', '2016MayisIlkCuma'], loc='best')
"""

"""resimAdresUcuncuCuma = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\MayisKarsilastirma.png"
plt.savefig(resimAdresUcuncuCuma)

"""