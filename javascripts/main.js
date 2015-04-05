(function() {
  var init;

  window.train_markers = [];

  window.current_time = 5 * 60 * 60;

  window.drawline = function(point_list) {
    var p;
    return new google.maps.Polyline({
      path: (function() {
        var i, len, results;
        results = [];
        for (i = 0, len = point_list.length; i < len; i++) {
          p = point_list[i];
          results.push(new google.maps.LatLng(p['lat'], p['lon']));
        }
        return results;
      })(),
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2,
      map: window.map
    });
  };

  window.drawpoint = function(point) {
    return new google.maps.Marker({
      position: new google.maps.LatLng(point['lat'], point['lon']),
      map: window.map,
      icon: {
        url: 'images/dot_point.png',
        anchor: new google.maps.Point(5, 6),
        size: new google.maps.Size(11, 12)
      }
    });
  };

  window.interpolate_coords = function(point1, point2, ratio) {
    ratio = Math.min(Math.max(0, ratio), 1);
    return {
      'lat': point1['lat'] + (point2['lat'] - point1['lat']) * ratio,
      'lon': point1['lon'] + (point2['lon'] - point1['lon']) * ratio
    };
  };

  window.callback_data_loaded = function() {
    var c, i, len, ref;
    console.log('data_loaded');
    ref = window.data_connections;
    for (i = 0, len = ref.length; i < len; i++) {
      c = ref[i];
      window.drawline([window.data_stations[c[0]], window.data_stations[c[1]]]);
    }
    return window.tick_forward();
  };

  window.draw_current_state = function(time_now) {
    var i, j, last_stop, len, len1, p, r, ref, ref1, results, s, t;
    ref = window.train_markers;
    for (i = 0, len = ref.length; i < len; i++) {
      p = ref[i];
      p.setMap(null);
    }
    window.train_markers = [];
    ref1 = window.data_trains['weekdays'];
    results = [];
    for (j = 0, len1 = ref1.length; j < len1; j++) {
      t = ref1[j];
      last_stop = null;
      results.push((function() {
        var k, len2, ref2, results1;
        ref2 = t['stops'];
        results1 = [];
        for (k = 0, len2 = ref2.length; k < len2; k++) {
          s = ref2[k];
          if (last_stop != null) {
            if (last_stop[1] < time_now && s[1] >= time_now) {
              r = (time_now - last_stop[1]) / (s[1] - last_stop[1]);
              window.train_markers.push(window.drawpoint(window.interpolate_coords(window.data_stations[last_stop[0]], window.data_stations[s[0]], r)));
            }
          }
          results1.push(last_stop = s);
        }
        return results1;
      })());
    }
    return results;
  };

  window.tick_forward = function() {
    var hours, minutes;
    window.current_time += 60;
    if (window.current_time > (24 * 60 * 60)) {
      window.current_time = 0;
    }
    window.draw_current_state(window.current_time);
    hours = Math.floor(window.current_time / (60 * 60));
    minutes = Math.floor((window.current_time % (60 * 60)) / 60);
    return document.getElementById('time-wrapper').innerHTML = "" + (hours < 10 ? '0' : '') + hours + ":" + (minutes < 10 ? '0' : '') + minutes;
  };

  window.tick_backward = function() {
    var hours, minutes;
    window.current_time -= 60;
    if (window.current_time < (0 * 60 * 60)) {
      window.current_time = 24 * 60 * 60;
    }
    window.draw_current_state(window.current_time);
    hours = Math.floor(window.current_time / (60 * 60));
    minutes = Math.floor((window.current_time % (60 * 60)) / 60);
    return document.getElementById('time-wrapper').innerHTML = "" + (hours < 10 ? '0' : '') + hours + ":" + (minutes < 10 ? '0' : '') + minutes;
  };

  document.onkeydown = function(e) {
    e = e || window.event;
    if (e.which === 39) {
      window.tick_forward();
      e.preventDefault();
    }
    if (e.which === 37) {
      window.tick_backward();
      return e.preventDefault();
    }
  };

  window.importjs = function(path) {
    var e;
    e = document.createElement('script');
    e.setAttribute('type', 'text/javascript');
    e.setAttribute('src', path);
    console.log('Attempting to import ' + path);
    document.getElementsByTagName('head')[0].appendChild(e);
  };

  init = function() {
    var anchor, mapOptions;
    anchor = new google.maps.LatLng(-33.9878033, 18.5625039);
    mapOptions = {
      zoom: 11,
      center: anchor,
      disableDefaultUI: true,
      styles: [
        {
          "featureType": "all",
          "elementType": "labels.text.fill",
          "stylers": [
            {
              "saturation": 36
            }, {
              "color": "#333333"
            }, {
              "lightness": 40
            }
          ]
        }, {
          "featureType": "all",
          "elementType": "labels.text.stroke",
          "stylers": [
            {
              "visibility": "on"
            }, {
              "color": "#ffffff"
            }, {
              "lightness": 16
            }
          ]
        }, {
          "featureType": "all",
          "elementType": "labels.icon",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        }, {
          "featureType": "administrative",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#fefefe"
            }, {
              "lightness": 20
            }
          ]
        }, {
          "featureType": "administrative",
          "elementType": "geometry.stroke",
          "stylers": [
            {
              "color": "#fefefe"
            }, {
              "lightness": 17
            }, {
              "weight": 1.2
            }
          ]
        }, {
          "featureType": "landscape",
          "elementType": "geometry",
          "stylers": [
            {
              "color": "#f5f5f5"
            }, {
              "lightness": 20
            }
          ]
        }, {
          "featureType": "poi",
          "elementType": "geometry",
          "stylers": [
            {
              "color": "#f5f5f5"
            }, {
              "lightness": 21
            }
          ]
        }, {
          "featureType": "poi.park",
          "elementType": "geometry",
          "stylers": [
            {
              "color": "#dedede"
            }, {
              "lightness": 21
            }
          ]
        }, {
          "featureType": "road.highway",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#ffffff"
            }, {
              "lightness": 17
            }
          ]
        }, {
          "featureType": "road.highway",
          "elementType": "geometry.stroke",
          "stylers": [
            {
              "color": "#ffffff"
            }, {
              "lightness": 29
            }, {
              "weight": 0.2
            }
          ]
        }, {
          "featureType": "road.arterial",
          "elementType": "geometry",
          "stylers": [
            {
              "color": "#ffffff"
            }, {
              "lightness": 18
            }
          ]
        }, {
          "featureType": "road.local",
          "elementType": "geometry",
          "stylers": [
            {
              "color": "#ffffff"
            }, {
              "lightness": 16
            }
          ]
        }, {
          "featureType": "transit",
          "elementType": "geometry",
          "stylers": [
            {
              "color": "#f2f2f2"
            }, {
              "lightness": 19
            }
          ]
        }, {
          "featureType": "water",
          "elementType": "geometry",
          "stylers": [
            {
              "color": "#e9e9e9"
            }, {
              "lightness": 17
            }
          ]
        }
      ]
    };
    window.map = new google.maps.Map(document.getElementById('map'), mapOptions);
    window.importjs('data/all_data.js');
  };

  google.maps.event.addDomListener(window, 'load', init);

}).call(this);
