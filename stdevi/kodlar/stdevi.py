from . import SQLeBaglanKarma as sql
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pyodbc
import matplotlib.pyplot as plt
import matplotlib
from sympy import S, symbols
import sympy
import numpy as np
import time
from pykml import parser


def degerleriAl(request, cursor, cnxn):
    start = time.time()
    print("stdevi.degerleriAl() fonksiyonuna girdik")
    yil = request.POST.get('year')
    ay = request.POST.get('month')
    ayinKaci = request.POST.get('day')
    vSegDir = request.POST.get('vSegDir')
    derece = 11
    derece7 = 7
    butunGun = True
    yiliAylaraBol = False

    #adres = "C:\\Users\\ASUS\\Desktop\\trafSite\\CSV\\stdevi\\stdevi{}-{}-{}.csv".format(yil, ay, ayinKaci)

    #yil = 2017
    #ay = 'Mayis'
    #vSegDir = 0
    #vSegID = 471
    #ayinKaci = 19
    print("butun degerler:", yil, ay, ayinKaci)

    #birgun = sql.SQLBaglanSinif(yil, ay, ayinKaci, vSegID, vSegDir)
    #birgun.veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, ay, adres, yil, cursor)

    belliBirGun = sql.SQLBaglanSinif(yil, ay, ayinKaci)
    if yiliAylaraBol == True:
        belliBirGun.yiliAylaraAyirFonk(cursor, yil, ay)
    stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"

    ### KML dosyasindaki her bir sensorun en yakin oldugu hava durumu sensorunu SQL'e kolon olarak ekle.
    ### Not: Bu islem her ay ve vSegDir icin 1 kereye mahsus yapilacak!!!
    # belliBirGun.sensorVeEnYakinHavaDurumuSensorunuBulVeKaydet(cursor, cnxn, belliBirGun, yil, ay, vSegDir)

    ### Veritabanindaki tabloya uygun hava durumu sicaklik bilgisi ekler.
    ### Bu islem de sadece 1 kere yapilacaktir.
    # belliBirGun.tabloyaSicaklikBilgisiEkle(cursor, cnxn)
    


    
    if butunGun == True:
        belliBirGun.butunSensorlerBirGun(yil, ay, ayinKaci, cursor, vSegDir)
    
    ### Bundan sonrasi her bir sensor icin ayri ayri dosya olusturma ve bu olusturulan dosyalardaki
    ### degerlere gore standart sapma alma islemi olacaktir.
    
    butunVerilerAdres = stdeviAdres+"{}-{}-{}-ButunVeriler.csv".format(yil, ay, ayinKaci)
    sadeceSensorlerAdres = stdeviAdres+"{}-{}-{}-SadeceSensorNo.csv".format(yil, ay, ayinKaci)
    standartSapmaAdres = stdeviAdres+ "{}-{}-{}-{}-StandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)
    siraliStandartSapmaAdres = stdeviAdres+ "{}-{}-{}-{}-SiraliStandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)

    ### her bir farkli vSegID'yi dosyaya kaydediyor.
    ### Burada SQL'in distinct fonksiyonu kullanılarak hiz kazanci saglanabilir.
    #belliBirGun.latLongdanAdresBul()
    belliBirGun.distinctSensorNo(butunVerilerAdres, sadeceSensorlerAdres)

    ### Veritabanindan zaten sirali geldigi icin buna gerek yok.
    # belliBirGun.vSegIDSirala(butunVerilerAdres)

    belliBirGun.herSensorunStandartSapmasi(yil, ay, ayinKaci, vSegDir,butunVerilerAdres, sadeceSensorlerAdres)
    belliBirGun.dosyadanOkuyupSirala(standartSapmaAdres, siraliStandartSapmaAdres)

    end = time.time()
    print("stdevi.degerleriAl() fonksiyonundan ciktik: ", end-start)

    return







    #sensorID_ve_EnYakinHavaDurumuSensorNo_Adres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\sensorID_ve_EnYakinHavaDurumuSensorNo"
    #with open(sensorID_ve_EnYakinHavaDurumuSensorNo_Adres, 'wb') as fp:
    #        pickle.dump(allOfvSegID_ve_EnYakinHavaDurumuSensoruList, fp)