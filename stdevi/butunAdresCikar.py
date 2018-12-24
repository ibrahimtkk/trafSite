# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 19:44:59 2018

@author: ibrahim
"""
import pickle
import pyodbc
import time

def butunSensorlerBirGun(yil, ay, gun, cursor, vSegDir):
    komut = (
        "SELECT * FROM [FusedData-2016-2017-2018].[dbo].[FusedData2017]"
        " WHERE datepart(dd, fusedDate)={} and"
        " datepart(mm, fusedDate)={} and"
        " vSegDir={}".format(gun, ay, vSegDir)
        )
    print(komut)
    cursor.execute(komut)
    
    adres = "{}-{}-{}-{}-ButunVeriler.csv".format(yil, ay, gun, vSegDir)

    butunVeriler = []
    for satir in cursor:
        deger = []
        deger.append(satir[0])
        deger.append( int(satir[1]) )
        deger.append( str(satir[2]) )
        deger.append(satir[3])
        butunVeriler.append(deger)
    #print(butunVeriler)

    with open(adres, "wb") as fp:
        pickle.dump(butunVeriler, fp)
        
        

global cursor
global cnxn
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "SERVER=MAG;"
                      "Database=FusedData-2016-2017-2018;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()



for ay in range(1, 13):
    for vSegDir in range(2):
        print("---")
        start = time.time()
        butunSensorlerBirGun(2017, ay, 15, cursor, vSegDir)
        end = time.time()
        print(ay, vSegDir, end-start)