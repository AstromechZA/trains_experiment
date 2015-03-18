google.maps.event.addDomListener(window, 'load', init)

function init() {
    var mapOptions = {
        zoom: 12,
        center: new google.maps.LatLng(-33.9878033,18.5625039),
        disableDefaultUI: true,
        styles:
        [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#0c0b0b"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#090909"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#e4e4e4"}]},{"featureType":"road.highway","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"road.local","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"visibility":"on"},{"weight":"2.66"},{"color":"#bd3e3e"}]},{"featureType":"transit.line","elementType":"geometry.stroke","stylers":[{"weight":"0.01"},{"visibility":"off"}]},{"featureType":"transit.station","elementType":"labels.text","stylers":[{"visibility":"simplified"}]},{"featureType":"transit.station","elementType":"labels.icon","stylers":[{"visibility":"on"},{"weight":"1.00"},{"saturation":"-28"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#d4e4eb"},{"visibility":"on"}]},{"featureType":"water","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#fef7f7"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"color":"#9b7f7f"}]},{"featureType":"water","elementType":"labels.text.stroke","stylers":[{"color":"#fef7f7"}]}]
    }

    var mapElement = document.getElementById('map');
    var map = new google.maps.Map(mapElement, mapOptions);
    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(-33.9878033,18.5625039),
        map: map,
        title: 'Snazzy!'
    })
}
