from . import SQLeBaglanKarma as sql
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pyodbc
import matplotlib.pyplot as plt
import matplotlib
from sympy import S, symbols
from sklearn.utils import check_array
import sympy
import numpy as np
import os
import pickle


def degerleriAl(request, cursor, vSegID, basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika):
    print("----degerleriAl fonksiyonuna girildi!!")
    tarihParcalanacakString = request.POST.get('datepicker1')
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    vSegDir = request.POST.get('vSegDirTumGun')
    yil =tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[1]
    hafta = 3
    #print("ay: ", ay)
    if (ay[0]=="0"):
        ay = ay.replace("0", "")
    ayinKaci = tarihParcalanmisListe[0]
    #print("---", yil, ay, ayinKaci)
    #adres = "C:\\Users\\ASUS\\djangoboys\\CSV1\\MayisUcuncuCuma2017.csv"
    tumGunAdres = "C:\\Users\\ASUS\\Desktop\\trafSite\\CSV\\analiz\\TumGun\\{}-{}-{}-{}-{}-{}.{}-{}.{}.csv".format(yil, ay, ayinKaci, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
    tumGunRegreAdres = "C:\\Users\\ASUS\\Desktop\\trafSite\\CSV\\analiz\\TumGun\\{} haftaRegre {}-{}-{}-{}-{}-{}.{}-{}.{}.csv".format(hafta,yil, ay, ayinKaci, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
    egriDerece = 3
    isVeriyiSuz = True

    #yil = 2017
    #ay = 'Mayis'
    #stringAylar = ['Ocak', 'Subat', 'Mart', 'Nisan', 'Mayis', 'Haziran', 'Temmuz', 'Agustos', 'Eylul', 'Ekim', 'Kasim', 'Aralik']
    #ay = stringAylar[int(ay)-1]
    #vSegDir = 0
    #vSegID = 471
    #ayinKaci = 19

    #birgun = sql.SQLBaglanSinif(yil, ay, ayinKaci, vSegID, vSegDir)
    #birgun.veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, birgun.getDakikaAraligi(), ay, adres,yil, cursor)

    ilkCuma = sql.SQLBaglanSinif(yil, ay, ayinKaci, vSegID, vSegDir)
    kHaftaRegre = sql.SQLBaglanSinif(yil, ay, ayinKaci, vSegID, vSegDir)
    #ilkCuma.veriyiSuzVeKaydet(471, 0, "5", ilkCuma.getDakikaAraligi(), "Mayis", adresMayisIlkCuma, 2017, cursor)
    if isVeriyiSuz==True:
        csvDosyasi = "{}-{}-{}-{}-{}-{}.{}-{}.{}.csv".format(yil, ay, ayinKaci, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
        #print("---csv Dosyasi: ", csvDosyasi)
        if csvDosyasi not in os.listdir("C:\\Users\\ASUS\\Desktop\\trafSite\\CSV\\analiz\\TumGun"):
            ilkCuma.veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, ay, tumGunAdres, yil, cursor, request)

    if isVeriyiSuz == True:
        regCsvDosyasi = "{} haftaRegre {}-{}-{}-{}-{}-{}.{}-{}.{}.csv".format(hafta,yil, ay, ayinKaci, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
        if regCsvDosyasi not in os.listdir("C:\\Users\\ASUS\\Desktop\\trafSite\\CSV\\analiz\\TumGun"):
            kHaftaRegre.regVerisiniSuzveKaydet(vSegID, vSegDir, ayinKaci, ay, tumGunRegreAdres, hafta, yil, cursor, request)

    #x_data, y_dataUcuncuCuma = birgun.y_DataOlustur(adres, derece, egriDerece)
    x_data, y_dataIlkCuma = ilkCuma.y_DataOlustur(tumGunAdres)
    regx_data, regy_data = kHaftaRegre.y_DataOlustur(tumGunRegreAdres)
    
    x_dataTrue = []
    regy_dataTrue = []
    y_dataIlkCumaTrue = []

    for i in x_data :
        if(i in regx_data):
            x_dataTrue.append(i)
            indexr = regx_data.index(i)
            indexx = x_data.index(i)
            y_dataIlkCumaTrue.append(y_dataIlkCuma[indexx])
            regy_dataTrue.append(regy_data[indexr])



    x_dataTrue05 = []
    x_dataTrueIsGiris = []
    x_dataTrueOgle = []
    x_dataTrueIsCikis = []
    x_dataTrue2024 = []
    y_dataIlkCumaTrue05 = []
    y_dataIlkCumaTrueIsGiris = []
    y_dataIlkCumaTrueOgle = []
    y_dataIlkCumaTrueIsCikis = []
    y_dataIlkCumaTrue2024 = []
    regy_dataTrue05 = []
    regy_dataTrueIsGiris = []
    regy_dataTrueOgle = []
    regy_dataTrueIsCikis = []
    regy_dataTrue2024 = []

        
    for i in x_dataTrue:
        if (i>=0) and (i<=19):
            x_dataTrue05.append(i)
            indexx = x_dataTrue.index(i)
            y_dataIlkCumaTrue05.append(y_dataIlkCumaTrue[indexx])
            regy_dataTrue05.append(regy_dataTrue[indexx])
        elif (i>=20) and (i<=39):
            x_dataTrueIsGiris.append(i)
            indexx = x_dataTrue.index(i)
            y_dataIlkCumaTrueIsGiris.append(y_dataIlkCumaTrue[indexx])
            regy_dataTrueIsGiris.append(regy_dataTrue[indexx])
        elif (i>=40) and (i<=63):
            x_dataTrueOgle.append(i)
            indexx = x_dataTrue.index(i)
            y_dataIlkCumaTrueOgle.append(y_dataIlkCumaTrue[indexx])
            regy_dataTrueOgle.append(regy_dataTrue[indexx])
        elif (i>=64) and (i<=79):
            x_dataTrueIsCikis.append(i)
            indexx = x_dataTrue.index(i)
            y_dataIlkCumaTrueIsCikis.append(y_dataIlkCumaTrue[indexx])
            regy_dataTrueIsCikis.append(regy_dataTrue[indexx])
        elif (i>=80) and (i<=95):
            x_dataTrue2024.append(i)
            indexx = x_dataTrue.index(i)
            y_dataIlkCumaTrue2024.append(y_dataIlkCumaTrue[indexx])
            regy_dataTrue2024.append(regy_dataTrue[indexx])


    print("----x_data= "+ str(len(x_data)) + " regx_data= " + str(len(regx_data))+ " x_dataTrue= "+ str(len(x_dataTrue)))
    print("----y_dataIlkCumaTrue= "+ str(len(y_dataIlkCumaTrue))+ " regy_dataTrue= "+ str(len(regy_dataTrue)))
    print("----Sensör= "+ str(vSegID) +"\n")
    print("\n-------x_data--------- \n"+ str(x_data) +"\n")
    print("\n-------regx_data--------- \n"+ str(regx_data) +"\n")
    print("\n-------x_dataTrue----------- \n"+ str(x_dataTrue) +"\n")
    print("\n-------y_dataIlkCumaTrue----------- \n"+ str(y_dataIlkCumaTrue) +"\n")
    print("\n-------RegyDataTrue--------- \n"+ str(regy_dataTrue) +"\n")


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
    y_predsRegData = []
    #y_predsUcuncuCuma, ps = birgun.y_predsle(x_data, y_dataUcuncuCuma, derece)
    #print(x_data, y_dataIlkCuma, derece)
    #y_predsRegData, ps = kHaftaRegre.y_predsle(x_dataTrue, regy_dataTrue, egriDerece+1)
    if(len(x_dataTrue05) != 0):
        y_predsRegData05, ps05 = kHaftaRegre.y_predsle(x_dataTrue05, regy_dataTrue05, egriDerece+1)
        for i in y_predsRegData05:
            y_predsRegData.append(i)
        print("-----------05",regy_dataTrue05,len(regy_dataTrue05),len(y_predsRegData05))
        for j in ps05:
            ps.append(j)
    if(len(x_dataTrueIsGiris) != 0):
        y_predsRegDataIsGiris, psIsGiris = kHaftaRegre.y_predsle(x_dataTrueIsGiris, regy_dataTrueIsGiris, egriDerece+1)
        for i in y_predsRegDataIsGiris:
            y_predsRegData.append(i)
        print("-----------Is Giris",regy_dataTrueIsGiris,len(regy_dataTrueIsGiris),len(y_predsRegDataIsGiris))
        for j in psIsGiris:
            ps.append(j)
    if(len(x_dataTrueOgle) != 0):
        y_predsRegDataOgle, psOgle = kHaftaRegre.y_predsle(x_dataTrueOgle, regy_dataTrueOgle, egriDerece+1)
        for i in y_predsRegDataOgle:
            y_predsRegData.append(i)
        print("--------Ogle",regy_dataTrueOgle,len(regy_dataTrueOgle),len(y_predsRegDataOgle))
        for j in psOgle:
            ps.append(j)
    if(len(x_dataTrueIsCikis) != 0):    
        y_predsRegDataIsCikis, psIsCikis = kHaftaRegre.y_predsle(x_dataTrueIsCikis, regy_dataTrueIsCikis, egriDerece+1)
        for i in y_predsRegDataIsCikis:
            y_predsRegData.append(i)
        print("------Is Cikis",regy_dataTrueIsCikis,len(regy_dataTrueIsCikis),len(y_predsRegDataIsCikis))
        for j in psIsCikis:
            ps.append(j)
    if(len(x_dataTrue2024) != 0):    
        y_predsRegData2024, ps2024 = kHaftaRegre.y_predsle(x_dataTrue2024, regy_dataTrue2024, egriDerece+1)
        for i in y_predsRegData2024:
            y_predsRegData.append(i)
        print("-----2024",regy_dataTrue2024,len(regy_dataTrue2024),len(y_predsRegData2024))
        for j in ps2024:
            ps.append(j)

    print("--------y_predsRegData ",y_predsRegData, len(y_predsRegData))
    print("-------------PS ", ps)
    
    regy_dataTrueGun = []
    regy_dataTrueGun, ps2 = kHaftaRegre.y_predsle(x_dataTrue, regy_dataTrue, egriDerece+1)

    
    print("--------regy_dataTrue ",regy_dataTrue, len(regy_dataTrue))
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
            mean_absolute_error(y_dataIlkCuma[10 * i:10 * (i + 1)], (y_predsRegData[egriDerece])[10 * i:10 * (i + 1)]),
            3), sep="")
    print()"""

    mape = []
    #mape.append(str(round(np.mean(np.abs((y_dataIlkCuma - y_predsRegData) / y_dataIlkCuma)) * 100),3))
    

    y_dataIlkCumaTrue, y_predsRegData = np.array(y_dataIlkCumaTrue), np.array(y_predsRegData)
    mape.append(round((np.mean(np.abs((y_dataIlkCumaTrue - y_predsRegData) / y_dataIlkCumaTrue)) * 100),3))
    #print("----MAPE = "+ str(mape))
    mape2 = []
    #mape.append(str(round(np.mean(np.abs((y_dataIlkCuma - y_predsRegData) / y_dataIlkCuma)) * 100),3))
    

    y_dataIlkCumaTrue, regy_dataTrueGun = np.array(y_dataIlkCumaTrue), np.array(regy_dataTrueGun)
    mape2.append(round((np.mean(np.abs((y_dataIlkCumaTrue - regy_dataTrueGun) / y_dataIlkCumaTrue)) * 100),3))

    mae = []
    
    mae.append( round(mean_absolute_error(y_dataIlkCumaTrue, y_predsRegData),3))

    mape2 = mape2[0]
    mape = mape[0]
    mae = mae[0]
    

    x_dataTrueSaat = []

    for i in x_dataTrue:
        saat = i/4
        x_dataTrueSaat.append(saat)

    # matplotlib.use('Agg')
    plt.figure(figsize=(6 * 3.3, 4 * 3.3))
    plt.title(r'ParcaliMAPE - BütünGünMAPE - ParcaliMAE =' r"%{} - %{} - {}".format(mape,mape2,mae), fontsize=12, color="b")
    ###Secilen gunun hiz degerlerinin noktali hali
    plt.plot(x_dataTrueSaat, y_dataIlkCumaTrue, "o")
    for a,b in zip(x_dataTrueSaat, y_dataIlkCumaTrue):
        plt.text(a,b,str(b))

    ### 3 hafta oncenin ortalama hiz degerlerinin noktali hali
    #plt.plot(x_dataTrueSaat, regy_dataTrue, "o")
    #for a,b in zip(x_dataTrueSaat, regy_dataTrue):
    #    plt.text(a,b,round(b,2))

    plt.plot(x_dataTrueSaat, regy_dataTrueGun, "-")

    plt.xlabel("Saatler",fontsize=20)
    plt.ylabel("Hızlar",fontsize=20)
    plt.plot(x_dataTrueSaat, y_predsRegData, "-")
    plt.legend(['SecilenGünVerisi', 'Parçalanmamış Regresyon Eğrisi', 'Parçalanmış Regresyon Eğrisi'], loc='best')

    resimAdresDeneme = "C:\\Users\\ASUS\\Desktop\\trafSite\\static\\images\\{}-{}-{}-{}-{}-{}.{}-{}.{}.png".format(yil, ay, ayinKaci, str(vSegID), vSegDir,basSaatSaat, basSaatDakika, bitSaatSaat, bitSaatDakika)
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
    with open('C:\\Users\\ASUS\\Desktop\\trafSite\\vSegIDlerVeKoordinatlar.csv', 'rb') as fp:
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


    ### Bulunan sensoru dondur