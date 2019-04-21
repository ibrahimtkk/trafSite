window.onload = function () {
    harita();
    /*src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap">*/
    BindEvent();
}

function BindEvent() {
    var aramaTurleri = document.getElementById("aramaTurleri");
    var deger = aramaTurleri.onchange = function () { SetSel (this); }
    /*if (deger == "Tüm Gün"){
        var vSegDir = document.getElementById("vSegDir");
        vSegDir.value = deger;
    }*/
    // elemToBind.onchange = function () { SetSel (this); }
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

function harita(){
    var src = 'C:\\Users\\ibrahim\\Desktop\\trafSite\\doc.kml';
    var myMap, myPlacemark;
    ymaps.ready(init);

    function init(){ 
        myMap = new ymaps.Map("map", {
            center: [41.0082, 28.9784],
            zoom: 10,
            controls: ['zoomControl']
        }), 
        kmlButton = $('.load-kml');

        kmlButton.get(0).disabled = false;

        myPlacemark = new ymaps.Placemark([41.0082, 28.9784], { 
            hintContent: 'Istanbul!', balloonContent: 'Capital of Ottoman'
        });


        myMap.geoObjects.add(myPlacemark);
        ymaps.geoXml.load('docu.kml')
            .then(function(res){
                myMap.geoObjects.add(res.geoObjects);
        });
    

    function onGeoXmlLoad(res) {
        myMap.geoObjects.add(res.geoObjects);
        if (res.mapState) {
            res.mapState.applyToMap(myMap);
        }
        else {
            myMap.setBounds(res.geoObjects.getBounds());
        }
    }


    }





}