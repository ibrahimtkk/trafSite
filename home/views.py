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
    kDegeri = request.POST.get('KTumGun')


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
    resimBilgisi = "images/" + yil + "-" + ay + "-" + ayinKaci + "-" + str(vSegID) + "-" + vSegDir + "-" + basSaatSaat + "." + basSaatDakika + "-" + bitSaatSaat + "." + bitSaatDakika + ".png"
    #resimBilgisi = "images/" + yil + "-" + ay + "-" + ayinKaci + "-" +"-" + ".png"
    #print("resimBilgisi: ", resimBilgisi, sep="")
    #mypytoncodeAnaliz.degerleriAl(request, cursor)
    return render(request, 'analizz/grafik.html', {'resimIsmi': resimBilgisi})

def home_to_renkliHarita(request):
    start = time.time()
    ### siraliKoorVeHiz = [ [x1, y1, hiz1, x2, y2, hiz2], [x5, y5, hiz5, x6, y6, hiz6, x7, y7, hiz7 ] ]
    siraliKoorVeHiz = stdevi.basBitKoorRenkKodu(request, cursor)
    end = time.time()
    print("siraliKoorVeHiz: ", end-start)
    return render(request, 'analizz/renkliHarita.html', {'siraliKoorVeHiz': siraliKoorVeHiz})

def home_to_tahmin(request):
    vSegDir = request.POST.get('vSegDirTahmin')
    vSegID = request.POST.get('vSegIDTahmin')
    # tarih = tahmin edilecek tarih
    tarih = request.POST.get('tarihTahmin')
    k = request.POST.get('KTahmin')

    siraliKoorVeHizTahmin = stdevi.tarihIcinOnTemizlik(request, cursor)

    return render(request, 'analizz/renkliHarita.html', {'siraliKoorVeHiz': siraliKoorVeHizTahmin})

def home_to_aylikHiz(request):
    acikAdresDosyaYolu = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\adresler\\butunAdresler.txt'
    resimAdresi, lat, lng, vSegID = mypytoncodeAnaliz.aylikOrtHizBul(request, cursor)
    #resimAdresi = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\static\\images\\aylik15DakikalikHızOrtCizgiGrafigi.png'
    with open(acikAdresDosyaYolu, 'rb') as fp:
        acikAdresListesi = pickle.load(fp)
    acikAdresIDList = []
    for adres in acikAdresListesi:
        acikAdresIDList.append(adres[0])
    indexx = acikAdresIDList.index(vSegID)
    acikAdres = acikAdresListesi[indexx][4]
    return render(request, 'analizz/aylikGrafik.html', {'resimAdresi': resimAdresi,
                                                        'lat': lat,
                                                        'lng': lng,
                                                        'acikAdres': acikAdres,
                                                        })

def home_to_havaDurumu(request):
    resimAdresi = mypytoncodeAnaliz.havaDurumu(request, cursor)

    cursor.close()
    cnxn.close()
    return render(request, 'analizz/havaDurumu.html', {'resimAdresi': resimAdresi})