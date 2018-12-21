# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 13:23:37 2018

@author: ibrahim
"""
import pyodbc
import matplotlib.pyplot as plt
from sympy import S, symbols
import sympy
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error
import time


class SQLBaglanSinif():
    print("hela////////////////////////////////////")
    derece = 11
    derece7 = 7
    vSegID = 471
    vSegDir = 0
    ay = 'Mayis'
    suzsunMu = False
    yil = 2017
    dakikaAraligiList = [0, 15, 30, 45]
    ayinKaciList = [19]

    # ayinKaci = self.ayinKaciDuzenle(ayinKaciList)

    def __init__(self, yil, ay, ayinKaci, vSegID, vSegDir):
        self.vSegID = vSegID
        self.vSegDir = vSegDir
        self.ay = ay
        self.yil = yil
        self.ayinKaci = ayinKaci

    def setVSegID(self, vSegID):
        self.vSegID = vSegID

    def setVSegDir(self, vSegDir):
        self.vSegDir = vSegDir

    def setAy(self, ay):
        self.ay = ay

    def setYil(self, yil):
        self.yil = yil

    def getVSegID(self):
        return self.vSegID

    def getVSegDir(self):
        return self.vSegDir

    def getAy(self):
        return self.ay

    def getYil(self):
        return self.yil

    def getDakikaAraligi(self):
        dakikaAraligi = self.dakikaAraligiDuzenle(self.dakikaAraligiList)
        return dakikaAraligi

    def duzenle(self, saat, hiz):
        ayri = ()
        ayri2 = ()
        # print("saat: ",saat)
        for i in hiz:
            j = hiz.index(i)
            i = i.strip("\n")
            i = float(i.replace(",", "."))
            hiz[j] = i
        for i in range(len(saat)):
            ayri = saat[i].split(':')
            mini = int(ayri[0])
            miniIndex = i
            for j in range(i + 1, len(saat)):
                ayri2 = saat[j].split(':')
                if (int(ayri2[0]) < mini):
                    miniIndex = j
                    mini = int(ayri2[0])
            saat[i], saat[miniIndex] = saat[miniIndex], saat[i]
            hiz[i], hiz[miniIndex] = hiz[miniIndex], hiz[i]
        for i in saat:
            ayri = i.split(":")
            if len(ayri[0]) == 1:
                j = saat.index(i)
                i = "0" + i
                saat[j] = i

    def veriyiSuzVeKaydet(self, vSegID, vSegDir, ayinKaci, ay, adres, yil, cursor):

        # cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
        #                       "SERVER=IBRAHIM;"
        #                       "Database=FusedData-2016-2017-2018;"
        #                       "Trusted_Connection=yes;")
        # cursor = cnxn.cursor()

        start = time.time()
        komut = (
            "SELECT convert(varchar(3), datepart(hh, fusedDate))+':'+convert(varchar(3), datepart(mi, fusedDate)), avg(cast(fusedSpeed as money))"
            " FROM [FusedData-2016-2017-2018].dbo.[{}-{}-{}] WHERE vSegID={} and"
            " datepart(dd, fusedDate)={} "
            " group by datepart(hh, fusedDate), datepart(mi, fusedDate)"
            " order by datepart(hh, fusedDate), DATEPART(mi, fusedDate)".format(yil, ay, vSegDir, vSegID, ayinKaci)
            )
        cursor.execute(komut)
        end = time.time()
        print("****************fark: ", end-start)

        # csv dosyalarini kaydettik
        # =====================================================================
        with open(adres, "w") as yaz:
            for row in cursor:
                satir = row[0] + ";"
                satir += str(row[1])
                satir += "\n"
                yaz.write(satir)
        return

    def ayinKaciDuzenle(self, ayinKaciList):
        ayinKaci = ""
        for i in ayinKaciList:
            ayinKaci += str(i)
            ayinKaci += ','
        ayinKaci = ayinKaci[:-1]
        return ayinKaci

    def dakikaAraligiDuzenle(self, dakikaAraligiList):
        dakikaAraligi = ""
        for i in dakikaAraligiList:
            dakikaAraligi += str(i)
            dakikaAraligi += ','
        dakikaAraligi = dakikaAraligi[:-1]
        return dakikaAraligi

    # csv dosyasindaki 2 kolonu noktali virgunden temizleyip ayri dizilere atiyor.
    def noktaliVirguldenTemizle(self, adres, derece):
        liste = []
        gunlerSaat = [[] for _ in range(derece)]
        gunlerHiz = [[] for _ in range(derece)]

        with open(adres, encoding='utf-8-sig') as myfile:
            for line in myfile:
                liste = line.split(";")
                gunlerSaat[0].append(liste[0])  # saat
                gunlerHiz[0].append(liste[1])  # hiz

        for a in range(7):
            self.duzenle(gunlerSaat[a], gunlerHiz[a])

        return gunlerSaat, gunlerHiz

    # 00:00 0. indis olacak sekilde saat ve dakikalari x eksenine indis olarak
    # atiyor.
    def saatiIndisYap(self, gunlerSaat):
        indisler = []
        for i in gunlerSaat[0]:
            virg = i.index(":")
            saat = int(i[:virg])
            dakika = int(i[virg + 1:])
            indisler.append(saat * 4 + dakika / 15)
        return indisler

    def y_DataOlustur(self, CSVadres, derece, derece7):
        gunlerSaat = [[] for _ in range(derece)]
        gunlerHiz = [[] for _ in range(derece)]
        gunlerSaat, gunlerHiz = self.noktaliVirguldenTemizle(CSVadres, derece7)
        x_data = self.saatiIndisYap(gunlerSaat)  # x_dattaki degerleri indisleyen degerler
        y_data = gunlerHiz[0]

        return x_data, y_data

    def fitle(self, x_data, y_data, derece):
        # verilen derecesine gore grafigi fitleyen fonksiyon
        ps = []
        for i in range(derece):
            ps.append(np.polyfit(x_data, y_data, i))
        return ps

    def polyvalla(self, ps, x_data, derece):
        y_preds = []
        # polinomsal degerleri hesaplar. polyval() fonksiyonu degisken olarak array
        # girdigimiz icin bize bir array dondurur.
        for i in range(derece):
            y_preds.append(np.polyval(ps[i], x_data))
        return y_preds

    def y_predsle(self, x_data, y_data, derece):
        ps = self.fitle(x_data, y_data, derece)
        y_preds = self.polyvalla(ps, x_data, derece)
        # y_p7 = np.poly1d(ps[7])
        # print(y_p7(30))          # 30 noktasindaki degerini verir.
        return y_preds, ps


# ==========================================================================
"""adres = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\MayisUcuncuCuma.csv"
ayinKaciList = [19]
ayinKaci = ayinKaciDuzenle(ayinKaciList)
dakikaAraligiList = [0,15,30,45]
dakikaAraligi = dakikaAraligiDuzenle(dakikaAraligiList)
if suzsunMu==True:
    veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, dakikaAraligi, ay, adres,yil)"""
# ==========================================================================

# ==========================================================================
"""adres3HI = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\MayisUcuncuHaftaIci.csv"
ayinKaciList = [15,16,17,18]
ayinKaci = ayinKaciDuzenle(ayinKaciList)
# Mayis 3. hafta icinin csv dosyasi
if suzsunMu==True:
    veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, dakikaAraligi, ay, adres3HI,yil)"""
# ==========================================================================

# ==========================================================================
"""adresMayisButunCumalar = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\MayisButunCumalar.csv"
ayinKaciList = [5,12,19]
ayinKaci = ayinKaciDuzenle(ayinKaciList)
dakikaAraligiList = [0,15,30,45]
dakikaAraligi = dakikaAraligiDuzenle(dakikaAraligiList)
if suzsunMu==True:
    veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, dakikaAraligi, ay, adresMayisButunCumalar,yil)"""
# ==========================================================================


# ==========================================================================
"""yil = 2016
adres2016MayisIlkCuma = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\Mayis2016IlkCuma.csv"
ayinKaciList = [13]
ayinKaci = ayinKaciDuzenle(ayinKaciList)
dakikaAraligiList = [0,15,30,45]
dakikaAraligi = dakikaAraligiDuzenle(dakikaAraligiList)
if suzsunMu==True:
    veriyiSuzVeKaydet(vSegID, vSegDir, ayinKaci, dakikaAraligi, ay, adres2016MayisIlkCuma,yil)"""
# ==========================================================================

"""x_data, y_dataUcuncuCuma = y_DataOlustur(adres,derece,derece7)
x_data, y_dataUcuncuHaftaIci = y_DataOlustur(adres3HI,derece,derece7)
x_data, y_dataButunCumalar = y_DataOlustur(adresMayisButunCumalar,derece,derece7)
x_data, y_data2016IlkCuma = y_DataOlustur(adres2016MayisIlkCuma,derece,derece7)"""

"""ps = []
y_predsUcuncuCuma,ps = y_predsle(x_data, y_dataUcuncuCuma, derece)
y_predsUcuncuHaftaIci,_ = y_predsle(x_data, y_dataUcuncuHaftaIci, derece)
y_predsButunCumalar,_ = y_predsle(x_data, y_dataButunCumalar, derece)
y_preds2016IlkCuma,_ = y_predsle(x_data, y_data2016IlkCuma, derece)"""

# poly1d() fonksiyonu ise bizim tahmini degerini ogrenmek istedigimiz
# sayinin sonucu verir.
# y_p7 = np.poly1d(p7)
# print(y_p7(0))     # 0 noktasindaki egrinin degerini verir.

"""y_trueUcuncuCuma = y_dataUcuncuCuma
x = symbols("x")

for a in range(derece7):
    poly = sum(S("{}".format(v))*x**i for i, v in enumerate(ps[a][::-1]))
    #print("poly: ", poly)
eq_latex = sympy.printing.latex(poly)

print("7. dereceden denklem icin:")
for i in range(10):
    print("{}= ".format(str(i*10)+"-"+ str(10*(i+1)) ), "%",round(mean_absolute_error(y_dataUcuncuCuma[10*i:10*(i+1)], (y_predsUcuncuCuma[derece7])[10*i:10*(i+1)] ),3 ), sep="")
print()
for i in range(10):
    print("{}= ".format(str(i*10)+"-"+ str(10*(i+1)) ), "%",round(mean_absolute_error(y_dataUcuncuHaftaIci[10*i:10*(i+1)], (y_predsUcuncuCuma[derece7])[10*i:10*(i+1)] ),3 ), sep="")
print()
for i in range(10):
    print("{}= ".format(str(i*10)+"-"+ str(10*(i+1)) ), "%",round(mean_absolute_error(y_dataButunCumalar[10*i:10*(i+1)], (y_predsUcuncuCuma[derece7])[10*i:10*(i+1)] ),3 ), sep="")
print()
for i in range(10):
    print("{}= ".format(str(i*10)+"-"+ str(10*(i+1)) ), "%",round(mean_absolute_error(y_data2016IlkCuma[10*i:10*(i+1)], (y_predsUcuncuCuma[derece7])[10*i:10*(i+1)] ),3 ), sep="")
print()
"""

"""#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text', usetex=True)
plt.figure(figsize=(6*3.3, 4*3.3))
plt.title(r'Eq =' r"${}$".format(eq_latex), fontsize=12, color="r")
# plt.plot(x_dat, y_dat, "-") yaparsak x eksenininde ceyrek saatleri
# verir ama o zaman da cok fazla deger oldugundan bir sey anlasilmiyor.
plt.plot(x_data, y_dataUcuncuCuma, "o")
plt.plot(x_data, y_predsUcuncuCuma[derece7], "-" )
plt.plot(x_data, y_predsUcuncuHaftaIci[derece7], "-")
plt.plot(x_data, y_predsButunCumalar[derece7], "-")
plt.plot(x_data, y_preds2016IlkCuma[derece7], "-")
plt.legend(['data', 'Ilk3Cuma', 'Ilk3HaftaIci', 'MayisButunCumalar', '2016MayisIlkCuma'], loc='best')
"""

"""resimAdresUcuncuCuma = "C:\\Users\\ibrahim\\Desktop\\SQL\\Regression\\MayisKarsilastirma.png"
plt.savefig(resimAdresUcuncuCuma)

"""