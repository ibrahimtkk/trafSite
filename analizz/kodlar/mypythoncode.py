from . import SQLeBaglanKarma as sql
from sklearn.metrics import mean_squared_error, mean_absolute_error
import pyodbc
import matplotlib.pyplot as plt
import matplotlib
from sympy import S, symbols
import sympy
import numpy as np


def degerleriAl(request, cursor):
    yil = request.POST.get('year')
    ay = request.POST.get('month')
    vSegDir = request.POST.get('vSegDir')
    vSegID = request.POST.get('sensor')
    ayinKaci = request.POST.get('day')
    adres = "C:\\Users\\ibrahim\\djangoboys\\CSV\\MayisUcuncuCuma2017.csv"
    adresMayisIlkCuma = "C:\\Users\\ibrahim\\djangoboys\\CSV\\MayisIlkCuma2017.csv"
    derece = 11
    derece7 = 7

    yil = 2017
    ay = 'Mayis'
    vSegDir = 0
    vSegID = 471
    ayinKaci = 19

    birgun = sql.SQLBaglanSinif(yil, ay, ayinKaci, vSegID, vSegDir)
    birgun.veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, birgun.getDakikaAraligi(), ay, adres,yil, cursor)

    ilkCuma = sql.SQLBaglanSinif(yil, ay, ayinKaci, vSegID, vSegDir)
    ilkCuma.veriyiSuzVeKaydet(471, 0, "5", ilkCuma.getDakikaAraligi(), "Mayis", adresMayisIlkCuma, 2017, cursor)

    x_data, y_dataUcuncuCuma = birgun.y_DataOlustur(adres, derece, derece7)
    x_data, y_dataIlkCuma = ilkCuma.y_DataOlustur(adresMayisIlkCuma, derece, derece7)

    ps = []
    y_predsUcuncuCuma, ps = birgun.y_predsle(x_data, y_dataUcuncuCuma, derece)
    y_predsIlkCuma, ps = ilkCuma.y_predsle(x_data, y_dataIlkCuma, derece)

    x = symbols("x")
    for a in range(derece7):
        poly = sum(S("{}".format(v)) * x ** i for i, v in enumerate(ps[a][::-1]))
    # print("poly: ", poly)
    eq_latex = sympy.printing.latex(poly)

    print("7. dereceden denklem icin:")
    for i in range(10):
        print("{}= ".format(str(i * 10) + "-" + str(10 * (i + 1))), "%", round(
            mean_absolute_error(y_dataUcuncuCuma[10 * i:10 * (i + 1)],
                                (y_predsUcuncuCuma[derece7])[10 * i:10 * (i + 1)]), 3), sep="")
    print()
    for i in range(10):
        print("{}= ".format(str(i * 10) + "-" + str(10 * (i + 1))), "%", round(
            mean_absolute_error(y_dataIlkCuma[10 * i:10 * (i + 1)], (y_predsUcuncuCuma[derece7])[10 * i:10 * (i + 1)]),
            3), sep="")
    print()

    # matplotlib.use('Agg')
    plt.figure(figsize=(6 * 3.3, 4 * 3.3))
    plt.title(r'Eq =' r"${}$".format(eq_latex), fontsize=12, color="r")
    plt.plot(x_data, y_dataUcuncuCuma, "o")
    plt.plot(x_data, y_predsUcuncuCuma[derece7], "-")
    plt.plot(x_data, y_predsIlkCuma[derece7], "-")
    plt.legend(['data', '3.Cuma', 'MayisIlkCuma'], loc='best')

    resimAdresDeneme = "C:\\Users\\ibrahim\\djangoboys\\CSV\\MayisUcuncuCuma2017.png"
    plt.savefig(resimAdresDeneme)
    return