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
import os


def degerleriAl(request, cursor, cnxn):
    start = time.time()
    print("stdevi.degerleriAl() fonksiyonuna girdik")
    tarihParcalanacakString = request.POST.get('datepicker5')
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    yil = tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[0].replace('0', '')
    ayinKaci = tarihParcalanmisListe[1].replace('0', '')
    vSegDir = request.POST.get('vSegDirStandartSapma')
    derece = 11
    derece7 = 7

    # ===================================================================
    yiliAylaraBol = False
    acikAdresBul = False
    # ===================================================================


    #birgun = sql.SQLeBaglanKarma(yil, ay, ayinKaci, vSegID, vSegDir)
    #birgun.veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, ay, adres, yil, cursor)

    belliBirGun = sql.SQLeBaglanKarma(yil, ay, ayinKaci)

    ### Her bir sensore ait acik adres bulma islemi yapilir.
    ### Bu islemin 1 kere yapilmasi yeterlidir.
    if acikAdresBul == True:
        belliBirGun.adresCikar()

    ### ???
    if yiliAylaraBol == True:
        belliBirGun.yiliAylaraAyirFonk(cursor, yil, ay)

    ### KML dosyasindaki her bir sensorun en yakin oldugu hava durumu sensorunu SQL'e kolon olarak ekle.
    ### Not: Bu islem her ay ve vSegDir icin 1 kereye mahsus yapilacak!!!
    # belliBirGun.sensorVeEnYakinHavaDurumuSensorunuBulVeKaydet(cursor, cnxn, belliBirGun, yil, ay, vSegDir)

    ### Veritabanindaki tabloya uygun hava durumu sicaklik bilgisi ekler.
    ### Bu islem de sadece 1 kere yapilacaktir.
    # belliBirGun.tabloyaSicaklikBilgisiEkle(cursor, cnxn)



    ### 13 tane dosyada bulunan adres bilgilerini tek bir listeye atıyoruz ve bu listeyi dosyaya kaydediyoruz.
    ### Bu islemi 1 kere yapmak yeterlidir.
    # belliBirGun.adresBilgileriniKaydet()

    ### Her bir sensor icin en yakin hava durumu sensorunu bulma islemini yapip bir dosyaya kaydediyoruz.
    ### Bu islemi 1 kere yapmak yeterlidir.
    #belliBirGun.butunAdres2HavaDurumu()

    
    ### Bundan sonrasi her bir sensor icin ayri ayri dosya olusturma ve bu olusturulan dosyalardaki
    ### degerlere gore standart sapma alma islemi olacaktir.

    stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"
    butunVerilerAdres = stdeviAdres+"{}-{}-{}-ButunVeriler.csv".format(yil, ay, ayinKaci)
    sadeceSensorlerAdres = stdeviAdres+"{}-{}-{}-SadeceSensorNo.csv".format(yil, ay, ayinKaci)
    standartSapmaAdres = stdeviAdres+ "{}-{}-{}-{}-StandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)
    siraliStandartSapmaAdres = stdeviAdres+ "{}-{}-{}-{}-SiraliStandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)
    siraliSS = "{}-{}-{}-{}-SiraliStandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)


    ### her bir farkli vSegID'yi dosyaya kaydediyor.
    ### Burada SQL'in distinct fonksiyonu kullanılarak hiz kazanci saglanabilir.
    ### Edit: KML dosyasi ile olan bagimizi kestigimizden artik buradaki fonksiyonlari kullanmamiza gerek kalmamistir.


    ### Veritabanindan zaten sirali geldigi icin buna gerek yok.
    # belliBirGun.vSegIDSirala(butunVerilerAdres)


    ### Her ayin 15'ine ait veriler hali hazirda bulunacak. Eger kullanici bunlara ek olarak
    ### baska bir gun girmek isterse veritabaninda bulunmadigi icin veri cikarma islemi yapilir.
    ### Bu islem biraz zaman alabilir, 450 saniye kadar :)
    if siraliSS not in os.listdir(stdeviAdres):
        belliBirGun.butunSensorlerBirGun(yil, ay, ayinKaci, cursor, vSegDir)
        belliBirGun.distinctSensorNo(butunVerilerAdres, sadeceSensorlerAdres)
        belliBirGun.herSensorunStandartSapmasi(yil, ay, ayinKaci, vSegDir,butunVerilerAdres, sadeceSensorlerAdres)
        belliBirGun.dosyadanOkuyupSirala(standartSapmaAdres, siraliStandartSapmaAdres)

    end = time.time()
    print("stdevi.degerleriAl() fonksiyonundan ciktik: ", end-start)

    return