from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
import random
from django.shortcuts import render, HttpResponse
from django.shortcuts import render, HttpResponse, get_object_or_404
import pyodbc
import time
from pykml import parser
import pickle
from stdevi.kodlar import stdevi
from stdevi.kodlar import SQLeBaglanKarma as sql
from analizz.kodlar import mypythoncode as mypytoncodeAnaliz
from analizz.kodlar import SQLeBaglanKarma as sqlAnaliz
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def home_view(request):
    print("home_view'dayiz")

    global cursor
    global cnxn
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "SERVER=IBRAHIM;"
                          "Database=FusedData-2016-2017-2018;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()
    print("-------------------Veritabanına bağlandı")

    return render(request, 'home.html', {})


def home_to_stdevi(request):
    start = time.time()
    print("home to stdevideyiz yani artik harita gosterilecek")
    vSegDir = request.POST.get('vSegDirStandartSapma')
    tarih = request.POST.get('datepicker5')
    tarihParcalanmisListe = tarih.split('/')
    year = tarihParcalanmisListe[2]
    # yil = request.POST.get('year')
    month = tarihParcalanmisListe[1].replace('0', '')
    # ay = request.POST.get('month')
    day = tarihParcalanmisListe[0].replace('0', '')
    # ayinKaci = request.POST.get('day')
    vSegDir = request.POST.get('vSegDirStandartSapma')
    print("\n\n--------: ", vSegDir, type(tarih), "\n\n")
    liste = tarih.split('/')
    print(liste)

    stdevi.degerleriAl(request, cursor, cnxn, 'home_to_stdevi')

    ### inputFile: KML dosyasi
    ### IDList[]: vSegID'lerin eklenecegi liste
    ### coordinateList[]: Koordinatlarin eklenecegi liste ( icinde x ve y koordinati virgulle ayrilmis olarak bulunuyor)
    print("/////bitti")
    inputFile = "C:\\Users\\ibrahim\\Desktop\\trafSite\\docu.kml"
    IDList = []
    coordinateList = []
    stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"
    siraliStandartSapmaAdres = stdeviAdres + "{}-{}-{}-{}-SiraliStandartSapma.csv".format(year, month, day, vSegDir)
    acikAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\butunAdresler.txt'
    havaDurumuAdres = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\havaDurumuAdres.txt'

    ### standart sapma miktarlarinin sirali listesi.
    ### sensorNo, sapmaMiktari
    with open(siraliStandartSapmaAdres, 'rb') as fp:
        siraliStandartSapmaListesi = pickle.load(fp)

    ### her bir sensorun acik adresini verir.
    ### vSegID, yKoor, xKoor, ?, acikAdres
    with open(acikAdres, 'rb') as fp:
        acikAdresListesi = pickle.load(fp)

    ### her bir sensore dusen en yakin hava durumu sensorunu verir.
    with open(havaDurumuAdres, 'rb') as fp:
        havaDurumuList = pickle.load(fp)


    ### Acik adres listesindeki sensorleri ayri bir listeye ekliyoruz, boylece index islemi daha rahat yapilabilecek.
    acikAdresIDList = []
    for adres in acikAdresListesi:
        acikAdresIDList.append(adres[0])

    ### HTML'e gonderilecek liste
    ### Bazi sensorler bulunamadigindan ValueError veriyor, ona tekrardan bak
    returnListe = []
    for i in range(20):
        vSegID = siraliStandartSapmaListesi[i][0]
        try:
            acikAdresIDIndex = acikAdresIDList.index(vSegID)
            yKoor = acikAdresListesi[acikAdresIDIndex][1]
            xKoor = acikAdresListesi[acikAdresIDIndex][2]
            standartSapmaSirasi = i
            standartSapmaMiktari = siraliStandartSapmaListesi[i][1]
            acikAdres = acikAdresListesi[acikAdresIDIndex][4]
            innerReturnList = [vSegID, yKoor, xKoor, standartSapmaSirasi, standartSapmaMiktari, acikAdres]
            returnListe.append(innerReturnList)
        except ValueError:
            pass


    returnListe100luk = []
    for i in range(100):
        vSegID = siraliStandartSapmaListesi[i][0]
        try:
            acikAdresIDIndex = acikAdresIDList.index(vSegID)
            yKoor = acikAdresListesi[acikAdresIDIndex][1]
            xKoor = acikAdresListesi[acikAdresIDIndex][2]
            standartSapmaSirasi = i
            standartSapmaMiktari = siraliStandartSapmaListesi[i][1]
            acikAdres = acikAdresListesi[acikAdresIDIndex][4]
            acikAdresList = acikAdres.split(',')
            innerReturnList = [vSegID, yKoor, xKoor, standartSapmaSirasi+1, round(standartSapmaMiktari, 4), acikAdresList[-5]]
            returnListe100luk.append(innerReturnList)
        except ValueError:
            pass

    return render(request, 'stdevi/harita.html', {'allOf': returnListe,
                                                    'alll': returnListe100luk,
                                                })


    #
    # ### KML dosyasini aciyoruz ve koordinatlar ile vSegID'leri ilgili listelere ekliyoruz
    # with open(inputFile) as f:
    #     doc = parser.parse(f).getroot().Document.Folder
    #
    #     for attr in doc.Placemark:
    #         coordinateList.append(attr.MultiGeometry.Point.coordinates)
    #         IDList.append(attr.name)
    #
    # allOfList = []
    # haritaBilgileri = []
    # for i in range(len(IDList)):
    #     b = []
    #     b.append(IDList[i])  # name(sensorNo)
    #     ayriKoordinatList = str(coordinateList[i]).split(",")
    #     b.append(ayriKoordinatList[0])  # y koordinati
    #     b.append(ayriKoordinatList[1])  # x koordinati
    #     b.append(ayriKoordinatList[2])  # onemsiz
    #     allOfList.append(b)
    #
    # HDSNbul = sql.SQLeBaglanKarma(year, month, day)
    # vSegIDveEnYakinHavaDurumuListGenel = []
    # for allOff in allOfList:
    #     vSegIDveEnYakinHavaDurumuListYerel = []
    #     enYakinHDSN = HDSNbul.enYakinHavaDurumuSensorunuBulFunc(allOff)
    #     if (enYakinHDSN == 17060):
    #         enYakinHDSN = "Havalimanı"
    #     elif (enYakinHDSN == 17813):
    #         enYakinHDSN = "Kadıköy"
    #     elif (enYakinHDSN == 18401):
    #         enYakinHDSN = 'Şişli'
    #     elif (enYakinHDSN == 18403):
    #         enYakinHDSN = 'Ümraniye'
    #     elif (enYakinHDSN == 18404):
    #         enYakinHDSN = 'Üsküdar'
    #
    #     vSegIDveEnYakinHavaDurumuListYerel.append(allOff[0])
    #     vSegIDveEnYakinHavaDurumuListYerel.append(enYakinHDSN)
    #     vSegIDveEnYakinHavaDurumuListGenel.append(vSegIDveEnYakinHavaDurumuListYerel)
    #
    # with open(siraliStandartSapmaAdres, 'rb') as fp:
    #     siraliStandartSapmaListesi = pickle.load(fp)
    #
    # a = 0
    # geolocator = Nominatim(user_agent="trafSite")
    # for i in range(20):
    #     vSegID = str(siraliStandartSapmaListesi[i][0])
    #     for j in range(len(allOfList)):
    #         if (str((allOfList[j])[0]) == str(vSegID)):
    #             b = []
    #             b.append(vSegID)
    #             x = allOfList[j][2]
    #             y = allOfList[j][1]
    #             b.append(y)  # y koor
    #             b.append(x)  # x koor
    #             b.append(i)  # standart sapmasi en yuksek kacinci sensor oldugu
    #             b.append(str(siraliStandartSapmaListesi[i][1]))  # standart sapma miktari
    #             #print(siraliStandartSapmaListesi)
    #             IDListIndex = IDList.index(int(vSegID))
    #             b.append(vSegIDveEnYakinHavaDurumuListGenel[IDListIndex][1]) # En yakin hava durumu sensoru ilce ismi
    #             koordinat = strKoordinatDondur(x, y)
    #             try:
    #                 location = geolocator.reverse(koordinat, timeout=None)
    #                 b.append(location.address)
    #                 # parcalaAdres = location.address.split(',')
    #                 # gerekliler = []
    #                 # gerekliler.append(parcalaAdres[-4])
    #                 # gerekliler.append(parcalaAdres[-5])
    #                 # gerekliler.append(parcalaAdres[1])
    #                 # print(parcalaAdres)
    #                 # adresStr = ", ".join(gerekliler)
    #                 # b.append(adresStr)
    #                 print(b)
    #                 haritaBilgileri.append(b)
    #             except GeocoderTimedOut:
    #                 print("error time out")
    #                 pass
    #
    # # print(haritaBilgileri)
    # end = time.time()
    # print("views.stdevi_harita() fonksiyonu bitti:", round(end - start))
    #
    # print("haritaBilgileri", haritaBilgileri)



    # return render(request, 'stdevi/harita.html', {})

    #return render(request, 'stdevi/harita.html')

def strKoordinatDondur(x, y):
    koor = "{}, {}".format(str(x), str(y) )
    return koor

def home_to_tumGun(request):
    start = time.time()

    basSaat = request.POST.get('datetimepicker7')
    bitSaat = request.POST.get('datetimepicker8')
    basSaatList = basSaat.split(':')
    bitSaatList = bitSaat.split(':')
    basSaatSaat = basSaatList[0]
    basSaatDakika = basSaatList[1]
    bitSaatSaat = bitSaatList[0]
    bitSaatDakika = bitSaatList[1]


    secilenX = request.POST.get('lat')
    secilenY = request.POST.get('lng')
    enYakinSensorID = mypytoncodeAnaliz.haritadanEnYakinSensorBul(request)
    print(enYakinSensorID)
    vSegID = enYakinSensorID
    #vSegID = request.POST.get('vSegIDTumGun')
    vSegDir = request.POST.get('vSegDirTumGun')
    #tarih = request.POST.get('datepicker1')

    mypytoncodeAnaliz.degerleriAl(request, cursor, vSegID,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
    end = time.time()
    tarihParcalanacakString = request.POST.get('datepicker1')
    #koordinatlar = request.POST.get('lat') + request.POST.get('lng')
    #print("***************koordinatlar: ", koordinatlar)
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    #vSegDir = request.POST.get('vSegDirTumGun')
    #vSegID = request.POST.get('vSegIDTumGun')
    yil = tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[1]
    ayinKaci = tarihParcalanmisListe[0]
    #print("ay: ", ay)
    if (ay[0] == "0"):
        ay = ay.replace("0", "")
    if (ayinKaci[0] == "0"):
        ayinKaci = ayinKaci.replace("0", "")
    ayinKaci = tarihParcalanmisListe[0]
    resimBilgisi = "images/" + yil + "-" + ay + "-" + ayinKaci + "-" + str(vSegID) + "-" + vSegDir + ".png"
    #resimBilgisi = "images/" + yil + "-" + ay + "-" + ayinKaci + "-" +"-" + ".png"
    #print("resimBilgisi: ", resimBilgisi, sep="")
    #mypytoncodeAnaliz.degerleriAl(request, cursor)
    return render(request, 'analizz/grafik.html', {'resimIsmi': resimBilgisi})

def home_to_renkliHarita(request):
    start = time.time()
    #stdevi.degerleriAl(request, cursor, cnxn, 'home_to_renkliHarita')
    end = time.time()
    
    hizLimit = 30

    start = time.time()
    #mypytoncodeAnaliz.degerleriAl(request, cursor, vSegID)

    ### siraliKoorVeHiz = [ [x1, y1, hiz1, x2, y2, hiz2], [x5, y5, hiz5, x6, y6, hiz6, x7, y7, hiz7 ] ]
    siraliKoorVeHiz = stdevi.basBitKoorRenkKodu(request, cursor)
    end = time.time()
    print("siraliKoorVeHiz: ", end-start)

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




    ### HTML'e gonderilecekler: baslangicKoor, bitisKoor, Renkkodu

    #distinctSemtIndex = distinctSemt.index(semt)
    ### o semte ait butun vSegID'leri dondurur
    #semtinSensorleri = semtlerinSensorleri[distinctSemtIndex]

    #for i in basBitKoorRenkKodu:
    #    print(i)
    return render(request, 'analizz/renkliHarita.html', {'siraliKoorVeHiz': siraliKoorVeHiz})