LAYER_ID = "7j6V";

function GeoTriggers(featureGroup, callback) {
  var self = this;
  this.featureGroup = featureGroup;
  this.callback = callback;
  this.timeoutIds = [];
  this._isPlaying = false;
  //this.login();
  //this.showTriggers();
}


GeoTriggers.prototype.updateLocation = function() {
  var timestamp = playback.getTime();
  var timeString = new Date().toISOString();

  var markers = playback.tick.getMarkers();
  for(var i=0,len=markers.length;i<len;i++){
    var latlng = markers[i].getLatLng();
    var points = [{
      date: timeString,
      location: {
        type: 'point',
        position: {
          latitude: latlng.lat,
          longitude: latlng.lng
        }
      },
      client: {
        platform: 'LeafletPlayback',
        hardware: 'browser',
        name: 'LeafletPlayback',
        version: '0.0.1'
      },
      raw: {
        inBrowser: true,
        simulation: true,
        clockTime: timestamp,
        application: 'LeafletPlayback',
        version: '0.0.1'
      }
    }];
  }
}


GeoTriggers.prototype._poll = function() {
  var updated = false;
  var self = this;
  self.updateLocation();
    // poll timer
    if (!self._isPlaying) return;
    var timeoutId = window.setTimeout(function(self) {
      self._poll();
    }, 1000, self);
    self.timeoutIds.push(timeoutId);
}


GeoTriggers.prototype.startPolling = function() {
  if (this.timeoutIds.length>0) return;
  this._isPlaying = true;
  this._poll();
}


GeoTriggers.prototype.stopPolling = function() {
  this._isPlaying = false;
  while (this.timeoutIds.length>0) {
    var id = this.timeoutIds.pop();
    window.clearTimeout(id);
  }
}

GeoTriggers.prototype._displayTrigger = function(trigger) {
  var place = trigger.place;
  var latlng = new L.LatLng(place.latitude,place.longitude);
  var radius = place.radius;
  var circle = new L.Circle(latlng, radius, {
    color: '#FF9500',
    fillColor: '#FF9500'
  });
  var popup = new L.Popup();
  // console.log(['trigger', trigger]);

  var title = trigger.place.name;
  var message = trigger.text;
  var visits = trigger.place.visits || 0;

  var html =
'<legend>' + title + '</legend>' +
'<p>' + message + '</p>' +
'<p>Visits: <span class="badge badge-info">' + visits + '</span></p>' +
'<div class="btn-group">' +
'  <button onclick="geoTriggers.deleteTriggerAndCircle(\''+place.place_id+'\')" class="btn btn-danger delete"><i class="icon-trash"></i> Delete</button>' +
'  <button class="btn btn-info edit"><i class="icon-edit"></i> Edit Details</button>' +
'  <button onclick="drawControl._toolbars[3560]._modes.edit.handler.enable()" class="btn btn-success move"><i class="icon-move"></i> Move</button>' +
'</div>';

  popup.setContent(html);
  circle.bindPopup(popup);
  circle.placeId = place.place_id;
  this.featureGroup.addLayer(circle);
}


GeoTriggers.prototype.deleteTriggerAndCircle = function(placeId) {
  var self = this;
  $('#delete-modal-btn').data('placeId',placeId).on('click',function(e){
    var placeId = $(this).data('placeId');
    self.deleteTrigger(placeId);
    var match = null;
    $.each(geoTriggerFeatureGroup._layers, function(i) {
      var id = geoTriggerFeatureGroup._layers[i].placeId;
      if (placeId === id) {
        var layer = geoTriggerFeatureGroup._layers[i];
        geoTriggerFeatureGroup.removeLayer(layer);
        $('#delete-modal').modal('hide');
        console.log(placeId);
        return;
      }
    });
  });
  $('#delete-modal').modal();
}
