from django.shortcuts import render, HttpResponse
from django.shortcuts import render, HttpResponse, get_object_or_404
import pyodbc
from pykml import parser
import pickle

def home_view(request):
    global cursor
    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "SERVER=IBRAHIM;"
                          "Database=FusedData-2016-2017-2018;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()
    vSegDir = request.POST.get('vSegDirStandartSapma')
    print("***: ", vSegDir)




    return render(request, 'home2.html', {})