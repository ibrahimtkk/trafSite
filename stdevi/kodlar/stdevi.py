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
        #print("stdevi.degerleriAl('home_to_stdevi') fonksiyonuna girdik")
        tarihParcalanacakString = request.POST.get('datepicker5')
        vSegDir = request.POST.get('vSegDirStandartSapma')
    elif (fonksiyon == 'home_to_renkliHarita'):
        tarihParcalanacakString = request.POST.get('datepicker6')
        semt = request.POST.get('semt')
        vSegDir = request.POST.get('vSegDirRenkliHarita')
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    yil = tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[0].replace('0', '')
    ayinKaci = tarihParcalanmisListe[1].replace('0', '')


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
    # (?-1)   belliBirGun.adresBilgileriniKaydet()
    stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"
    adresler = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\'
    butunVerilerAdres = stdeviAdres + "{}-{}-{}-{}-ButunVeriler.csv".format(yil, ay, ayinKaci, vSegDir)
    sadeceSensorlerAdres = stdeviAdres + "{}-{}-{}-SadeceSensorNo.csv".format(yil, ay, ayinKaci)
    standartSapmaAdres = stdeviAdres + "{}-{}-{}-{}-StandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)
    siraliStandartSapmaAdres = stdeviAdres + "{}-{}-{}-{}-SiraliStandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)
    siraliSS = "{}-{}-{}-{}-SiraliStandartSapma.csv".format(yil, ay, ayinKaci, vSegDir)
    butunVeriler = '{}-{}-{}-{}-ButunVeriler.csv'.format(yil, ay, ayinKaci, vSegDir)

    if (fonksiyon=='home_to_renkliHarita'):

        hizSiniri = 50

        ### [semt, [vSegID1, ortHiz1, yKoor1, xKoor1], [vSegID2, ortHiz2, yKoor2, xKoor2] ]
        ### (?-3)
        secilenSemttekiSensorlerinOrtHizlariVeKoordinatlari = '{}-{}-{}-{}-{}-secilenSemttekiSensorlerinOrtHizlariVeKoordinatlari.csv'.format(yil, ay, ayinKaci, vSegDir, semt)
        if secilenSemttekiSensorlerinOrtHizlariVeKoordinatlari not in os.listdir(stdeviAdres):
            belliBirGun.secilenSemttekiSensorlerinOrtHizlariVeKoordinatlari(semt, yil, ay, ayinKaci, vSegDir)


        ### Harita renklendirme icin ilk once kullanici tarafindan girilen semte ait sensorleri bulmamiz gerekiyor
        ### Daha sonra bulunan bu sensorlerden sirali olanlarini gruplamamiz gerekiyor boylece ardarda gelen sensorleri
        ### buluyoruz.
        ### Bu islemlerin 1 kere yapilmasi yeterlidir.
        semtlerVeSiraliListelerAdres = 'semtlerVeSiraliListeler.txt'
        if semtlerVeSiraliListelerAdres not in os.listdir(adresler):
            belliBirGun.semttekiSiraliSensorleriBul(yil, ay, ayinKaci)
            print(semtlerVeSiraliListelerAdres, os.listdir(adresler))

        ### [ [1, 30], [2, 31], ... ]  -> [ [vSegID1, ortHiz1], [vSegID2, ortHiz2], ... ]
        ### Girilen tarihteki butun sensorlerin ortalama hizlarini bulur ve dosyaya kaydeder.
        ### Yeni bir tarih girilmedigi surece bu islemin 1 kere yapilmasi yeterlidir.
        ### (?-2)
        sensorlerinOrtHizAdres = '{}-{}-{}-{}-sensorlerVeHizOrt.csv'.format(yil, ay, ayinKaci, vSegDir)
        if sensorlerinOrtHizAdres not in os.listdir(stdeviAdres):
            belliBirGun.sensorlerinOrtHizBul(yil, ay, ayinKaci, vSegDir)

        ### ['Üsküdar', [1, 30], [2, 31], ... ]  -> [semt, [vSegID1, ortHiz1], [vSegID2, ortHiz2], ... ]
        ### Secilen tarih ve semte ait sensorlerin hiz ortalamalarini dosyaya kaydeder.
        ### Yeni tarih girilmedigi surece 1 kere yapilmasi makuldur.
        ### (?-3)
        secilenSemtVeSensorlerinHizOrtAdres = '{}-{}-{}-{}-{}-secilenSemtVeSensorlerinHizOrt.csv'.format(yil, ay, ayinKaci, vSegDir, semt)
        if secilenSemtVeSensorlerinHizOrtAdres not in stdeviAdres:
            belliBirGun.secilenSemttekiSensorlerinOrtHizlari(semt, yil, ay, ayinKaci, vSegDir)

        secilenSemttekiSensorlerinOrtHizlariKoordinatlariVeRenkKodlari = '{}-{}-{}-{}-{}-secilenSemttekiSensorlerinOrtHizlariKoordinatlariVeRenkKodlari.csv'.format(yil, ay, ayinKaci, vSegDir, semt)
        if secilenSemttekiSensorlerinOrtHizlariKoordinatlariVeRenkKodlari not in stdeviAdres:
            belliBirGun.hizaGoreRenklendir(semt, yil, ay, ayinKaci, vSegDir, hizSiniri)

    ### Her bir sensor icin en yakin hava durumu sensorunu bulma islemini yapip bir dosyaya kaydediyoruz.
    ### Bu islemi 1 kere yapmak yeterlidir.
    #belliBirGun.butunAdres2HavaDurumu()

    
    ### Bundan sonrasi her bir sensor icin ayri ayri dosya olusturma ve bu olusturulan dosyalardaki
    ### degerlere gore standart sapma alma islemi olacaktir.




    ### her bir farkli vSegID'yi dosyaya kaydediyor.
    ### Burada SQL'in distinct fonksiyonu kullanılarak hiz kazanci saglanabilir.
    ### Edit: KML dosyasi ile olan bagimizi kestigimizden artik buradaki fonksiyonlari kullanmamiza gerek kalmamistir.


    ### Veritabanindan zaten sirali geldigi icin buna gerek yok.
    # belliBirGun.vSegIDSirala(butunVerilerAdres)


    ### Her ayin 15'ine ait veriler hali hazirda bulunacak. Eger kullanici bunlara ek olarak
    ### baska bir gun girmek isterse veritabaninda bulunmadigi icin veri cikarma islemi yapilir.
    ### Bu islem biraz zaman alabilir, 450 saniye kadar :)
    if siraliSS not in os.listdir(stdeviAdres):
        print(butunVeriler)
        if butunVeriler not in os.listdir(stdeviAdres):
            print('Butun veriler cikariliyor, yaklasik 450 saniye')
            belliBirGun.butunSensorlerBirGun(yil, ay, ayinKaci, cursor, vSegDir)
        print('Butun veriler var, sapma hesaplaniyor')
        belliBirGun.distinctSensorNo(butunVerilerAdres, sadeceSensorlerAdres)
        belliBirGun.herSensorunStandartSapmasi(yil, ay, ayinKaci, vSegDir,butunVerilerAdres, sadeceSensorlerAdres)
        belliBirGun.dosyadanOkuyupSirala(standartSapmaAdres, siraliStandartSapmaAdres)

    end = time.time()
    print("stdevi.degerleriAl() fonksiyonundan ciktik: ", end-start)

    return


def basBitKoorRenkKodu(semt, request, hizLimit):
    tarihParcalanacakString = request.POST.get('datepicker6')
    semt = request.POST.get('semt')
    vSegDir = request.POST.get('vSegDirRenkliHarita')
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    yil = tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[0].replace('0', '')
    ayinKaci = tarihParcalanmisListe[1].replace('0', '')

    with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\semtlerVeSiraliListeler.txt', 'rb') as fp:
        semtlerVeSiraliListeler = pickle.load(fp)
    for semtVeSiraliListeler in semtlerVeSiraliListeler:
        if semtVeSiraliListeler[0]==semt:
            arananSemtVeSiraliListe = semtVeSiraliListeler  # [semt, [ID1, ID2, ID3, ...]]

    with open(
            'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\{}-{}-{}-{}-{}-secilenSemttekiSensorlerinOrtHizlariKoordinatlariVeRenkKodlari.csv'.format(
                    yil, ay, ayinKaci, vSegDir, semt), 'rb') as fp:
        secilenSemtVeSensorlerinHizOrtKoorVeRenk = pickle.load(fp)

    belliBirGun = sql.SQLeBaglanKarma(yil, ay, ayinKaci)


    ### [ [x1, y1, hiz1, x2, y2, hiz2], [x5, y5, hiz5, x6, y6, hiz6, x7, y7, hiz7 ] ]
    #gonderilecek = belliBirGun.SiraliKoorVeHizDondur(semt, yil, ay, ayinKaci, vSegDir)

    #with open('gonderilecek.txt', 'wb') as fp:
    #    pickle.dump(gonderilecek, fp)

    with open('gonderilecek.txt', 'rb') as fp:
        gonderilecek = pickle.load(fp)
    #print("\n\n", gonderilecek)

    """
    for siraliListe in arananSemtVeSiraliListe[1:]:
        for sensorIndex in range(len(siraliListe)-2):
            for hizOrtKoorRenkIndex in range(1, len(secilenSemtVeSensorlerinHizOrtKoorVeRenk)):
                if siraliListe[sensorIndex]==secilenSemtVeSensorlerinHizOrtKoorVeRenk[hizOrtKoorRenkIndex][0]:
                    basX = secilenSemtVeSensorlerinHizOrtKoorVeRenk[hizOrtKoorRenkIndex][3]
                    basY = secilenSemtVeSensorlerinHizOrtKoorVeRenk[hizOrtKoorRenkIndex][2]
                    basRenk = secilenSemtVeSensorlerinHizOrtKoorVeRenk[hizOrtKoorRenkIndex][4]
                    basOrt = secilenSemtVeSensorlerinHizOrtKoorVeRenk[hizOrtKoorRenkIndex][1]

                    bitX = secilenSemtVeSensorlerinHizOrtKoorVeRenk[hizOrtKoorRenkIndex+1][3]
                    bitY = secilenSemtVeSensorlerinHizOrtKoorVeRenk[hizOrtKoorRenkIndex+1][2]
                    bitRenk = secilenSemtVeSensorlerinHizOrtKoorVeRenk[hizOrtKoorRenkIndex+1][4]
                    bitOrt = secilenSemtVeSensorlerinHizOrtKoorVeRenk[hizOrtKoorRenkIndex+1][1]

                    if (basOrt+bitOrt)/2<hizLimit:
                        Renk = "#208B23"
                    else:
                        Renk = "#8b0013"


                    gonderilecek.append( [ basY, basX, bitY, bitX, Renk ] )
                    
    """
    return gonderilecek