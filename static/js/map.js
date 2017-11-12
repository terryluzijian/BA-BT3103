/**
 * Created by terry on 11/12/2017.
 */

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