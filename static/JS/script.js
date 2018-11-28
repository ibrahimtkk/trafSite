//{% extends "harita.html" %}

window.onload = function () {
    //harita();
    //harita.initMap();
    //BindEvent();
    getTakvim();
}

function getTakvim () {
    var objCal = document.getElementById("datepicker");
    $(function(){
        $('#datepicker').datepicker();                     
    });
}

function BindEvent() {
    var aramaTurleri = document.getElementById("aramaTurleri");
    var deger = aramaTurleri.onchange = function () { 
        SetSel (this);
    }
    /*if (deger == "Tüm Gün"){
        var vSegDir = document.getElementById("vSegDir");
        vSegDir.value = deger;
    }*/
    //elemToBind.onchange = function () { SetSel (this); }
}

function SetSel(deger) {
    var vSegDir = document.getElementById("vSegDir");
    var vSegDirLabel = document.getElementById("vSegDirLabel");
    var vSegID = document.getElementById("vSegID");
    var vSegIDLabel = document.getElementById("vSegIDLabel");
    var year = document.getElementById("year");
    var yearLabel = document.getElementById("yearLabel");
    var month = document.getElementById("month");
    var monthLabel = document.getElementById("monthLabel");
    var day = document.getElementById("day");
    var dayLabel = document.getElementById("dayLabel");
    var startClock = document.getElementById("startClock");
    var startClockLabel = document.getElementById("startClockLabel");
    var endClock = document.getElementById("endClock");
    var endClockLabel = document.getElementById("endClockLabel");
    var aralik = document.getElementById("aralik");
    var aralikLabel = document.getElementById("aralikLabel");
    var trafikSorguLegend = document.getElementById("trafikSorguLegend");
    if (deger.value == "Seçiniz.."){
        day.style.visibility = 'hidden';
        dayLabel.style.visibility = 'hidden';
        startClock.style.visibility = 'hidden';
        startClockLabel.style.visibility = 'hidden';
        endClock.style.visibility = 'hidden';
        endClockLabel.style.visibility = 'hidden';
        aralik.style.visibility = 'hidden';
        aralikLabel.style.visibility = 'hidden';

    }
    else if (deger.value == "Tüm Gün"){
        day.style.visibility = 'visible';
        dayLabel.style.visibility = 'visible';
        startClock.style.visibility = 'hidden';
        startClockLabel.style.visibility = 'hidden';
        endClock.style.visibility = 'hidden';
        endClockLabel.style.visibility = 'hidden';
        aralik.style.visibility = 'hidden';
        aralikLabel.style.visibility = 'hidden';
    }
    else if (deger.value == "Belirli Saat"){
        day.style.visibility = 'visible';
        dayLabel.style.visibility = 'visible';
        startClock.style.visibility = 'visible';
        startClockLabel.style.visibility = 'visible';
        endClock.style.visibility = 'visible';
        endClockLabel.style.visibility = 'visible';
        aralik.style.visibility = 'hidden';
        aralikLabel.style.visibility = 'hidden';
    }

    else if (deger.value == "Günün Belirli Aralıkları"){
        startClock.style.visibility = 'hidden';
        startClockLabel.style.visibility = 'hidden';
        endClock.style.visibility = 'hidden';
        endClockLabel.style.visibility = 'hidden';
        aralik.style.visibility = 'visible';
        aralikLabel.style.visibility = 'visible';
    }
}

/*function harita(){
    var map;
    function initMap(){
        map = new google.maps.Map(document.getElementById('map'),
        {
            center: new google.maps.LatLng(41.0082, 28.9784),
            zoom: 11,
            mapTypeId: 'terrain'
        });

        var j=0;
        var arr = [];

        {% for i in iler %}
            arr.push( '{{ i }}' );
        {% endfor %}

        {% for all in allOff %}
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng( {{ all.2 }}, {{ all.1 }} ),
                map: map
            });

            alert(arr[j]);

            var infowindow = new google.maps.InfoWindow({
                //content: ` ${arr[j]} `
                //content: String(all.3)
                content: arr[j] ,
                map: map
            });
            j += 1;

            google.maps.event.addListener(marker, 'mouseover',
                function(){
                    infowindow.open(map, this);
                });

            google.maps.event.addListener(marker, 'mouseout',
                function(){
                    infowindow.close(map, this);
                });

        {% endfor %}


    "https://maps.googleapis.com/maps/api/js?key=AIzaSyAiLaYpd0zx4HfjULaOVcgxVpQMuKNmD04&callback=initMap"


    }
*/






    /*function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
            center: new google.maps.LatLng(32.715736, -117.161087),
            zoom: 8,
            mapTypeId: 'terrain'
        });
        var kmlLayer = new google.maps.KmlLayer('https://www.dropbox.com/s/q4539mtu14whgkm/doc.kml?dl=0', {
            suppressInfoWindows: true,
            preserveViewport: false,
            map: map
        });
        //kmlLayer.setMap(map);
    }
    'https://maps.googleapis.com/maps/api/js?key=AIzaSyAiLaYpd0zx4HfjULaOVcgxVpQMuKNmD04&callback=initMap'*/


    //var src = 'https://www.dropbox.com/s/q4539mtu14whgkm/doc.kml?dl=0';
    /*src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAiLaYpd0zx4HfjULaOVcgxVpQMuKNmD04&callback=initMap"
    map = new google.maps.Map(document.getElementById('map'), {
        center: new google.maps.LatLng(38.1910, -120.6750),
        zoom: 14,
        mapTypeId: 'terrain'
    });
    var kmlLayer = new google.maps.KmlLayer('https://drive.google.com/file/d/1SKATZLnCq-dz4PHjfUKpmO9xPgbjHzPe/view', {
        suppressInfoWindows: true,
        preserveViewport: true,
        map: map
    });*/
    //kmlLayer.setMap(map);

    //myParser.parse('C:\\Users\\ibrahim\\Desktop\\trafSite\\docu.kml');

    /*var ctaLayer = new google.maps.KmlLayer({
        url: 'C:\\Users\\ibrahim\\Desktop\\trafSite\\docu.kml',
        map: map
    });*/

    /*
    kmlLayer.addListener('click', function(event) {
        var content = event.featureData.infoWindowHtml;
        var testimonial = document.getElementById('capture');
        testimonial.innerHTML = content;
    });*/

    // san andreas = (38.1910, -120.6750)
    // istanbul = (41.0082, 28.9784)




    //}