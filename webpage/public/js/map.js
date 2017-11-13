mapboxgl.accessToken = 'pk.eyJ1IjoidGVycnlsdXppamlhbiIsImEiOiJjajFpcWJsMHcwMXJ5MndvMHExNTVpcXM3In0.jBC1AkZcA08dnE018DIYrQ';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    zoom: 16,
    center: [103.776587, 1.296644],
    maxBounds: [
        [103.766871, 1.289500],
        [103.786345, 1.309276]
    ]
});
var nav = new mapboxgl.NavigationControl();
map.addControl(nav, 'bottom-right');

map.on('load', function () {

    var url = 'https://carvpx8wn6.execute-api.ap-southeast-1.amazonaws.com/v1/get-all-taxi?lat=1.296644&lon=103.776587';
    $(document).ready(function () {
        $.getJSON(url).then(data => {
            $.each(data.taxi.results, function(index) {
            var eachData = data.taxi.results[index];
            console.log(eachData);
            map.addLayer({
                "id": String(eachData.code),
                "type": "symbol",
                "source": {
                    "type": "geojson",
                    "data": {
                        "type": "FeatureCollection",
                        "features": [{
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [eachData.lon, eachData.lat]
                            },
                            "properties": {
                                "title": "",
                                "icon": "car"
                            }
                        }]
                    }
                },
                "layout": {
                    "icon-image": "{icon}-15",
                    "text-field": "{title}",
                    "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
                    "text-offset": [0, 0.6],
                    "text-anchor": "top"
                }
            });
        });
    });

        var url2 = 'https://carvpx8wn6.execute-api.ap-southeast-1.amazonaws.com/v1/get-all-bikes?lat=1.296644&lon=103.776587';
        $(document).ready(function () {
            $.getJSON(url2).then(data => {
                $.each(data.bike.results, function (index) {
                var eachData = data.bike.results[index];
                console.log(eachData);
                map.addLayer({
                    "id": String(eachData.code),
                    "type": "symbol",
                    "source": {
                        "type": "geojson",
                        "data": {
                            "type": "FeatureCollection",
                            "features": [{
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [eachData.lon, eachData.lat]
                                },
                                "properties": {
                                    "title": "",
                                    "icon": "bicycle"
                                }
                            }]
                        }
                    },
                    "layout": {
                        "icon-image": "{icon}-15",
                        "text-field": "{title}",
                        "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
                        "text-offset": [0, 0.6],
                        "text-anchor": "top"
                    }
                });
            });
        });
        });

        var url3 = 'https://carvpx8wn6.execute-api.ap-southeast-1.amazonaws.com/v1/get-all-buses?lat=1.296644&lon=103.776587';
        $(document).ready(function () {
            $.getJSON(url3).then(data => {
                $.each(data.bus.results, function (index) {
                var eachData = data.bus.results[index];
                console.log(eachData);
                map.addLayer({
                    "id": String(eachData.code),
                    "type": "symbol",
                    "source": {
                        "type": "geojson",
                        "data": {
                            "type": "FeatureCollection",
                            "features": [{
                                "type": "Feature",
                                "geometry": {
                                    "type": "Point",
                                    "coordinates": [eachData.lon, eachData.lat]
                                },
                                "properties": {
                                    "title": "",
                                    "icon": "bus"
                                }
                            }]
                        }
                    },
                    "layout": {
                        "icon-image": "{icon}-15",
                        "text-field": "{title}",
                        "text-font": ["Open Sans Semibold", "Arial Unicode MS Bold"],
                        "text-offset": [0, 0.6],
                        "text-anchor": "top"
                    }
                });
            });
        });
        });

    });

});