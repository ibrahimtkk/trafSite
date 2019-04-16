# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 18:26:32 2018

@author: ibrahim
"""
import pandas as pd

xlsxDosyaAdresi = "C:\\Users\\ibrahim\\Desktop\\trafSite\\Meteoroloji_Verisi\\olduSanirim.xlsx"

df = pd.read_excel(xlsxDosyaAdresi)

xlsxSatirListesi = []
istasyonNolar = [17060, 17813, 18401, 18403, 18404]
i = 0
aylar = [1,2,3,4,5,6,7,8,9,10,11,12]
maxGunler = [31,28,31,30,31,30,31,31,30,31,30,31]
sayi = [[], [], [], [], []]

for i in range(5):
    print(istasyonNolar[i], ":", "\n")
    for ay in range(len(aylar)):
        havaDurumuSayisi = 0
        for row in df.iterrows():
            index, data = row
            #print(data[0], data[1], data[2], data[3], data[4], data[5])
            if istasyonNolar[i] == data[0]:
                if (ay+1)==data[3]:
                    havaDurumuSayisi += 1
        print("{}. ay: ".format(ay+1), havaDurumuSayisi/(maxGunler[ay]*24)*100)
        

           #if ( data[0]==Istasyon_No and data[2]==yil and data[3]==gun and data[4]==saat ):
            #   return data[5] 