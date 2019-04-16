from django.shortcuts import render, HttpResponse, get_object_or_404
from .kodlar import mypythoncode
import pyodbc
from pykml import parser
import pickle
from django.template.loader import render_to_string

def analiz_home(request):
    global cursor
    
    outputNameFile = "C:\\Users\\ibrahim\\Desktop\\trafSite\\znameList.txt"
    outputCoordinateFile = "C:\\Users\\ibrahim\\Desktop\\trafSite\\zcoordinateList.txt"
    inputFile = "C:\\Users\\ibrahim\\Desktop\\trafSite\\docu.kml"
    nameList = []
    coordinateList = []

    cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                          "SERVER=IBRAHIM;"
                          "Database=FusedData-2016-2017-2018;"
                          "Trusted_Connection=yes;")
    cursor = cnxn.cursor()
    print("-------------------Veritabanına bağlandı")
    allOfList = []
    itemlist = []
    """
    Matrix = [[0 for x in range(2)] for y in range(10000)] 

    with open(inputFile) as f:
        doc = parser.parse(f).getroot().Document.Folder

        for attr in doc.Placemark:
            coordinateList.append(attr.MultiGeometry.Point.coordinates)
            nameList.append(attr.name)

    with open(outputNameFile, 'rb') as fp:
        itemlist = pickle.load(fp)

    with open(outputCoordinateFile, 'rb') as fp:
        item2list = pickle.load(fp)

    #for i in range(len(itemlist)):
    for i in range(100):
        b = []
        b.append(itemlist[i])
        ayriKoordinatList = str(item2list[i]).split(",")
        b.append(ayriKoordinatList[0])
        b.append(ayriKoordinatList[1])
        b.append(ayriKoordinatList[2])
        allOfList.append(b)
        #Matrix[i][0] = itemlist[i]
        #Matrix[i][1] = item2list[i]
        #allOfList.append(itemlist[i])
        #allOfList.append(item2list[i])

    """

    """locations = [[32.715736, -117.161087],
                 [32.723036, -117.259052]
                ]
    for i in locations:
        print(i)"""

    return render(request, 'analizz/analizTakvim.html', {'allOf': allOfList, 'range': range(len(itemlist))})

def analiz_grafikler(request):
    print("ahanda ")
    year = request.POST.get('year')
    month = request.POST.get('month')
    #day = request.POST.get('day')
    sensor = request.POST.get('sensor')
    vSegDir = request.POST.get('vSegDir')
    print(year, month, sensor, vSegDir)
    mypythoncode.degerleriAl(request, cursor)
    tarihParcalanacakString = request.POST.get('datepicker1')
    tarihParcalanmisListe = tarihParcalanacakString.split('/')
    vSegDir = request.POST.get('vSegDirTumGun')
    vSegID = request.POST.get('vSegIDTumGun')
    yil = tarihParcalanmisListe[2]
    ay = tarihParcalanmisListe[0]
    print("ay: ", ay)
    if (ay[0] == "0"):
        ay = ay.replace("0", "")
    ayinKaci = tarihParcalanmisListe[1]
    resimBilgisi = "images/"+ yil+ "-"+ ay+ "-"+ ayinKaci+ "-"+ vSegID+"-"+vSegDir+".png"
    context = {'resimIsmi': 'resimBilgisi'}
    return render(request, 'analizz/grafik.html', context)