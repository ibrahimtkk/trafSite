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
import pickle

def degerleriAl(request, cursor, cnxn, fonksiyon):
    start = time.time()
    if (fonksiyon == 'home_to_stdevi'):
        tarihParcalanacakString = request.POST.get('datepicker5')
        vSegDir = request.POST.get('vSegDirStandartSapma')        
        
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    yil = tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[1].replace('0', '')
    gun = tarihParcalanmisListe[0].replace('0', '')


    # ===================================================================
    yiliAylaraBol = False
    acikAdresBul = False
    # ===================================================================


    #birgun = sql.SQLeBaglanKarma(yil, ay, gun, vSegID, vSegDir)
    #birgun.veriyiSuzVeKaydet(vSegID, vSegDir, gun, ay, adres, yil, cursor)

    belliBirGun = sql.SQLeBaglanKarma(yil, ay, gun)

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
    # (?-1)   belliBirGun.adresBilgileriniKaydet()
    stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"
    renkliYolAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\"
    adresler = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\'
    butunVerilerAdres = stdeviAdres + "{}-{}-{}-{}-ButunVeriler.csv".format(yil, ay, gun, vSegDir)
    
    standartSapmaAdres = stdeviAdres + "{}-{}-{}-{}-StandartSapma.csv".format(yil, ay, gun, vSegDir)
    siraliStandartSapmaAdres = stdeviAdres + "{}-{}-{}-{}-SiraliStandartSapma.csv".format(yil, ay, gun, vSegDir)
    
    butunVeriler = '{}-{}-{}-{}-ButunVeriler.csv'.format(yil, ay, gun, vSegDir)

    if (fonksiyon=='home_to_stdevi'):
        sadeceSensorlerAdres = stdeviAdres + "{}-{}-{}-SadeceSensorNo.csv".format(yil, ay, gun)
        if siraliStandartSapmaAdres not in os.listdir(stdeviAdres):
            print(butunVeriler)
            belliBirGun.butunSensorlerBirGun(yil, ay, gun, cursor, vSegDir)
            belliBirGun.distinctSensorNo(butunVerilerAdres, sadeceSensorlerAdres)
            belliBirGun.herSensorunStandartSapmasi(yil, ay, gun, vSegDir, butunVerilerAdres, sadeceSensorlerAdres)
            belliBirGun.dosyadanOkuyupSirala(standartSapmaAdres, siraliStandartSapmaAdres)

    return


def basBitKoorRenkKodu(request, cursor):
    tarihParcalanacakString = request.POST.get('datepicker6')
    vSegDir = request.POST.get('vSegDirRenkliHarita')
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    yil = tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[1].replace('0', '')
    gun = tarihParcalanmisListe[0].replace('0', '')

    basSaat = request.POST.get('datetimepicker5')
    bitSaat = request.POST.get('datetimepicker6')
    basSaatList = basSaat.split(':')
    bitSaatList = bitSaat.split(':')
    basSaatSaat = basSaatList[0]
    basSaatDakika = basSaatList[1]
    bitSaatSaat = bitSaatList[0]
    bitSaatDakika = bitSaatList[1]

    vSegIDveOrtHizAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\{}-{}-{}-{}-{}-{}-{}-{}-vSegIDveOrtHiz.pickle'.format(
                    yil, ay, gun, vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)

    belliBirGun = sql.SQLeBaglanKarma(yil, ay, gun)

    renkliHaritaKlasor = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\'
    koorVeHizAdres = '{}-{}-{}-{}-{}.{}-{}.{}-koorVeHiz.pickle'.format(yil, ay, gun, vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)

    if koorVeHizAdres not in os.listdir(renkliHaritaKlasor):
        belliBirGun.renkliHaritaSaatlikVeDakikalikSQLSorgusu(cursor, yil, ay, gun, vSegDir, basSaat, bitSaat)
        siraliKoorVeHiz = belliBirGun.SiraliKoorVeHizDondur(yil,ay,gun,vSegDir, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
        with open(renkliHaritaKlasor+koorVeHizAdres, 'wb') as fp:
            pickle.dump(siraliKoorVeHiz, fp)

    with open(renkliHaritaKlasor+koorVeHizAdres, 'rb') as fp:
        siraliKoorVeHiz = pickle.load(fp)
    print("asdfff")

    ### enAz3Sensor = icerisinde en az 3 sensor olan liste
    enAz3Sensor = []
    for i in siraliKoorVeHiz:
        if len(i) < 7:
            enAz3Sensor.append(i)
    print("---")
    print(len(siraliKoorVeHiz))
    for i in enAz3Sensor:
        siraliKoorVeHiz.remove(i)
    print(len(siraliKoorVeHiz))

    siraliKoorVeHiz = belliBirGun.uzakSensorleriParcala(siraliKoorVeHiz)
    return siraliKoorVeHiz

def tarihIcinOnTemizlik(request, cursor):
    vSegDir = request.POST.get('vSegDirTahmin')
    vSegID = request.POST.get('vSegIDTahmin')
    k = int(request.POST.get('KTahmin'))
    renkliHaritaKlasor = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\'

    tarih = request.POST.get('datepicker7')
    tarihParcalanmisListe = tarih.split('/')
    yil = tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[1].replace('0', '')
    gun = tarihParcalanmisListe[0].replace('0', '')
    saatTahmin = request.POST.get('datetimepicker9')
    tahminList = saatTahmin.split(':')
    saatTahmin = tahminList[0]
    dakikaTahmin = tahminList[1]

    renkliHaritaKlasor = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\renkliYol\\'
    koorVeHizAdres = '{}-{}-{}-{}-{}.{}-{} tahmin-koorVeHiz.pickle'.format(yil, ay, gun, vSegDir, saatTahmin, dakikaTahmin, k)
    belliBirGun = sql.SQLeBaglanKarma(yil, ay, gun)

    if koorVeHizAdres not in os.listdir(renkliHaritaKlasor):
        belliBirGun.stringSQLSorgusuTahmin(request, cursor, tarih, k, vSegDir)
        siraliKoorVeHiz = belliBirGun.SiraliKoorVeHizDondurTahmin(yil,ay,gun,vSegDir, saatTahmin, dakikaTahmin, k)
        with open(renkliHaritaKlasor+koorVeHizAdres, 'wb') as fp:
            pickle.dump(siraliKoorVeHiz, fp)

    with open(renkliHaritaKlasor+koorVeHizAdres, 'rb') as fp:
        siraliKoorVeHiz = pickle.load(fp)
    print("asdfff")

    ### enAz3Sensor = icerisinde en az 3 sensor olan liste
    enAz3Sensor = []
    for i in siraliKoorVeHiz:
        if len(i) < 7:
            enAz3Sensor.append(i)
    print("---")
    print(len(siraliKoorVeHiz))
    for i in enAz3Sensor:
        siraliKoorVeHiz.remove(i)
    print(len(siraliKoorVeHiz))

    siraliKoorVeHiz = belliBirGun.uzakSensorleriParcala(siraliKoorVeHiz)
    return siraliKoorVeHiz