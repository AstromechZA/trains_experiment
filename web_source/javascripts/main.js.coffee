window.drawline = (point_list) ->
  new google.maps.Polyline({
    path: (new google.maps.LatLng(p['lat'], p['lon']) for p in point_list),
    geodesic: true,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 2,
    map: window.map
  })

window.drawpoint = (point) ->
  new google.maps.Marker({
    position: new google.maps.LatLng(point['lat'], point['lon']),
    map: window.map,
    icon: {url: 'images/dot_point.png', anchor: new google.maps.Point(5, 6), size: new google.maps.Size(11, 12)}
  })

window.drawme = (data) ->
  window.drawpoint(p) for p in data['points']
  window.drawline(l) for l in data['lines']

window.importjs = (path) ->
  e = document.createElement 'script'
  e.setAttribute 'type', 'text/javascript'
  e.setAttribute 'src', path
  console.log('Attempting to import ' + path)
  document.getElementsByTagName('head')[0].appendChild e
  return

init = ->
  anchor = new google.maps.LatLng(-33.9878033, 18.5625039)

  mapOptions =
    zoom: 11
    center: anchor
    disableDefaultUI: true
    styles: [{"featureType":"administrative","elementType":"labels.text.fill","stylers":[{"color":"#0c0b0b"}]},{"featureType":"landscape","elementType":"all","stylers":[{"color":"#f2f2f2"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":-100},{"lightness":45}]},{"featureType":"road","elementType":"labels.text.fill","stylers":[{"color":"#090909"}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#e4e4e4"}]},{"featureType":"road.highway","elementType":"labels","stylers":[{"visibility":"off"}]},{"featureType":"road.arterial","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"road.local","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"transit.line","elementType":"geometry","stylers":[{"visibility":"on"},{"weight":"2.66"},{"color":"#bd3e3e"}]},{"featureType":"transit.line","elementType":"geometry.stroke","stylers":[{"weight":"0.01"},{"visibility":"off"}]},{"featureType":"transit.station","elementType":"labels.text","stylers":[{"visibility":"simplified"}]},{"featureType":"transit.station","elementType":"labels.icon","stylers":[{"visibility":"on"},{"weight":"1.00"},{"saturation":"-28"}]},{"featureType":"water","elementType":"all","stylers":[{"color":"#d4e4eb"},{"visibility":"on"}]},{"featureType":"water","elementType":"geometry.fill","stylers":[{"visibility":"on"},{"color":"#fef7f7"}]},{"featureType":"water","elementType":"labels.text.fill","stylers":[{"color":"#9b7f7f"}]},{"featureType":"water","elementType":"labels.text.stroke","stylers":[{"color":"#fef7f7"}]}]

  window.map = new google.maps.Map(document.getElementById('map'), mapOptions)

  window.importjs 'data/drawme.js'

  return

google.maps.event.addDomListener window, 'load', init
