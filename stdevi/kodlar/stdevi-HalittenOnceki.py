from . import SQLeBaglanKarma as sql
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pyodbc
import matplotlib.pyplot as plt
import matplotlib
from sympy import S, symbols
import sympy
import numpy as np
import time


def degerleriAl(request, cursor):
    start = time.time()
    print("stdevi.degerleriAl() fonksiyonuna girdik")
    yil = request.POST.get('year')
    ay = request.POST.get('month')
    ayinKaci = request.POST.get('day')
    vSegDir = request.POST.get('vSegDir')
    derece = 11
    derece7 = 7
    butunGun = False
    ayiGunlereAyirBoolean = False




    #adres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\stdevi{}-{}-{}.csv".format(yil, ay, ayinKaci)

    #yil = 2017
    #ay = 'Mayis'
    #vSegDir = 0
    #vSegID = 471
    #ayinKaci = 19
    print("butun degerler:", yil, ay, ayinKaci)

    #birgun = sql.SQLBaglanSinif(yil, ay, ayinKaci, vSegID, vSegDir)
    #birgun.veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, ay, adres, yil, cursor)

    belliBirGun = sql.SQLBaglanSinif(yil, ay, ayinKaci)

    if ayiGunlereAyirBoolean==True:
        belliBirGun.ayiGunlereAyir(yil, ay, vSegDir)
    
    if butunGun == True:
        belliBirGun.butunSensorlerBirGun(yil, ay, ayinKaci, cursor)

    ### Bundan sonrasi her bir sensor icin ayri ayri dosya olusturma ve bu olusturulan dosyalardaki
    ### degerlere gore standart sapma alma islemi olacaktir.
    stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"
    butunVerilerAdres = stdeviAdres+"{}-{}-{}-ButunVeriler.csv".format(yil, ay, ayinKaci)
    sadeceSensorlerAdres = stdeviAdres+"{}-{}-{}-SadeceSensorNo.csv".format(yil, ay, ayinKaci)
    standartSapmaAdres = stdeviAdres+ "{}-{}-{}-{}-StandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)
    siraliStandartSapmaAdres = stdeviAdres+ "{}-{}-{}-{}-SiraliStandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)

    ### her bir farkli vSegID'yi dosyaya kaydediyor
    belliBirGun.distinctSensorNo(butunVerilerAdres, sadeceSensorlerAdres)

    ### SQL Server uzerinden filtrelenen veriler sirali olmadigi icin siralama islemini Python uzerinden yapiyoruz.
    ### Her bir farkli gun icin bu islemin 1 kere yapilmasi yeterli olacaktir.
    #belliBirGun.vSegIDSirala(butunVerilerAdres)
    
    belliBirGun.herSensorunStandartSapmasi(yil, ay, ayinKaci, vSegDir,butunVerilerAdres, sadeceSensorlerAdres)
    belliBirGun.dosyadanOkuyupSirala(standartSapmaAdres, siraliStandartSapmaAdres)

    end = time.time()
    print("stdevi.degerleriAl() fonksiyonundan ciktik: ", end-start)
    
    return