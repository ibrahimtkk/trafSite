from django.shortcuts import render, HttpResponse
from django.shortcuts import render, HttpResponse, get_object_or_404
import pyodbc
import time
from pykml import parser
import pickle
from stdevi.kodlar import stdevi
from stdevi.kodlar import SQLeBaglanKarma as sql
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

    return render(request, 'home2.html', {})


def home_to_stdevi(request):
    start = time.time()
    print("home to stdevideyiz yani artik harita gosterilecek")
    vSegDir = request.POST.get('vSegDirStandartSapma')
    tarih = request.POST.get('datepicker5')
    tarihParcalanmisListe = tarih.split('/')
    year = tarihParcalanmisListe[2]
    # yil = request.POST.get('year')
    month = tarihParcalanmisListe[0].replace('0', '')
    # ay = request.POST.get('month')
    day = tarihParcalanmisListe[1].replace('0', '')
    # ayinKaci = request.POST.get('day')
    vSegDir = request.POST.get('vSegDirStandartSapma')
    print("\n\n--------: ", vSegDir, type(tarih), "\n\n")
    liste = tarih.split('/')
    print(liste)

    stdevi.degerleriAl(request, cursor, cnxn)

    ### inputFile: KML dosyasi
    ### IDList[]: vSegID'lerin eklenecegi liste
    ### coordinateList[]: Koordinatlarin eklenecegi liste ( icinde x ve y koordinati virgulle ayrilmis olarak bulunuyor)
    print("/////bitti")
    inputFile = "C:\\Users\\ibrahim\\Desktop\\trafSite\\docu.kml"
    IDList = []
    coordinateList = []
    stdeviAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\stdevi\\"
    siraliStandartSapmaAdres = stdeviAdres + "{}-{}-{}-{}-SiraliStandartSapma.csv".format(year, month, day, vSegDir)

    ### KML dosyasini aciyoruz ve koordinatlar ile vSegID'leri ilgili listelere ekliyoruz
    with open(inputFile) as f:
        doc = parser.parse(f).getroot().Document.Folder

        for attr in doc.Placemark:
            coordinateList.append(attr.MultiGeometry.Point.coordinates)
            IDList.append(attr.name)

    allOfList = []
    haritaBilgileri = []
    for i in range(len(IDList)):
        b = []
        b.append(IDList[i])  # name(sensorNo)
        ayriKoordinatList = str(coordinateList[i]).split(",")
        b.append(ayriKoordinatList[0])  # y koordinati
        b.append(ayriKoordinatList[1])  # x koordinati
        b.append(ayriKoordinatList[2])  # onemsiz
        allOfList.append(b)

    HDSNbul = sql.SQLBaglanSinif(year, month, day)
    vSegIDveEnYakinHavaDurumuListGenel = []
    for allOff in allOfList:
        vSegIDveEnYakinHavaDurumuListYerel = []
        enYakinHDSN = HDSNbul.enYakinHavaDurumuSensorunuBulFunc(allOff)
        if (enYakinHDSN == 17060):
            enYakinHDSN = "Havalimanı"
        elif (enYakinHDSN == 17813):
            enYakinHDSN = "Kadıköy"
        elif (enYakinHDSN == 18401):
            enYakinHDSN = 'Şişli'
        elif (enYakinHDSN == 18403):
            enYakinHDSN = 'Ümraniye'
        elif (enYakinHDSN == 18404):
            enYakinHDSN = 'Üsküdar'

        vSegIDveEnYakinHavaDurumuListYerel.append(allOff[0])
        vSegIDveEnYakinHavaDurumuListYerel.append(enYakinHDSN)
        vSegIDveEnYakinHavaDurumuListGenel.append(vSegIDveEnYakinHavaDurumuListYerel)

    with open(siraliStandartSapmaAdres, 'rb') as fp:
        siraliStandartSapmaListesi = pickle.load(fp)

    a = 0
    geolocator = Nominatim(user_agent="trafSite")
    for i in range(20):
        vSegID = str(siraliStandartSapmaListesi[i][0])
        for j in range(len(allOfList)):
            if (str((allOfList[j])[0]) == str(vSegID)):
                b = []
                b.append(vSegID)
                x = allOfList[j][2]
                y = allOfList[j][1]
                b.append(y)  # y koor
                b.append(x)  # x koor
                b.append(i)
                b.append(str(siraliStandartSapmaListesi[i][1]))
                IDListIndex = IDList.index(int(vSegID))  # En yakin hava durumu sensoru ilce ismi
                b.append(vSegIDveEnYakinHavaDurumuListGenel[IDListIndex][1])
                koordinat = strKoordinatDondur(x, y)
                try:
                    location = geolocator.reverse(koordinat, timeout=None)
                    b.append(location.address)
                    # parcalaAdres = location.address.split(',')
                    # gerekliler = []
                    # gerekliler.append(parcalaAdres[-4])
                    # gerekliler.append(parcalaAdres[-5])
                    # gerekliler.append(parcalaAdres[1])
                    # print(parcalaAdres)
                    # adresStr = ", ".join(gerekliler)
                    # b.append(adresStr)
                    print(b)
                    haritaBilgileri.append(b)
                except GeocoderTimedOut:
                    print("error time out")
                    pass

    # print(haritaBilgileri)
    end = time.time()
    print("views.stdevi_harita() fonksiyonu bitti:", round(end - start))

    print(len(haritaBilgileri))

    return render(request, 'stdevi/harita.html', {'allOf': haritaBilgileri})

    # return render(request, 'stdevi/harita.html', {})

    return render(request, 'stdevi/harita.html')

def strKoordinatDondur(x, y):
    koor = "{}, {}".format(str(x), str(y) )
    return koor