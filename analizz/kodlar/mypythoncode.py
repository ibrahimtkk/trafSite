from . import SQLeBaglanKarma as sql
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pyodbc
import matplotlib.pyplot as plt
import matplotlib
from sympy import S, symbols
import sympy
import numpy as np
import os


def degerleriAl(request, cursor):
    tarihParcalanacakString = request.POST.get('datepicker1')
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    vSegDir = request.POST.get('vSegDirTumGun')
    vSegID = request.POST.get('vSegIDTumGun')
    yil =tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[0]
    print("ay: ", ay)
    if (ay[0]=="0"):
        ay = ay.replace("0", "")
    ayinKaci = tarihParcalanmisListe[1]
    print("---", yil, ay, ayinKaci)
    adres = "C:\\Users\\ibrahim\\djangoboys\\CSV1\\MayisUcuncuCuma2017.csv"
    tumGunAdres = "C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\TumGun\\{}-{}-{}-{}-{}.csv".format(yil, ay, ayinKaci, vSegID, vSegDir)
    derece = 11
    derece7 = 7
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
    #ilkCuma.veriyiSuzVeKaydet(471, 0, "5", ilkCuma.getDakikaAraligi(), "Mayis", adresMayisIlkCuma, 2017, cursor)
    if isVeriyiSuz==True:
        csvDosyasi = "{}-{}-{}-{}-{}.csv".format(yil, ay, ayinKaci, vSegID, vSegDir)
        if csvDosyasi not in os.listdir("C:\\Users\\ibrahim\\Desktop\\trafSite\\CSV\\analiz\\TumGun"):
            ilkCuma.veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, ay, tumGunAdres, yil, cursor)

    #x_data, y_dataUcuncuCuma = birgun.y_DataOlustur(adres, derece, derece7)
    x_data, y_dataIlkCuma = ilkCuma.y_DataOlustur(tumGunAdres, derece, derece7)

    ps = []
    #y_predsUcuncuCuma, ps = birgun.y_predsle(x_data, y_dataUcuncuCuma, derece)
    y_predsIlkCuma, ps = ilkCuma.y_predsle(x_data, y_dataIlkCuma, derece)

    x = symbols("x")
    for a in range(derece7):
        poly = sum(S("{}".format(v)) * x ** i for i, v in enumerate(ps[a][::-1]))
    # print("poly: ", poly)
    eq_latex = sympy.printing.latex(poly)

    print("7. dereceden denklem icin:")
    """for i in range(10):
        print("{}= ".format(str(i * 10) + "-" + str(10 * (i + 1))), "%", round(
            mean_absolute_error(y_dataUcuncuCuma[10 * i:10 * (i + 1)],
                                (y_predsUcuncuCuma[derece7])[10 * i:10 * (i + 1)]), 3), sep="")
    print()
    for i in range(10):
        print("{}= ".format(str(i * 10) + "-" + str(10 * (i + 1))), "%", round(
            mean_absolute_error(y_dataIlkCuma[10 * i:10 * (i + 1)], (y_predsUcuncuCuma[derece7])[10 * i:10 * (i + 1)]),
            3), sep="")
    print()
    """

    # matplotlib.use('Agg')
    plt.figure(figsize=(6 * 3.3, 4 * 3.3))
    plt.title(r'Eq =' r"${}$".format(eq_latex), fontsize=12, color="r")
    plt.plot(x_data, y_dataIlkCuma, "o")
    #plt.plot(x_data, y_predsUcuncuCuma[derece7], "-")
    plt.plot(x_data, y_predsIlkCuma[derece7], "-")
    plt.legend(['data', 'regresyonEğrisi'], loc='best')

    resimAdresDeneme = "C:\\Users\\ibrahim\\Desktop\\trafSite\\static\\images\\{}-{}-{}-{}-{}.png".format(yil, ay, ayinKaci, vSegID, vSegDir)
    plt.savefig(resimAdresDeneme)
    return