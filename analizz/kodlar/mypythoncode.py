from sklearn.metrics import mean_squared_error, mean_absolute_error
import pyodbc
import matplotlib
matplotlib.use('Agg')
from . import SQLeBaglanKarma as sql
import matplotlib.pyplot as plt
from sympy import S, symbols
from sklearn.utils import check_array
import sympy
import numpy as np
import os
import pickle
import time
from datetime import datetime, timedelta


def degerleriAl(request, cursor, vSegID, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika):
    print("----degerleriAl fonksiyonuna girildi!!")
    tarihParcalanacakString = request.POST.get('datepicker1')
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    vSegDir = request.POST.get('vSegDirTumGun')
    yil =tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[1]
    #hafta = 3
    hafta = int(request.POST.get('KTumGun'))
    #print("ay: ", ay)
    if (ay[0]=="0"):
        ay = ay.replace("0", "")
    gun = tarihParcalanmisListe[0]
    #print("---", yil, ay, gun)
    #adres = "C:\\Users\\ibrahim\\djangoboys\\CSV1\\MayisUcuncuCuma2017.csv"
    tumGunAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\TumGun\\{}-{}-{}-{}-{}-{}.{}-{}.{}.csv".format(yil, ay, gun, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
    tumGunRegreAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\TumGun\\{} haftaRegre {}-{}-{}-{}-{}-{}.{}-{}.{}.csv".format(hafta,yil, ay, gun, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
    egriDerece = 3
    isVeriyiSuz = True

    #yil = 2017
    #ay = 'Mayis'
    #stringAylar = ['Ocak', 'Subat', 'Mart', 'Nisan', 'Mayis', 'Haziran', 'Temmuz', 'Agustos', 'Eylul', 'Ekim', 'Kasim', 'Aralik']
    #ay = stringAylar[int(ay)-1]
    #vSegDir = 0
    #vSegID = 471
    #gun = 19

    #birgun = sql.SQLBaglanSinif(yil, ay, gun, vSegID, vSegDir)
    #birgun.veriyiSuzVeKaydet(vSegID, vSegDir, gun, birgun.getDakikaAraligi(), ay, adres,yil, cursor)

    oGun = sql.SQLBaglanSinif(yil, vSegID, vSegDir, ay, gun)
    kHaftaRegre = sql.SQLBaglanSinif(yil, vSegID, vSegDir, ay, gun)
    #oGun.veriyiSuzVeKaydet(471, 0, "5", oGun.getDakikaAraligi(), "Mayis", adresMayisoGun, 2017, cursor)
    if isVeriyiSuz==True:
        csvDosyasi = "{}-{}-{}-{}-{}-{}.{}-{}.{}.csv".format(yil, ay, gun, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
        #print("---csv Dosyasi: ", csvDosyasi)
        if csvDosyasi not in os.listdir("C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\TumGun"):
            oGun.veriyiSuzVeKaydet(vSegID, vSegDir, gun, ay, tumGunAdres, yil, cursor, request)

    if isVeriyiSuz == True:
        regCsvDosyasi = "{} haftaRegre {}-{}-{}-{}-{}-{}.{}-{}.{}.csv".format(hafta,yil, ay, gun, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
        if regCsvDosyasi not in os.listdir("C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\TumGun"):
            start = time.time()
            kHaftaRegre.regVerisiniSuzveKaydet2(vSegID, vSegDir, gun, ay, tumGunRegreAdres, hafta, yil, cursor, request)
            end = time.time()
            print("fark: ", end-start)
    # x_dataOGun:     [0,1,2,3 ... 95]
    # y_dataOGun: [32,32,35,40,39, ... 56]  = Gercek Hizlar
    x_dataOGun, y_dataOGun = oGun.y_DataOlustur(tumGunAdres)
    print('ogun: ',x_dataOGun, y_dataOGun)
    # x_dataKHafta:     [0,1,2,3 ... 95]
    # y_dataKHafta: [32,32,35,40,39, ... 56]  = k Haftalik Ortalama Hizlar
    x_dataKHafta, y_dataKHafta = kHaftaRegre.y_DataOlustur(tumGunRegreAdres)
    
    x_dataTrue = []
    # y_dataKHaftaTrue: k Haftalik Ortalama Hizlar
    y_dataKHaftaTrue = []
    # y_dataOGunTrue: Gercek Hizlar
    y_dataOGunTrue = []

    for i in x_dataOGun :
        if(i in x_dataKHafta):
            x_dataTrue.append(i)
            indexr = x_dataKHafta.index(i)
            indexx = x_dataOGun.index(i)
            y_dataOGunTrue.append(y_dataOGun[indexx])
            y_dataKHaftaTrue.append(y_dataKHafta[indexr])

    regsizOrtDataKHafta = y_dataKHaftaTrue

    x_dataTrue05 = []
    x_dataTrueIsGiris = []
    x_dataTrueOgle = []
    x_dataTrueIsCikis = []
    x_dataTrue2024 = []
    y_dataOGunTrue05 = []
    y_dataOGunTrueIsGiris = []
    y_dataOGunTrueOgle = []
    y_dataOGunTrueIsCikis = []
    y_dataOGunTrue2024 = []
    y_dataKHaftaTrue05 = []
    y_dataKHaftaTrueIsGiris = []
    y_dataKHaftaTrueOgle = []
    y_dataKHaftaTrueIsCikis = []
    y_dataKHaftaTrue2024 = []

    ### Gunun hangi saatine denk geliyorsa o listeye atıyoruz ki her biri icin ayri
    ### regresyon egrisi cikartabilelim.
    for i in x_dataTrue:
        if (i>=0) and (i<=19):
            x_dataTrue05.append(i)
            indexx = x_dataTrue.index(i)
            y_dataOGunTrue05.append(y_dataOGunTrue[indexx])
            y_dataKHaftaTrue05.append(y_dataKHaftaTrue[indexx])
        elif (i>=20) and (i<=39):
            x_dataTrueIsGiris.append(i)
            indexx = x_dataTrue.index(i)
            y_dataKHaftaTrueIsGiris.append(y_dataKHaftaTrue[indexx])
        elif (i>=40) and (i<=63):
            x_dataTrueOgle.append(i)
            indexx = x_dataTrue.index(i)
            y_dataKHaftaTrueOgle.append(y_dataKHaftaTrue[indexx])
        elif (i>=64) and (i<=79):
            x_dataTrueIsCikis.append(i)
            indexx = x_dataTrue.index(i)
            y_dataOGunTrueIsCikis.append(y_dataOGunTrue[indexx])
            y_dataKHaftaTrueIsCikis.append(y_dataKHaftaTrue[indexx])
        elif (i>=80) and (i<=95):
            x_dataTrue2024.append(i)
            indexx = x_dataTrue.index(i)
            y_dataOGunTrue2024.append(y_dataOGunTrue[indexx])
            y_dataKHaftaTrue2024.append(y_dataKHaftaTrue[indexx])


    print("----x_dataOGun= "+ str(len(x_dataOGun)) + " x_dataKHafta= " + str(len(x_dataKHafta))+ " x_dataTrue= "+ str(len(x_dataTrue)))
    print("----y_dataOGunTrue= "+ str(len(y_dataOGunTrue))+ " y_dataKHaftaTrue= "+ str(len(y_dataKHaftaTrue)))
    print("----Sensör= "+ str(vSegID) +"\n")
    print("\n-------x_dataOGun--------- \n"+ str(x_dataOGun) +"\n")
    print("\n-------x_dataKHafta--------- \n"+ str(x_dataKHafta) +"\n")
    print("\n-------x_dataTrue----------- \n"+ str(x_dataTrue) +"\n")
    print("\n-------y_dataOGunTrue----------- \n"+ str(y_dataOGunTrue) +"\n")
    print("\n-------RegyDataTrue--------- \n"+ str(y_dataKHaftaTrue) +"\n")


    print("\n-------x_Data05----------- \n"+ str(x_dataTrue05) +"\n")   
    print(" "+ str(len(x_dataTrue05)) +"\n")
    print("\n-------x_DataIsGiris----------- \n"+ str(x_dataTrueIsGiris) +"\n")
    print("\n-------x_DataOgle----------- \n"+ str(x_dataTrueOgle) +"\n")
    print("\n-------x_DataIsCikis----------- \n"+ str(x_dataTrueIsCikis) +"\n")
    print("\n-------x_Data2024----------- \n"+ str(x_dataTrue2024) +"\n")

    ps = []
    ps05 = []
    psIsGiris = []
    psOgle = []
    psIsCikis = []
    ps2024 = []
    k=0
    y_KHaftaRegDataParcali = []
    #y_predsUcuncuCuma, ps = birgun.y_predsle(x_dataOGun, y_dataUcuncuCuma, derece)
    #print(x_dataOGun, y_dataOGun, derece)
    #y_KHaftaRegDataParcali, ps = kHaftaRegre.y_predsle(x_dataTrue, y_dataKHaftaTrue, egriDerece+1)
    if(len(x_dataTrue05) != 0):
        y_KHaftaRegDataParcali05, ps05 = kHaftaRegre.y_predsle(x_dataTrue05, y_dataKHaftaTrue05, egriDerece+1)
        for i in y_KHaftaRegDataParcali05:
            y_KHaftaRegDataParcali.append(i)
        print("-----------05",y_dataKHaftaTrue05,len(y_dataKHaftaTrue05),len(y_KHaftaRegDataParcali05))
        for j in ps05:
            ps.append(j)
    if(len(x_dataTrueIsGiris) != 0):
        y_KHaftaRegDataParcaliIsGiris, psIsGiris = kHaftaRegre.y_predsle(x_dataTrueIsGiris, y_dataKHaftaTrueIsGiris, egriDerece+1)
        for i in y_KHaftaRegDataParcaliIsGiris:
            y_KHaftaRegDataParcali.append(i)
        print("-----------Is Giris",y_dataKHaftaTrueIsGiris,len(y_dataKHaftaTrueIsGiris),len(y_KHaftaRegDataParcaliIsGiris))
        for j in psIsGiris:
            ps.append(j)
    if(len(x_dataTrueOgle) != 0):
        y_KHaftaRegDataParcaliOgle, psOgle = kHaftaRegre.y_predsle(x_dataTrueOgle, y_dataKHaftaTrueOgle, egriDerece+1)
        for i in y_KHaftaRegDataParcaliOgle:
            y_KHaftaRegDataParcali.append(i)
        print("--------Ogle",y_dataKHaftaTrueOgle,len(y_dataKHaftaTrueOgle),len(y_KHaftaRegDataParcaliOgle))
        for j in psOgle:
            ps.append(j)
    if(len(x_dataTrueIsCikis) != 0):    
        y_KHaftaRegDataParcaliIsCikis, psIsCikis = kHaftaRegre.y_predsle(x_dataTrueIsCikis, y_dataKHaftaTrueIsCikis, egriDerece+1)
        for i in y_KHaftaRegDataParcaliIsCikis:
            y_KHaftaRegDataParcali.append(i)
        print("------Is Cikis",y_dataKHaftaTrueIsCikis,len(y_dataKHaftaTrueIsCikis),len(y_KHaftaRegDataParcaliIsCikis))
        for j in psIsCikis:
            ps.append(j)
    if(len(x_dataTrue2024) != 0):    
        y_KHaftaRegDataParcali2024, ps2024 = kHaftaRegre.y_predsle(x_dataTrue2024, y_dataKHaftaTrue2024, egriDerece+1)
        for i in y_KHaftaRegDataParcali2024:
            y_KHaftaRegDataParcali.append(i)
        print("-----2024",y_dataKHaftaTrue2024,len(y_dataKHaftaTrue2024),len(y_KHaftaRegDataParcali2024))
        for j in ps2024:
            ps.append(j)

    print("--------y_KHaftaRegDataParcali ",y_KHaftaRegDataParcali, len(y_KHaftaRegDataParcali))
    print("-------------PS ", ps)

    y_KHaftaRegDataParcasiz = []
    y_KHaftaRegDataParcasiz, ps2 = kHaftaRegre.y_predsle(x_dataTrue, y_dataKHaftaTrue, egriDerece+1)

    
    print("--------y_dataKHaftaTrue ",y_dataKHaftaTrue, len(y_dataKHaftaTrue))
    #x = symbols("x")
    #for a in range(egriDerece):
    #    poly = sum(S("{}".format(v)) * x ** i for i, v in enumerate(ps[a][::-1]))
    ## print("poly: ", poly)
    #eq_latex = sympy.printing.latex(poly)


    #print("7. dereceden denklem icin:")
    """for i in range(10):
        print("{}= ".format(str(i * 10) + "-" + str(10 * (i + 1))), "%", round(
            mean_absolute_error(y_dataUcuncuCuma[10 * i:10 * (i + 1)],
                               (y_predsUcuncuCuma[egriDerece])[10 * i:10 * (i + 1)]), 3), sep="") 
    print()
    for i in range(10):
        print("{}= ".format(str(i * 10) + "-" + str(10 * (i + 1))), "%", round(
            mean_absolute_error(y_dataOGun[10 * i:10 * (i + 1)], (y_KHaftaRegDataParcali[egriDerece])[10 * i:10 * (i + 1)]),
            3), sep="")
    print()"""

    y_dataOGunTrue, y_KHaftaRegDataParcali = np.array(y_dataOGunTrue), np.array(y_KHaftaRegDataParcali)
    kHaftaParcaliRegMAPE = round((np.mean(np.abs((y_dataOGunTrue - y_KHaftaRegDataParcali) / y_dataOGunTrue)) * 100),3)
    
    y_dataOGunTrue, y_KHaftaRegDataParcasiz = np.array(y_dataOGunTrue), np.array(y_KHaftaRegDataParcasiz)
    kHaftaParcasizRegMAPE = round((np.mean(np.abs((y_dataOGunTrue - y_KHaftaRegDataParcasiz) / y_dataOGunTrue)) * 100),3)

    y_dataOGunTrue, y_dataKHaftaTrue = np.array(y_dataOGunTrue), np.array(y_dataKHaftaTrue)
    kHaftaParcasizOrtMAPE = round((np.mean(np.abs((y_dataOGunTrue - y_dataKHaftaTrue) / y_dataOGunTrue)) * 100),3)

    kHaftaParcaliRegMAE = round(mean_absolute_error(y_dataOGunTrue, y_KHaftaRegDataParcali),3)

    tarih = '{}-{}-{} hafta-{}-{}-{}-{}:{}-{}:{}'.format(str(vSegID), vSegDir, hafta, yil, ay, gun,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)

    with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\MAPEveMAEler.txt', 'a') as f:
        f.write('\n'+ int(((20-len(str(kHaftaParcaliRegMAPE)))/2))*' '  +str(kHaftaParcaliRegMAPE)+int(((20-len(str(kHaftaParcaliRegMAPE))+1)/2))*' '+' - '
            +int(((21-len(str(kHaftaParcasizRegMAPE)))/2))*' '  +str(kHaftaParcasizRegMAPE)+int(((21-len(str(kHaftaParcasizRegMAPE))+1)/2))*' '+' - '
            +int(((21-len(str(kHaftaParcasizOrtMAPE)))/2))*' '  +str(kHaftaParcasizOrtMAPE)+int(((21-len(str(kHaftaParcasizOrtMAPE))+1)/2))*' '+' - '
            +int(((19-len(str(kHaftaParcaliRegMAE)))/2))*' '  +str(kHaftaParcaliRegMAE)+int(((19-len(str(kHaftaParcaliRegMAE))+1)/2))*' '+' - '
            +str(tarih)+' ')

    x_dataTrueSaat = []

    for i in x_dataTrue:
        saat = i/4
        x_dataTrueSaat.append(saat)

    # matplotlib.use('Agg')
    #plt.xticks(0,23,4)
    plt.figure(figsize=(6 * 3.3, 4 * 3.3))
    plt.title(r'ParcaliMAPE - ParcasizMAPE - ParcasizOrtMAPE - ParcaliMAE =' r"%{} - %{} - %{} - {}".format(kHaftaParcaliRegMAPE,kHaftaParcasizRegMAPE,kHaftaParcasizOrtMAPE,kHaftaParcaliRegMAE), fontsize=12, color="b")
    ###Secilen gunun hiz degerlerinin noktali hali
    plt.plot(x_dataTrueSaat, y_dataOGunTrue, "o")
    for a,b in zip(x_dataTrueSaat, y_dataOGunTrue):
        plt.text(a,b,str(b))

    ### 3 hafta oncenin ortalama hiz degerlerinin noktali hali
    #plt.plot(x_dataTrueSaat, y_dataKHaftaTrue, "o")
    #for a,b in zip(x_dataTrueSaat, y_dataKHaftaTrue):
    #    plt.text(a,b,round(b,2))

    plt.plot(x_dataTrueSaat, y_KHaftaRegDataParcasiz, "-")

    plt.xlabel("Saatler",fontsize=20)
    plt.ylabel("Hızlar",fontsize=20)
    plt.plot(x_dataTrueSaat, y_KHaftaRegDataParcali, "-")
    plt.legend(['SecilenGünVerisi', 'Parçalanmamış Regresyon Eğrisi', 'Parçalanmış Regresyon Eğrisi'], loc='best', prop={'size':15})

    resimAdresDeneme = "C:\\Users\\ibrahim\\Desktop\\trafSite\\static\\images\\{}-{}-{}-{}-{}-{}.{}-{}.{}.png".format(yil, ay, gun, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
    plt.savefig(resimAdresDeneme)
    print("----degerleriAl fonksiyonuna çıkıldı!!")
    return

def haritadanEnYakinSensorBul(request):
    print("----haritadanEnYakinSensorBul fonksiyonuna girildi!!")
    secilenX = float(request.POST.get('lat'))
    secilenY = float(request.POST.get('lng'))
    farklarList = []

    ### KML dosyasini ac
    ### [[ID, yKoor, xKoor, ?], [ID, yKoor, xKoor, ?]...]
    with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\vSegIDlerVeKoordinatlar.csv', 'rb') as fp:
        vSegIDlerVeKoordinatlar = pickle.load(fp)

    ### KML dosyasindaki X ve Y koordinatina gore secilenX ve secilenY'ye en yakin sensoru bul
    #print("--*-**-*: ", vSegIDlerVeKoordinatlar[0][1], secilenY)
    for vSegIDVeKoordinat in vSegIDlerVeKoordinatlar:
        xFark = float(vSegIDVeKoordinat[2])**2 - secilenX**2
        yFark = float(vSegIDVeKoordinat[1])**2 - secilenY**2
        toplamFark = abs(xFark)+abs(yFark)
        farklarList.append(toplamFark)
    indx = farklarList.index(min(farklarList))
    return vSegIDlerVeKoordinatlar[indx][0]

def haritadanEnYakinSensorBulLatLong(lat, lng):
    print("----haritadanEnYakinSensorBul fonksiyonuna girildi!!")
    secilenX = float(lat)
    secilenY = float(lng)
    farklarList = []

    ### KML dosyasini ac
    ### [[ID, yKoor, xKoor, ?], [ID, yKoor, xKoor, ?]...]
    with open('C:\\Users\\ibrahim\\Desktop\\trafSite\\vSegIDlerVeKoordinatlar.csv', 'rb') as fp:
        vSegIDlerVeKoordinatlar = pickle.load(fp)

    ### KML dosyasindaki X ve Y koordinatina gore secilenX ve secilenY'ye en yakin sensoru bul
    #print("--*-**-*: ", vSegIDlerVeKoordinatlar[0][1], secilenY)
    for vSegIDVeKoordinat in vSegIDlerVeKoordinatlar:
        xFark = float(vSegIDVeKoordinat[2])**2 - secilenX**2
        yFark = float(vSegIDVeKoordinat[1])**2 - secilenY**2
        toplamFark = abs(xFark)+abs(yFark)
        farklarList.append(toplamFark)
    indx = farklarList.index(min(farklarList))
    return vSegIDlerVeKoordinatlar[indx][0], vSegIDlerVeKoordinatlar[indx][1], vSegIDlerVeKoordinatlar[indx][2]

def koordanEnYakinHavaDurumuSemtiBulMy(lat, lng):
    birSeferlik = sql.SQLBaglanSinif(1, 1, 1, 1, 1)
    enYakinHDSA = birSeferlik.koordanEnYakinHavaDurumuSemtiBul(lat, lng)
    return enYakinHDSA


def aylikOrtHizBul(cursor, lat, lng, vSegDir):
    yil = 2017
    cikarilacakAySayisi = 4
    vSegID = haritadanEnYakinSensorBulLatLong(lat, lng)[0]
    #print("-----------: " ,vSegID)
    ortHiz = sql.SQLBaglanSinif(yil, vSegID, vSegDir)
    hata = ortHiz.dolulukKontrolEt(vSegID, vSegDir, cikarilacakAySayisi)
    dosyaYolu = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\Aylik\\2017-5-1-SensorlerinAylikDolulukOranlari.pickle'
    print("3, ", hata)
    if (hata==True):
        return 'error', 'error', 'error', 'error'
    resimAdresi = ortHiz.aylikOrtHizBul(yil, vSegID, vSegDir, cursor)
    return resimAdresi, lat, lng, vSegID

def havaDurumu(request, cursor, ufakYagisListListesi, havaOlayliGunler):
    vSegDir = request.POST.get('HavaDurumuvSegDir')
    tarihParcalanacakString1 = request.POST.get('datepickerHavaDurumu1')
    tarihParcalanmisListe1 = tarihParcalanacakString1.split('/')
    yil1 = tarihParcalanmisListe1[2]
    ay1 = tarihParcalanmisListe1[1]
    if (ay1[0]=="0"):
        ay1 = ay1.replace("0", "")
    gun1 = tarihParcalanmisListe1[0]

    tarihParcalanacakString2 = request.POST.get('datepickerHavaDurumu2')
    tarihParcalanmisListe2 = tarihParcalanacakString2.split('/')
    yil2 =tarihParcalanmisListe2[2]
    ay2 = tarihParcalanmisListe2[1]
    if (ay2[0]=="0"):
        ay2 = ay2.replace("0", "")
    gun2 = tarihParcalanmisListe2[0]

    lat, lng = request.POST.get('latHava'), request.POST.get('lngHava')


    vSegID, enYakinSensorY, enYakinSensorX = haritadanEnYakinSensorBulLatLong(lat, lng)
    print("---vSegID: ", vSegID)

    hava = sql.SQLBaglanSinif(yil1, vSegID, vSegDir)

    ### havaOlayliDegerler = [ [vSegID, semt, yil, ay, gun, saat, miktar], [vSegID, semt, yil, ay, gun, saat, miktar], ... ]
    #havaOlayliDegerler, distinctHavaOlayiYasananDegerler = hava.havaOlayindanAyVeGunBulYagmur(havaOlayi, secilenSemt)
    ### havaOlaysizDegerler = [Istasyon_No, Istasyon_Adi, YIL, AY, GUN, Yagis]
    #havaOlaysizDegerler = hava.havaOlaysizAyVeGunBulYagmur(havaOlayliDegerler, secilenSemt)
    print("+++++++++++++")
    #print(havaOlaysizDegerler)
    
    #if (havaOlaysizDegerler!=False):
    ### yagis olmayan 1 hafta onceki degerler
    #havaOlaysizSemt, yil, oncekiAy, oncekiGun = havaOlaysizDegerler[1], havaOlaysizDegerler[2], havaOlaysizDegerler[3], havaOlaysizDegerler[4]
    start = time.time()
    hava.gunVeSensorVerCiktiAl(cursor, yil1, ay1, gun1, vSegID, vSegDir)
    end = time.time()
    print("ilk sorgu: ", end- start)
    start = time.time()
    hava.gunVeSensorVerCiktiAl(cursor, yil2, ay2, gun2, vSegID, vSegDir)
    end = time.time()
    print("ikinci sorgu: ", end- start)
    
    resimAdresi = hava.havaOlayiResimCikar(yil1, ay1, gun1, ay2, gun2, vSegID, vSegDir, ufakYagisListListesi, havaOlayliGunler)
    return resimAdresi

def havaDurumuAjax(cursor, secilenSemt):
    vSegDir = 0
    yil = 2017
    havaOlayi = 'Yağmur'
    print("------------------------------------: ", secilenSemt)

    if (secilenSemt == 'Üsküdar'):
        print('Üsküdardayız')
        vSegID = 404
    elif (secilenSemt == 'Kadıköy'):
        print('Kadıköydeyiz')
        vSegID = 10

    elif secilenSemt=='Şişli':
        print('Şişlideyiz')
        vSegID = 404

    elif secilenSemt=='Ümraniye':
        print('Ümraniyedeyiz')
        vSegID = 404

    hava = sql.SQLBaglanSinif(yil, vSegID, vSegDir)

    havaOlayliDegerler, distinctHavaOlayiYasananDegerler, ufakYagisListListesi = hava.havaOlayindanAyVeGunBulYagmur(secilenSemt)

    return distinctHavaOlayiYasananDegerler, ufakYagisListListesi


    #if (havaOlayi=='Yağmur'):
        ### havaOlayliDegerler = [ [vSegID, semt, yil, ay, gun, saat, miktar], [vSegID, semt, yil, ay, gun, saat, miktar], ... ]
        #havaOlayliDegerler, distinctHavaOlayiYasananDegerler = hava.havaOlayindanAyVeGunBulYagmur(havaOlayi, secilenSemt)
        #print(distinctHavaOlayiYasananDegerler)
        #return distinctHavaOlayiYasananDegerler
        ### havaOlaysizDegerler = [Istasyon_No, Istasyon_Adi, YIL, AY, GUN, Yagis]
        #havaOlaysizDegerler = hava.havaOlaysizAyVeGunBulYagmur(havaOlayliDegerler, secilenSemt)
        #print("+++++++++++++")
        #print(havaOlaysizDegerler)
        #
        #if (havaOlaysizDegerler!=False):
        #    ### yagis olmayan 1 hafta onceki degerler
        #    havaOlaysizSemt, yil, oncekiAy, oncekiGun = havaOlaysizDegerler[1], havaOlaysizDegerler[2], havaOlaysizDegerler[3], havaOlaysizDegerler[4]
        #    hava.gunVeSensorVerCiktiAl(cursor, yil, oncekiAy, oncekiGun, vSegID, vSegDir, havaOlaysizSemt, olay='yagmursuz')
        #    
        #    oGun = datetime(yil, oncekiAy, oncekiGun)
        #    ### yagisin oldugu gun ve ay
        #    sonraki1Hafta = oGun + timedelta(days=7)
        #    sonrakiAy = int(sonraki1Hafta.strftime('%m'))
        #    sonrakiGun = int(sonraki1Hafta.strftime('%d'))
        #    hava.gunVeSensorVerCiktiAl(cursor, yil, sonrakiAy, sonrakiGun, vSegID, vSegDir, havaOlaysizSemt, olay='yagmurlu')
        #    
        #    #resimAdresi = hava.havaOlayiResimCikar(havaOlaysizSemt, yil, oncekiAy, oncekiGun, sonrakiAy, sonrakiGun, havaOlayi)
        #    return distinctHavaOlayiYasananDegerler