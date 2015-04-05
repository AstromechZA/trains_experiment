
window.train_markers = []
window.current_time = (6 * 60 * 60)

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

window.interpolate_coords = (point1, point2, ratio) ->
  ratio = Math.min(Math.max(0, ratio), 1)
  return {
    'lat': point1['lat'] + (point2['lat'] - point1['lat']) * ratio
    'lon': point1['lon'] + (point2['lon'] - point1['lon']) * ratio
  }

window.callback_data_loaded = ->
  console.log 'data_loaded'
  for c in window.data_connections
    window.drawline [window.data_stations[c[0]], window.data_stations[c[1]]]

  window.draw_current_state(window.current_time)


window.draw_current_state = (time_now) ->
  for p in window.train_markers
    p.setMap(null)

  window.train_markers = []

  for t in window.data_trains['weekdays']
    last_stop = null
    for s in t['stops']
      if last_stop?
        if last_stop[1] < time_now and s[1] >= time_now
          r = (time_now - last_stop[1]) / (s[1] - last_stop[1])
          window.train_markers.push(window.drawpoint window.interpolate_coords(window.data_stations[last_stop[0]], window.data_stations[s[0]], r))
      last_stop = s


window.tick = ->
  window.current_time += 60
  window.draw_current_state(window.current_time)

document.onkeydown = (e) ->
  e = e || window.event
  if e.which == 39
    window.tick()
    e.preventDefault()


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
    styles: [{"featureType":"all","elementType":"labels.text.fill","stylers":[{"saturation":36},{"color":"#333333"},{"lightness":40}]},{"featureType":"all","elementType":"labels.text.stroke","stylers":[{"visibility":"on"},{"color":"#ffffff"},{"lightness":16}]},{"featureType":"all","elementType":"labels.icon","stylers":[{"visibility":"off"}]},{"featureType":"administrative","elementType":"geometry.fill","stylers":[{"color":"#fefefe"},{"lightness":20}]},{"featureType":"administrative","elementType":"geometry.stroke","stylers":[{"color":"#fefefe"},{"lightness":17},{"weight":1.2}]},{"featureType":"landscape","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":20}]},{"featureType":"poi","elementType":"geometry","stylers":[{"color":"#f5f5f5"},{"lightness":21}]},{"featureType":"poi.park","elementType":"geometry","stylers":[{"color":"#dedede"},{"lightness":21}]},{"featureType":"road.highway","elementType":"geometry.fill","stylers":[{"color":"#ffffff"},{"lightness":17}]},{"featureType":"road.highway","elementType":"geometry.stroke","stylers":[{"color":"#ffffff"},{"lightness":29},{"weight":0.2}]},{"featureType":"road.arterial","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":18}]},{"featureType":"road.local","elementType":"geometry","stylers":[{"color":"#ffffff"},{"lightness":16}]},{"featureType":"transit","elementType":"geometry","stylers":[{"color":"#f2f2f2"},{"lightness":19}]},{"featureType":"water","elementType":"geometry","stylers":[{"color":"#e9e9e9"},{"lightness":17}]}]

  window.map = new google.maps.Map(document.getElementById('map'), mapOptions)

  window.importjs 'data/all_data.js'

  return

google.maps.event.addDomListener window, 'load', init
