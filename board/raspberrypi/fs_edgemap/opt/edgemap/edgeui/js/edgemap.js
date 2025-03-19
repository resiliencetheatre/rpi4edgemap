/*
     _____    _                                  
    | ____|__| | __ _  ___ _ __ ___   __ _ _ __  
    |  _| / _` |/ _` |/ _ \ '_ ` _ \ / _` | '_ \ 
    | |__| (_| | (_| |  __/ | | | | | (_| | |_) |
    |_____\__,_|\__, |\___|_| |_| |_|\__,_| .__/ 
             |___/                     |_|   

    Simple Edgemap user interface for off the grid browser use
    Copyright (C) 2023 Resilience Theatre

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

    [1] https://www.spatialillusions.com/milsymbol/documentation.html
    [2] https://maplibre.org/maplibre-gl-js/docs/API/
    [3] https://protomaps.com/
 
*/
class peerList {
        constructor() {
            this.members = [];
            this.timestamps = [];
        }
        add(callsign, timeStamp) {            
            const index = this.members.findIndex(x => x === callsign);
            if (index !== -1) {
                // Update existing
                this.members[index] = callsign;
                this.timestamps[index] = timeStamp;
                return true;
            } else {
                // Add new
                this.members.push(callsign);  
                this.timestamps.push(timeStamp); 
                return true;
            }
            return false;
        }
        remove(callsign) {
            const index = this.members.findIndex(x => x === callsign);
            if (index !== -1) {
                this.members.splice(index, 1);
                this.timestamps.splice(index, 1);
                return true;
            }
            return false;
        }
        present(callsign) {
            const index = this.members.findIndex(x => x === callsign);
            if (index !== -1) {
                return true;
            }
            return false;
        }
        getSize() {
            return this.members.length;
        }
}

// Meshtastic radio list
class radioList {
        constructor() {
            this.members = [];
            this.timestamps = [];
            this.battery = [];
            this.airUtilTx = [];
            this.rxSnr = [];
            this.hopLimit = [];
            this.rxRssi = [];
        }
        add(callsign, timeStamp,DeviceBat,DeviceAirUtilTx,DeviceRxSnr,DeviceHopLimit,DeviceRxRssi) {            
            const index = this.members.findIndex(x => x === callsign);
            if (index !== -1) {
                // Update existing but don't over write existing 
                this.members[index] = callsign;
                this.timestamps[index] = timeStamp;
                if ( DeviceBat != "-" )
                    this.battery[index] = DeviceBat;
                if ( DeviceAirUtilTx != "-" )    
                    this.airUtilTx[index] = DeviceAirUtilTx;
                if ( DeviceRxSnr != "-" ) 
                    this.rxSnr[index] = DeviceRxSnr;
                if ( DeviceHopLimit != "-" ) 
                    this.hopLimit[index] = DeviceHopLimit;
                if ( DeviceRxRssi != "-" ) 
                    this.rxRssi[index] = DeviceRxRssi;
                return true;
            } else {
                // Add new
                this.members.push(callsign);  
                this.timestamps.push(timeStamp); 
                this.battery.push(DeviceBat); 
                this.airUtilTx.push(DeviceAirUtilTx); 
                this.rxSnr.push(DeviceRxSnr); 
                this.hopLimit.push(DeviceHopLimit); 
                this.rxRssi.push(DeviceRxRssi);
                return true;
            }
            return false;
        }
        // TODO: Not tested at all
        remove(callsign) {
            const index = this.members.findIndex(x => x === callsign);
            if (index !== -1) {
                this.members.splice(index, 1);
                this.timestamps.splice(index, 1);
                this.battery.splice(index, 1);
                this.airUtilTx.splice(index, 1);
                this.rxSnr.splice(index, 1);
                this.hopLimit.splice(index, 1);
                this.rxRssi.splice(index, 1);
                return true;
            }
            return false;
        }
        present(callsign) {
            const index = this.members.findIndex(x => x === callsign);
            if (index !== -1) {
                return true;
            }
            return false;
        }
        getSize() {
            return this.members.length;
        }
}

// Create sensor marker for local map when sending them
function localSensorMarkerCreate(messageData) {
    var incomingMessage = messageData;
    var trimmedString = incomingMessage.substring(0, 200);
    const msgArray=trimmedString.split("|");
    const msgFrom =  msgArray[0];
    const msgType =  msgArray[1];
    const msgLocation =  msgArray[2];
    const msgMessage =  msgArray[3];

    if ( msgArray.length == 4 ) 
    {
        //
        // Sensor marker: [FROM]|sensorMarker|[LAT,LON]|[markedId],[markerStatus],[symbol code]
        //
        if ( msgType == "sensorMarker" ) {
            const location = msgLocation;
            const locationNumbers = location.replace(/[\])}[{(]/g, '');
            const locationArray = locationNumbers.split(",");   
            const sensorDataArray = msgMessage.split(",");
            const sensorId = sensorDataArray[0];
            const sensorStatus = sensorDataArray[1];
            const sensorSymbol = sensorDataArray[2];
            createSensorMarker(locationArray[0], locationArray[1],sensorId,sensorStatus,sensorSymbol);
        }
    }
}


function toggleStyle() {
    // Get the current URL
    const url = new URL(window.location.href);

    // Get the current value of the 'style' parameter
    const currentStyle = url.searchParams.get('style');

    // Determine the new value (toggle between 'bright' and 'dark')
    const newStyle = currentStyle === 'bright' ? 'dark' : 'bright';

    // Update the 'style' parameter in the URL
    url.searchParams.set('style', newStyle);

    // Reload the page with the updated URL
    window.location.href = url.toString();
}

// reticulum node list
class reticulumList {
        constructor() {
            this.members = [];
            this.age = [];
            this.hash = [];
            this.link = [];
            this.snr = [];
            this.rssi = [];
            this.q = [];
            
        }
        add(callsign,age,hash,link,snr,rssi,q) {            
            const index = this.members.findIndex(x => x === callsign);
            if (index !== -1) {
                // Update existing but don't over write existing 
                this.members[index] = callsign;
                this.age[index] = age;
                this.hash[index] = hash;
                this.link[index] = link;
                this.snr[index] = snr;
                this.rssi[index] = rssi;
                this.q[index] = q;
                return true;
            } else {
                // Add new
                this.members.push(callsign);  
                this.age.push(age); 
                this.hash.push(hash);
                this.hash.push(link);
                this.snr.push(snr);
                this.rssi.push(rssi);
                this.q.push(q);
                return true;
            }
            return false;
        }
        // TODO: Not tested at all
        remove(callsign) {
            const index = this.members.findIndex(x => x === callsign);
            if (index !== -1) {
                this.members.splice(index, 1);
                this.age.splice(index, 1);
                this.hash.splice(index, 1);
                this.link.splice(index, 1);
                this.snr.splice(index, 1);
                this.rssi.splice(index, 1);
                this.q.splice(index, 1);
                return true;
            }
            return false;
        }
        present(callsign) {
            const index = this.members.findIndex(x => x === callsign);
            if (index !== -1) {
                return true;
            }
            return false;
        }
        getSize() {
            return this.members.length;
        }
}



function updateMeshtasticRadioListBlock() {
    document.getElementById("radiolist").innerHTML = "";
    var radioLoop=0;
    var radioListContent = "";
    // List with hop limit
    // radioListContent = "<table width=90%><tr ><td style='border-bottom: 1px solid #0F0;' >Radio</td><td style='border-bottom: 1px solid #0F0;' >Bat</td><td style='border-bottom: 1px solid #0F0;'>Air Util</td><td style='border-bottom: 1px solid #0F0;' align='center'>Hop</td><td style='border-bottom: 1px solid #0F0;' align='center'>S/N</td><td style='border-bottom: 1px solid #0F0;' align='center'>RSSI</td><td style='border-bottom: 1px solid #0F0;' align='center'>Age</td></tr>";
    // List without hop limit
    radioListContent = "<table width=90%><tr ><td style='border-bottom: 1px solid #0F0;' >Radio</td><td style='border-bottom: 1px solid #0F0;' >Bat</td><td style='border-bottom: 1px solid #0F0;'>Air Util</td><td style='border-bottom: 1px solid #0F0;' align='center'>S/N</td><td style='border-bottom: 1px solid #0F0;' align='center'>RSSI</td><td style='border-bottom: 1px solid #0F0;' align='center' title='Age in minutes' >Age</td></tr>";
    for ( radioLoop = 0; radioLoop < meshtasticRadiosOnSystem.getSize(); radioLoop++) { 
        // Calculate age
        let currentTime = Math.round(+new Date()/1000);
        var ageInSeconds = parseInt ( currentTime ) - parseInt( meshtasticRadiosOnSystem.timestamps[radioLoop] );
        var age = Math.round(ageInSeconds/60);        
        if ( age > 60 ) {
            age = ">60";
        }
        // radioListContent += "<tr><td>" + meshtasticRadiosOnSystem.members[radioLoop] + "</td><td>" + meshtasticRadiosOnSystem.battery[radioLoop] + " %</td><td>" + meshtasticRadiosOnSystem.airUtilTx[radioLoop] + " %</td><td align='center'>" + meshtasticRadiosOnSystem.hopLimit[radioLoop] + "</td><td align='center'>" + meshtasticRadiosOnSystem.rxSnr[radioLoop] + "</td><td align='center'>" + meshtasticRadiosOnSystem.rxRssi[radioLoop] + "</td><td align='center'>" + age + "</td></tr>";
        radioListContent += "<tr><td>" + meshtasticRadiosOnSystem.members[radioLoop] + "</td><td>" + meshtasticRadiosOnSystem.battery[radioLoop] + " %</td><td>" + meshtasticRadiosOnSystem.airUtilTx[radioLoop] + " %</td><td align='center'>" + meshtasticRadiosOnSystem.rxSnr[radioLoop] + "</td><td align='center'>" + meshtasticRadiosOnSystem.rxRssi[radioLoop] + "</td><td align='center'>" + age + "</td></tr>";
    }
    radioListContent += "</table>";
    document.getElementById("radiolist").innerHTML = radioListContent;
}


function updateReticulumBlock() {
    document.getElementById("reticulumlist").innerHTML = "";
    var reticulumLoop=0;
    var reticulumListContent = "";

    reticulumListContent = "<table width=90%><tr ><td style='border-bottom: 1px solid #0F0;' >Callsign</td><td style='border-bottom: 1px solid #0F0;' >Age</td><td style='border-bottom: 1px solid #0F0;'>Link</td><td style='border-bottom: 1px solid #0F0;'>SNR</td><td style='border-bottom: 1px solid #0F0;'>RSSI</td><td style='border-bottom: 1px solid #0F0;'>Qual</td> </tr>";
    for ( reticulumLoop = 0; reticulumLoop < reticulumNodesOnSystem.getSize(); reticulumLoop++) { 
        // Show nodes ages under 30 minutes
        if ( reticulumNodesOnSystem.age[reticulumLoop] < 30 ) {
            // Test some background color set to indicate aging nodes
            if ( reticulumNodesOnSystem.age[reticulumLoop] < 2 ) {
                reticulumListContent += "<tr><td title='"+reticulumNodesOnSystem.hash[reticulumLoop]+"'>" + reticulumNodesOnSystem.members[reticulumLoop] + "</td><td>" + reticulumNodesOnSystem.age[reticulumLoop] + "</td><td>" + reticulumNodesOnSystem.link[reticulumLoop]  + "</td><td>"+reticulumNodesOnSystem.snr[reticulumLoop]+"</td><td>"+reticulumNodesOnSystem.rssi[reticulumLoop]+"</td><td>"+reticulumNodesOnSystem.q[reticulumLoop]+"</td></tr>";
            } else {
                if ( reticulumNodesOnSystem.age[reticulumLoop] < 10 ) {
                    opacity = reticulumNodesOnSystem.age[reticulumLoop] / 10
                } else {
                    opacity = 1
                }
                reticulumListContent += "<tr style='background-color: rgba(255, 49, 49, "+opacity+");;'><td title='"+reticulumNodesOnSystem.hash[reticulumLoop]+"'>" + reticulumNodesOnSystem.members[reticulumLoop] + "</td><td>" + reticulumNodesOnSystem.age[reticulumLoop] + "</td><td>" + reticulumNodesOnSystem.link[reticulumLoop]  + "</td><td>"+reticulumNodesOnSystem.snr[reticulumLoop]+"</td><td>"+reticulumNodesOnSystem.rssi[reticulumLoop]+"</td><td>"+reticulumNodesOnSystem.q[reticulumLoop]+"</td></tr>";
            }
        }
    }
    reticulumListContent += "</table>";
    document.getElementById("reticulumlist").innerHTML = reticulumListContent;
}

// TODO: add openJanus() and janus destroy
function toggleVideoConference() {
    const elementOpacity=0.8;
    if( typeof toggleVideoConference.videoListVisible == 'undefined' ) {
        fadeInTo09(videoConferenceDiv ,400,elementOpacity);
        toggleVideoConference.videoListVisible = true;
        openJanus();
        return;
    }
    if ( toggleVideoConference.videoListVisible == true ) {
        fadeOutFrom09(videoConferenceDiv ,400,elementOpacity);
        toggleVideoConference.videoListVisible = false;
        closeJanus();
        return;
    }
    if ( toggleVideoConference.videoListVisible == false ) {
        fadeInTo09(videoConferenceDiv ,400,elementOpacity);
        toggleVideoConference.videoListVisible = true;
        openJanus();
        return;
    }    
}

function toggleUserList() {
    const elementOpacity=0.8;
    if( typeof toggleUserList.userListVisible == 'undefined' ) {
        fadeInTo09(peerlistblockDiv ,400,elementOpacity);
        toggleUserList.userListVisible = true;
        return;
    }
    if ( toggleUserList.userListVisible == true ) {
        fadeOutFrom09(peerlistblockDiv ,400,elementOpacity);
        toggleUserList.userListVisible = false;
        return;
    }
    if ( toggleUserList.userListVisible == false ) {
        fadeInTo09(peerlistblockDiv ,400,elementOpacity);
        toggleUserList.userListVisible = true;
        return;
    }    
}

function toggleRadioList() {
    const elementOpacity=0.8;
    
    if ( toggleReticulumList.radioListVisible == true ) {
        fadeOutFrom09(reticulumListblockDiv ,400,elementOpacity);
        toggleReticulumList.radioListVisible = false;
    }
    
    if( typeof toggleRadioList.radioListVisible == 'undefined' ) {
        fadeInTo09(radiolistblockDiv ,400,elementOpacity);
        toggleRadioList.radioListVisible = true;
        fadeOut(radioNotifyDotDiv,200);
        return;
    }
    if ( toggleRadioList.radioListVisible == true ) {
        fadeOutFrom09(radiolistblockDiv ,400,elementOpacity);
        toggleRadioList.radioListVisible = false;
        return;
    }
    if ( toggleRadioList.radioListVisible == false ) {
        fadeInTo09(radiolistblockDiv ,400,elementOpacity);
        toggleRadioList.radioListVisible = true;
        fadeOut(radioNotifyDotDiv,200);
        return;
    }    
}

function toggleReticulumList() {
    const elementOpacity=0.8;
    
    if ( toggleRadioList.radioListVisible == true ) {
        fadeOutFrom09(radiolistblockDiv ,400,elementOpacity);
        toggleRadioList.radioListVisible = false;
    }
    
    if( typeof toggleReticulumList.radioListVisible == 'undefined' ) {
        fadeInTo09(reticulumListblockDiv ,400,elementOpacity);
        toggleReticulumList.radioListVisible = true; // ???
        fadeOut(radioNotifyDotDiv,200);
        fadeOut(logDiv,200);
        return;
    }
    if ( toggleReticulumList.radioListVisible == true ) {
        fadeOutFrom09(reticulumListblockDiv ,400,elementOpacity);
        toggleReticulumList.radioListVisible = false;
        return;
    }
    if ( toggleReticulumList.radioListVisible == false ) {
        fadeInTo09(reticulumListblockDiv ,400,elementOpacity);
        toggleReticulumList.radioListVisible = true;
        fadeOut(radioNotifyDotDiv,200);
        fadeOut(logDiv,200);
        return;
    }    
}


// 
// Send to both bearers ( reticulum & meshtastic ) if they are connected
// 
function sendRetiCulumAndMeshtasticMessage(messagepayload) {
    if ( reticulumMsgSocketConnected ) {
        reticulumMsgSocket.send( messagepayload );
    }
    if ( meshtasticMsgSocketConnected ) {
        meshtasticMsgSocket.send( messagepayload );
    }
}

function sendReticulumControlMessage(messagepayload) {
    console.log("Sending reticulum control message:" + messagepayload)
    if ( reticulumStatusSocketConnected ) {
        reticulumStatusSocket.send( messagepayload + '\n' );
        notifyMessage("Announce sent", 5000);
    }
}

/*
function updatePeerListBlock() {
    document.getElementById("peerlist").innerHTML = "";
    var peerLoop=0;
    var peerListContent = "";
    for ( peerLoop = 0; peerLoop < peersOnMap.getSize(); peerLoop++) {
        peerListContent += peersOnMap.members[peerLoop];
        peerListContent += "<br>";
    }
    document.getElementById("peerlist").innerHTML = peerListContent;
}*/

// Remove peers if unheard over 30 s -> 600 s (10 min)
/*
function checkPeerExpiry() {
    let currentTime = Math.round(+new Date()/1000);
    for ( peerLoop = 0; peerLoop < peersOnMap.getSize(); peerLoop++) {
        var peerAge = parseInt ( currentTime ) - parseInt( peersOnMap.timestamps[peerLoop] );
        if ( peerAge > 600 ) {
            peersOnMap.remove( peersOnMap.members[peerLoop] );
            updatePeerListBlock(); 
        }
    }
}*/

// Remove meshstastic radios if unheard over 300 s
function checkMeshtasticRadioExpiry() {
    let currentTime = Math.round(+new Date()/1000);
    for ( nodeLoop = 0; nodeLoop < meshtasticRadiosOnSystem.getSize(); nodeLoop++) {
        var radioAge = parseInt ( currentTime ) - parseInt( meshtasticRadiosOnSystem.timestamps[nodeLoop] );
        if ( radioAge > 1200 ) {
            meshtasticRadiosOnSystem.remove( meshtasticRadiosOnSystem.members[nodeLoop] );
            updateMeshtasticRadioListBlock(); 
        }
    }
}

// Remove reticulum radios if unheard over 5 minutes
function checkReticulumRadioExpiry() {
    let currentTime = Math.round(+new Date()/1000);
    for ( nodeLoop = 0; nodeLoop < reticulumNodesOnSystem.getSize(); nodeLoop++) {
        // var radioAge = parseInt ( currentTime ) - parseInt( reticulumNodesOnSystem.timestamps[nodeLoop] );
        if ( reticulumNodesOnSystem.age[nodeLoop] > 30 ) {
            reticulumNodesOnSystem.remove( reticulumNodesOnSystem.members[nodeLoop] );
            updateReticulumBlock(); 
        }
    }
}


function notifyMessage(message, timeout) {
     fadeIn(document.getElementById("bottomLog") ,400);
        document.getElementById("notifyMessage").innerHTML = message;
        setTimeout(() => {
            fadeOut(document.getElementById("bottomLog") ,1000);
        }, timeout);
}





// 
// Replace window.location.reload(); on page reload
// 
function reloadPage() {
    window.location=window.location;
}

// If you enable geolocate, post contains also lat,lon and callsign
// They are updated from geolocate callback at map.php 
function submitImage() {
    // Submit to upload.php
    uploadform.submit();
    // Capture what upload.php outputs to 'dummyframe' (filename) and use location
    // (if available) and callsign. So we have everything at hand to form "new image" 
    // message to other peers.
    iframeContentChange(document.getElementById("dummyframe"), function (payload) {
       if ( payload != "" ) {
            var notifyMessagePayload="Image sent";
            if ( lastKnownCoordinates ) {
            notifyMessagePayload = notifyMessagePayload + " with location";
            // Send imageMarker if we have location available
            var imgMsg = callSign + `|imageMarker|[`+lastKnownCoordinates.latitude+`,`+lastKnownCoordinates.longitude+`]|`+ payload + '\n';
            
            // TODO: Handle meshtasticMsgSocket.send( );
            // reticulumMsgSocket.send( imgMsg );
            sendRetiCulumAndMeshtasticMessage(imgMsg);
            
            }
            notifyMessage(notifyMessagePayload, 5000);
       }
    });
    
}

// Monitoring dummyframe content change, based on:
// https://gist.github.com/hdodov/a87c097216718655ead6cf2969b0dcfa
function iframeContentChange(iframe, callback) {
    var lastDispatched = null;
    var dispatchChange = function () {
        if ( iframe.contentWindow.document.body !== null ) {
            var newContent = iframe.contentWindow.document.body.innerHTML;
            if (newContent !== lastDispatched) {
                callback(newContent);
                lastDispatched = newContent;
                iframe.contentWindow.document.body.innerHTML="";
            }
        }
    };
    var unloadHandler = function () {
        // Timeout needed because the URL changes immediately after
        // the `unload` event is dispatched.
        setTimeout(dispatchChange, 0);
    };
    function attachUnload() {
        // Remove the unloadHandler in case it was already attached.
        // Otherwise, there will be two handlers, which is unnecessary.
        iframe.contentWindow.removeEventListener("unload", unloadHandler);
        iframe.contentWindow.addEventListener("unload", unloadHandler);
    }
    iframe.addEventListener("load", function () {
        attachUnload();
        // Just in case the change wasn't dispatched during the unload event...
        dispatchChange();
    });
    attachUnload();
}

//
// Image markers
// 
// upload.php creates two files:
// '1700964684_-_-_HAME-21_Screenshot from 2023-11-25 07-58-21.png'
// '1700964684_-_-_HAME-21_Screenshot from 2023-11-25 07-58-21_thumb.png'
// 
function createImageMarker(from,lat,lon,filename) {
        var markerId=filename;
        
        // Display thumbnail and add modal class and id
        // markerStatus contains img src (thumbnail) and img alt (full size)
        var filename_without_extension=filename.slice(0, -4); 
        var filename_extension=filename.slice(-4); // .png
        var filename_thumb=filename_without_extension+"_thumb"+filename_extension;        
        var markerStatus = "<img class='myImages' id='myImg' src='../uploads/" + filename_thumb + "' alt='../uploads/" + filename+ "' width=100px;>";
        
        if ( !imageMarker[markerId] ) {
            var ll = new maplibregl.LngLat(lon, lat);	
            imageMarkerPopup[markerId] = new maplibregl.Popup({ offset: 25, closeOnClick: false,  }).setHTML(markerStatus);
            imageMarker[markerId] = new maplibregl.Marker({
                color: "#2EAA2E",
                draggable: false
                })
                .setLngLat( ll )
                .setPopup(imageMarkerPopup[markerId])
                .addTo(map);
            imageMarker[markerId].togglePopup();
        }
        // If marker is already created with 'markerId' - update location + markerStatus + symbol
        // NOTE: This is not in use
        if ( imageMarker[markerId] ) {
            var ll = new maplibregl.LngLat(lon, lat);
            imageMarker[markerId].remove();
            // Create marker DOM
            imageMarker[markerId] = new maplibregl.Marker({
                color: "#2EAA2E",
                draggable: false
                })
                .setLngLat( ll )
                .setPopup(imageMarkerPopup[markerId])
                .addTo(map);
            imageMarkerPopup[markerId].setHTML(markerStatus);
            if ( !imageMarkerPopup[markerId].isOpen() ) {
                imageMarker[markerId].togglePopup();
            }
        }
}

//
// Sensor markers
//
function createSensorMarker(lat,lon,markerId,markerStatus,sensorSymbol) {
    
    if ( sensorMarker[markerId] && markerStatus == "delete" ) {
        sensorMarker[markerId].remove();
    } else {
    
        if ( !sensorMarker[markerId] ) {
            var ll = new maplibregl.LngLat(lon, lat);	
            sensorMarkerPopup[markerId] = new maplibregl.Popup({ offset: 25, closeOnClick: false,  }).setHTML(markerStatus);
            const sensoreMarkerGraph = new ms.Symbol(sensorSymbol, { size:30 });
            var sensoreMarkerGraphDom = sensoreMarkerGraph.asDOM();
            // Use milsymbol as marker
            sensorMarker[markerId] = new maplibregl.Marker({
                color: "#2EAA2E",
                element: sensoreMarkerGraphDom,
                draggable: false
                })
                .setLngLat( ll )
                .setPopup(sensorMarkerPopup[markerId])
                .addTo(map);
            sensorMarker[markerId].togglePopup();
        }
        // If marker is already created with 'markerId' - update location + markerStatus + symbol
        if ( sensorMarker[markerId] ) {
            var ll = new maplibregl.LngLat(lon, lat);
            sensorMarker[markerId].remove();
            // Create marker DOM
            const sensoreMarkerGraph = new ms.Symbol(sensorSymbol, { size:30 });
            var sensoreMarkerGraphDom = sensoreMarkerGraph.asDOM();
            sensorMarker[markerId] = new maplibregl.Marker({
                color: "#2EAA2E",
                element: sensoreMarkerGraphDom,
                draggable: false
                })
                .setLngLat( ll )
                .setPopup(sensorMarkerPopup[markerId])
                .addTo(map);
            sensorMarkerPopup[markerId].setHTML(markerStatus);
            if ( !sensorMarkerPopup[markerId].isOpen() ) {
                sensorMarker[markerId].togglePopup();
            }
        }
    }
}

//
// Marker from geolocation
//
function createTrackMarkerFromMessage(lon, lat, msgFrom, msgMessage) {

    if ( !trackMessageMarkers[msgFrom] ) {        
        notifyMessage("Creating marker for: " + msgFrom, 5000);
        trackMessageMarkerGraph.setOptions({ type: msgFrom });
        trackMessageMarkerGraphDom = trackMessageMarkerGraph.asDOM();
        var ll = new maplibregl.LngLat(lon, lat);
        trackMessageMarkers[msgFrom] = new maplibregl.Marker({
		element: trackMessageMarkerGraphDom,
		draggable: false
		})
		.setLngLat( ll )
		.addTo(map);
    }
    
    // Update location of already created markers 
    if ( trackMessageMarkers[msgFrom] ) {
        
         if ( msgMessage.includes("Stopped") ) {
            notifyMessage("Tracking stopped: " + msgFrom, 5000);
        }
        trackMessageMarkers[msgFrom].remove();
        // Get time
        var date = new Date();        
        var hours;
        var minutes;
        var seconds;
        if ( date.getHours() < 10 ) {
            hours = "0" + date.getHours();
        } else {
            hours = date.getHours();
        }
        if ( date.getMinutes() < 10 ) {
            minutes = "0" + date.getMinutes();
        } else {
            minutes = date.getMinutes();
        }
         if ( date.getSeconds() < 10 ) {
            seconds = "0" + date.getSeconds();
        } else {
            seconds = date.getSeconds();
        }
        var timeStamp = hours + ":" + minutes + ":"+ seconds;
        // Update marker options
        trackMessageMarkerGraph.setOptions({ staffComments: timeStamp  });
        trackMessageMarkerGraph.setOptions({ additionalInformation: msgMessage  });
        trackMessageMarkerGraph.setOptions({ type: msgFrom });
        trackMessageMarkerGraphDom = trackMessageMarkerGraph.asDOM();
        // Get new position
        var ll = new maplibregl.LngLat(lon, lat);
        // Add marker to map
        // TODO: Calculate offset based on getAnchor(), see: https://www.spatialillusions.com/milsymbol/documentation.html#getanchor
        trackMessageMarkers[msgFrom] = new maplibregl.Marker({
            element: trackMessageMarkerGraphDom,
            draggable: false,
            offset: [30, 0]
            })
            .setLngLat( ll )
            .addTo(map);
    }  
}

//
// Create marker from incoming Message
//
function createMarkerFromMessage(index, lon, lat, markerText) {
	var ll = new maplibregl.LngLat(lon, lat);	
	// create the popup
	mapPinMarkerPopup[index] = new maplibregl.Popup({ offset: 35, closeOnClick: false,  }).setHTML(markerText);
	// create DOM element for the marker TODO: Array?
	var el = document.createElement('div');
	el.id = 'marker';
	mapPinMarker[index] = new maplibregl.Marker({
		color: "#FF515E",
		draggable: false
		})
		.setLngLat( ll )
		.setPopup(mapPinMarkerPopup[index])
		.addTo(map);
	mapPinMarker[index].togglePopup();
}

//
// Create new dragable marker and push it to array for later use
//
function newDragableMarker() {
	var newPopup = new maplibregl.Popup({ offset: 35, closeOnClick: false, }).setText('popup'+ Date.now());		
	var markerD = new maplibregl.Marker({
		draggable: 'true',
		id: 'c1'
	})
	.setLngLat( map.getCenter().toArray() )
	.setPopup(newPopup)
	.addTo(map);
	markerD._element.id = "dM-" + Date.now();
	// inline dragend function
	markerD.on('dragend', () => {
        msgInput.value = "";
		var lngLat = markerD.getLngLat();
		var msgLatValue = String(lngLat.lat);
		var msgLonValue = String(lngLat.lng);	
		var templateValue = 'dropMarker|[' + msgLonValue.substr(0,8) + ',' + msgLatValue.substr(0,8) + ']|';
		msgInput.value = templateValue;
        document.getElementById("msgInput").focus();
		markerD.setPopup(new maplibregl.Popup().setHTML(templateValue)); // probably not needed
		lastDraggedMarkerId = markerD._element.id;
	});
	dragMarkers.push(markerD);
	dragPopups.push(newPopup);
}

function addPopupToMarker(popupText) {
	mapPinMarkerPopup.setText( popupText );
}

function eraseMsgLog() {
	document.getElementById('msgChannelLog').innerHTML = ""; 
}

function parse_query_string(query) {
  var vars = query.split("&");
  var query_string = {};
  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");
    var key = decodeURIComponent(pair.shift());
    var value = decodeURIComponent(pair.join("="));
    // If first entry with this name
    if (typeof query_string[key] === "undefined") {
      query_string[key] = value;
      // If second entry with this name
    } else if (typeof query_string[key] === "string") {
      var arr = [query_string[key], value];
      query_string[key] = arr;
      // If third or later entry with this name
    } else {
      query_string[key].push(value);
    }
  }
  return query_string;
}

// Local GPS marker animation
function animateLocalGpsMarker(timestamp) {		
    // localGpsMarker.remove();
    var lat = document.getElementById('lat_localgps').innerHTML;
    var lon = document.getElementById('lon_localgps').innerHTML; 
    var mode = document.getElementById('mode_localgps').innerHTML;
    var speed = document.getElementById('speed_localgps').innerHTML;
    var localGpsName = "Local GPS"; 
    var locationComment = speed + " km/h";
    milSymbolLocalGps.setOptions({ staffComments: locationComment });
    milSymbolLocalGps.setOptions({ commonIdentifier: "" });
    milSymbolLocalGps.setOptions({ type: localGpsName });
    milSymbolLocalGpsMarker = milSymbolLocalGps.asDOM(); 
    /*localGpsMarker = new maplibregl.Marker({
            element: milSymbolLocalGpsMarker
        });*/
    localGpsMarker.setLngLat([lat,lon]);
    localGpsMarker.addTo(map);
    requestAnimationFrame(animateLocalGpsMarker);
} 

// Send my GPS provided location over meshtastic msg channel when
// coordinates are clicked on top bar.
function sendMyGpsLocation() {
    var lat = document.getElementById('lat_localgps').innerHTML;
    var lon = document.getElementById('lon_localgps').innerHTML; 
    sendRetiCulumAndMeshtasticMessage ( callSign + `|trackMarker|` + lat + `,` + lon + `|GPS-snapshot` + '\n' );
    notifyMessage("Local GPS position sent as track marker", 5000);
}

//
// Highrate marker animation
//
function animateHighrateMarker(timestamp) {		
        // Experimental version
        if ( 1 ) {
            highrateMarker.remove();
            var lat = document.getElementById('lat_highrate').innerHTML;
            var lon = document.getElementById('lon_highrate').innerHTML; 
            var highrateName = document.getElementById('name_highrate').innerHTML;
            var locationComment = lat + "," + lon;
            milSymbolHighrate.setOptions({ type: highrateName });
            milSymbolHighrate.setOptions({ uniqueDesignation: locationComment }); 
            milSymHighrateMarker = milSymbolHighrate.asDOM(); 
            highrateMarker = new maplibregl.Marker({
                    element: milSymHighrateMarker
				});
            highrateMarker.setLngLat([lat,lon]);
            highrateMarker.addTo(map);
            requestAnimationFrame(animateHighrateMarker);
        }
        // Working stable:
        if( 0 ) {
            var lat = document.getElementById('lat_highrate').innerHTML;
            var lon = document.getElementById('lon_highrate').innerHTML; 
            highrateMarker.setLngLat([lat,lon]);
            // Ensure it's added to the map. This is safe to call if it's already added.
            highrateMarker.addTo(map);
            // Request the next frame of the animation. ,
            requestAnimationFrame(animateHighrateMarker);
        }
} 

// CoT target tail toggle
function toggleTail() {
	if (map.getLayer('route')) {
		hideTails();
	} else {
		showTails();
	}
}
// Add 'route' layer for LineString geojson display. 
// NOTE: Layer is added before 'drone' layer. 
// https://jsfiddle.net/brianssheldon/wm18a33d/27/
function showTails() {
	if (!map.getLayer('route')) {
		/* line string layer */
		map.addLayer({
		'id': 'route',
		'type': 'line',
		'source': 'drone',
		'layout': {
            'line-join': 'round',
            'line-cap': 'round'
        },
        'paint': {
            'line-color':  ['get', 'color'],
            'line-width': ['get', 'width'],
            'line-opacity': ['get', 'opacity']
            
		},
		'filter': ['==', '$type', 'LineString']
		},'drone');
        
        // Test labeling link lines with data from geojson
          map.addLayer({
            "id": "symbols",
            "type": "symbol",
            "source": "drone",
            "layout": {
              "symbol-placement": "line",
              "text-font": ["Open Sans Regular"],
              "text-field":  ['get', 'title'], 
              "text-size": ['get', 'text-size']
            },
            paint: {
              "text-color": ['get', 'text-color'],
              "text-halo-color":  ['get', 'text-halo-color'],
              "text-halo-width":  ['get', 'text-halo-width'],
              "text-halo-blur":  ['get', 'text-halo-blur']
            },
            filter: ['==', '$type', 'LineString']
          });
	}
}

function hideTails() {
	if (map.getLayer('route')) map.removeLayer('route'); 
}

// Options to change map style on fly.
// NOTE: Not in use, since style change loses symbols
function setDarkStyle() {
	map.setStyle("styles/style-v4-dark.json");
}
function setNormalStyle() {
	map.setStyle("styles/style-v4.json");
}

function centerMap(lat,lon) {
    map.flyTo({
        // These options control the ending camera position: centered at
        // the target, at zoom level 9, and north up.
        center: [lat,lon],
        zoom: 15,
        bearing: 0,
        // These options control the flight curve, making it move
        // slowly and zoom out almost completely before starting
        // to pan.
        speed: 0.8, // make the flying slow
        curve: 1,   // change the speed at which it zooms out

        // This can be any easing function: it takes a number between
        // 0 and 1 and returns another number between 0 and 1.
        easing (t) {
            return t;
        },
        // this animation is considered essential with respect to prefers-reduced-motion
        essential: true
    });
}

function zoomIn() {
	currentZoom = document.getElementById('zoomlevel').innerHTML;
	if ( currentZoom < 17 ) {
		currentZoom++;
		map.setZoom(currentZoom);
		document.getElementById('zoomlevel').innerHTML = currentZoom;
	}
}
function zoomOut() {
	currentZoom = document.getElementById('zoomlevel').innerHTML;
	if ( currentZoom > 1 ) {
		currentZoom--;
		map.setZoom(currentZoom);
		document.getElementById('zoomlevel').innerHTML = currentZoom;
	}
}

function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
};

// Support function to check video server presense on network
// TODO: hard coded IP of ZM instance still present
function checkVideoServer(cb){
	var img = new Image();
	img.onerror = function() {
		cb(false)
	}
	img.onload = function() {
		cb(true)
	}
	// Use fixed ZM image element as test point
	img.src = "http://192.168.5.97/zm/graphics/spinner.png?t=" + (+new Date);
}
function videoPanelsVisible(videoAvail) {
	var x = document.getElementById("leftVideo");
	var y = document.getElementById("rightVideo"); 
	if ( videoAvail == true ) {
		x.style.display = "";
		y.style.display = "";
	} else {
		x.style.display = "none";
		y.style.display = "none";
		// Instead of just hide, we can also stop streams (for bw reasons)
		// Note that resume needs page reload.
		document.getElementById("cam1").src="";
		document.getElementById("cam2").src="";
		document.getElementById("cam3").src="";
		document.getElementById("cam4").src="";
		document.getElementById("cam5").src="";
		document.getElementById("cam6").src="";
		document.getElementById("cam7").src="";
		document.getElementById("cam8").src="";
		document.getElementById("cam9").src="";
		document.getElementById("cam10").src="";
	}
}

// 
// This will update image based on JSON parsing every 2 s 
// Only dynamic field is dtg: sTimeStamp
// 
// NOTE: 
// * We have ageSeconds - but needs to illustrate it still
// * Simulation targets do not provide time
//
function updateImage(sName, sTimeStamp, ageSeconds) {
    // SFGAUCR-----	Anticipated
	// SFGPUCR----- Present
	// SFGCUCR----- Fully capable
	// SFGDUCR----- Damaged
    if ( ageSeconds < 60 ) {
		symbolCode = "SFGCUCR-----"; 
	} else {
		symbolCode = "SFGDUCR-----";
	}
	// NOTE: This is override for simulation    
    // symbolCode = "SFGPUCR-----";
	var updatedSym = new ms.Symbol(symbolCode, { size:20,
		dtg: "",
		staffComments: "".toUpperCase(),
		additionalInformation: "".toUpperCase(),
		combatEffectiveness: "".toUpperCase(),
		type: "",
		padding: 5
	});
	var updateCanvasElement = updatedSym.asCanvas();
	var updateSymoffset = 0 - updatedSym.getAnchor().x;				
	var updatedImg = new Image();
	updatedImg.src = updateCanvasElement.toDataURL();
	if ( map.hasImage( sName ) ) {
        // Update would be better, but size change
        // map.updateImage( sName, updatedImg );
        map.removeImage( sName );
        map.addImage( sName, updatedImg );
	}
}	


// Create image function, creates image element initially. 
// TODO: Size mismatch is an issue still.  symbolSize
function createImage(sName) {
    var updatedSym = new ms.Symbol("SFGPUCR-----", { size:20,
        dtg: "",
        staffComments: "".toUpperCase(),
        additionalInformation: "".toUpperCase(),
        combatEffectiveness: "READY".toUpperCase(),
        type: "",
        padding: 5
	});
	var updateCanvasElement = updatedSym.asCanvas();
    // TODO: On first call, we get this
    // "Uncaught DOMException: Index or size is negative or greater than the allowed amount"
    // Is this firefox issue?
    var updatedImg = new Image();
	updatedImg.src = updateCanvasElement.toDataURL();
    map.addImage(sName,updatedImg );
}

function getCoordinatesToClipboard() {
	var copyText = document.getElementById('lat').innerHTML + "," + document.getElementById('lon').innerHTML;
	copyToClipboard(copyText);
    document.getElementById('lat').innerHTML = "";
    document.getElementById('lon').innerHTML = "";
    document.getElementById('coordinateComma').innerHTML = "";
    document.getElementById("copyNotifyText").innerHTML = "Copied to clipboard!";
    fadeOut( document.getElementById("mapClickLatlonSection"), 1400 );
} 

function changeLanguage(language) {
    /* Complete this property list */
    map.setLayoutProperty('places_country', 'text-field', ['get',`name:${language}` ]);
    map.setLayoutProperty('places_subplace', 'text-field', ['get',`name:${language}` ]);
    map.setLayoutProperty('places_locality', 'text-field', ['get',`name:${language}` ]);
    map.setLayoutProperty('places_region', 'text-field', ['get',`name:${language}` ]);    
    map.setLayoutProperty('roads_labels_minor', 'text-field', ['get',`name:${language}` ]);
    map.setLayoutProperty('roads_labels_major', 'text-field', ['get',`name:${language}` ]);
    closeLanguageSelectBox();
}

//
// Example from maplibre-gl pulsedot
//
function addDot(lon,lat) {
    const size = 100;
    const pulsingDot = {
        width: size,
        height: size,
        data: new Uint8Array(size * size * 4),

        // get rendering context for the map canvas when layer is added to the map
        onAdd () {
            const canvas = document.createElement('canvas');
            canvas.width = this.width;
            canvas.height = this.height;
            this.context = canvas.getContext('2d');
        },
        // called once before every frame where the icon will be used
        render () {
            const duration = 1000;
            const t = (performance.now() % duration) / duration;
            const radius = (size / 2) * 0.3;
            const outerRadius = (size / 2) * 0.7 * t + radius;
            const context = this.context;
            // draw outer circle
            context.clearRect(0, 0, this.width, this.height);
            context.beginPath();
            context.arc(
                this.width / 2,
                this.height / 2,
                outerRadius,
                0,
                Math.PI * 2
            );
            context.fillStyle = `rgba(255, 200, 200,${1 - t})`;
            context.fill();
            // draw inner circle
            context.beginPath();
            context.arc(
                this.width / 2,
                this.height / 2,
                radius,
                0,
                Math.PI * 2
            );
            context.fillStyle = 'rgba(255, 100, 100, 1)';
            context.strokeStyle = 'white';
            context.lineWidth = 2 + 4 * (1 - t);
            context.fill();
            context.stroke();
            // update this image's data with data from the canvas
            this.data = context.getImageData(
                0,
                0,
                this.width,
                this.height
            ).data;
            // continuously repaint the map, resulting in the smooth animation of the dot
            map.triggerRepaint();
            // return `true` to let the map know that the image was updated
            return true;
        }
    };
    // if (!map.hasImage('pulsing-dot')) 
    map.addImage('pulsing-dot', pulsingDot, {pixelRatio: 2});
    
    // map.removeSource('pulsingpoints');
    map.addSource('pulsingpoints', {
        'type': 'geojson',
        'data': {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [lon,lat]
                    }
                }
            ]
        }
    });
    // if (map.getLayer('pulsepointslayer')) map.removeLayer('pulsepointslayer');
    map.addLayer({
        'id': 'pulsepointslayer',
        'type': 'symbol',
        'source': 'pulsingpoints',
        'layout': {
            'icon-image': 'pulsing-dot'
        }
    });
}

function removeDot() {
    if (map.getImage("pulsing-dot")) {
        map.removeImage('pulsing-dot');
    }
    if (map.getLayer("pulsepointslayer")) {
        map.removeLayer('pulsepointslayer');
    }
    if (map.getSource("pulsingpoints")) {
        map.removeSource('pulsingpoints');
    }
}

// Nice example from stackoverflow how to capture coordinates on click to clipboard
// [1] https://stackoverflow.com/questions/51805395/navigator-clipboard-is-undefined
function copyToClipboard(textToCopy) {
	// navigator clipboard api needs a secure context (https)
	if (navigator.clipboard && window.isSecureContext) {
		// navigator clipboard api method'
		return navigator.clipboard.writeText(textToCopy);
	} else {
		// text area method
		let textArea = document.createElement("textarea");
		textArea.value = textToCopy;
		// make the textarea out of viewport
		textArea.style.position = "fixed";
		textArea.style.left = "-999999px";
		textArea.style.top = "-999999px";
		document.body.appendChild(textArea);
		textArea.focus();
		textArea.select();
		return new Promise((res, rej) => {
			// here the magic happens
			document.execCommand('copy') ? res() : rej();
			textArea.remove();
		});
	}
}

//
// Generate random callsign for demo
//
function genCallSign() {
	var	min=0;
	var max=11;
	var nummin=10
	var nummax=50
	const csItems = ["ASTRA","BLACK","GOOFY","HAME","KAYA","SHOG","TIGER","VAN","WOLF","GOAT","IRON","NOMAD"];
	var csIndex = Math.floor(Math.random() * (max - min + 1) ) + min;
	var numValue = Math.floor(Math.random() * (nummax - nummin + 1) ) + nummin;
	var callSign=csItems[csIndex] + "-" + numValue;
	return callSign; 
}

//
// Dialog functions
//
function openLanguageSelectBox() {
    console.log("opening language");
    fadeIn(languageSelectDialogDiv,100);
    console.log("opening language 2");
}
function closeLanguageSelectBox() {
    fadeOut(languageSelectDialogDiv,100);
}
function openCoordinateSearchEntryBox() {
    document.getElementById('coordinateInput').value="";
    fadeIn(coordinateEntryBoxDiv,100);
    document.getElementById("coordinateInput").focus();
}
function closeCoordinateSearchEntryBox() {
    fadeOut(coordinateEntryBoxDiv,100);
}
function openCallSignEntryBox() {
    fadeIn(callSignEntryBoxDiv,200);
}

function closeCallSignEntryBox() {
    fadeOut(callSignEntryBoxDiv,200);
    var newCallSign = document.getElementById('myCallSign').value; 
    document.getElementById('myCallSign').value = newCallSign;
    document.getElementById('callSignDisplay').innerHTML = newCallSign;
    newCallSignWithLifeFeed = newCallSign + "\n";
    
    // Save changes to "/opt/edgemap-persist/callsign.txt"
    fetch('save_callsign.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: newCallSignWithLifeFeed })
    })
    .then(response => response.text())
    .then(data => {
        console.log('Data saved:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
    
}

function openRadioList() {
    if ( logDiv.style.display == "" || logDiv.style.display !== "inline-block"  ) {
        if ( radiolistblockDiv.style.display !== "inline-block" ) {
            fadeIn(radiolistblockDiv ,200);
            fadeOut(radioNotifyDotDiv,200);
        }
    }
}

function closeRadioList() {
    if (logDiv.style.display !== "inline-block" ) {
        fadeOut(radiolistblockDiv ,200);
    }
}

function openReticulumList() {
    if ( logDiv.style.display == "" || logDiv.style.display !== "inline-block"  ) {
        if ( reticulumListblockDiv.style.display !== "inline-block" ) {
            fadeIn(reticulumListblockDiv ,200);
            fadeOut(radiolistblockDiv,200);
        }
    }
}

function closeReticulumList() {
    if (logDiv.style.display !== "inline-block" ) {
        fadeOut(reticulumListblockDiv ,200);
    }
}


function openMessageEntryBox() {
    const canVibrate = window.navigator.vibrate
    if (canVibrate) window.navigator.vibrate(100)
    if ( logDiv.style.display == "" || logDiv.style.display == "none" )
    {
        const canVibrate = window.navigator.vibrate
        if (canVibrate) window.navigator.vibrate([200, 100, 200]);
        fadeIn(logDiv,200);
        // fadeOut(zoomDiv,200);
        // fadeOut(sensorDiv,200);
        fadeOut(bottomBarDiv,200);
        // fadeOut(cameracontrol,200);
        // fadeOut(userlistbuttonDiv ,200);
        // fadeOut(radiolistbuttonDiv ,200);
        fadeOut(radiolistblockDiv ,200);
        // fadeOut(videoconferenceButton ,200);
        fadeOut(reticulumListblockDiv ,200);
        // fadeOut(reticulumListButtonDiv ,200);
        // fadeOut(manualGpsbuttonDiv ,200);
    }
    document.getElementById("msgInput").focus();
}

function closeMessageEntryBox() {
    console.log("closeMessageEntryBox()");
    // return; // new menu debug
    if ( logDiv.style.display == "" )
    {
      fadeIn(logDiv,200);
      /*
        fadeOut(zoomDiv,200);
        fadeOut(sensorDiv,200);
        fadeOut(cameracontrol,200);
        fadeOut(userlistbuttonDiv ,200);
        fadeOut(videoconferenceButton ,200);
        fadeOut(reticulumListblockDiv ,200);
        fadeOut(reticulumListButtonDiv ,200);
        fadeOut(deliveryStatusDiv ,200);
        */
       // fadeOut(manualGpsbuttonDiv ,200);
    } else {
      if (logDiv.style.display !== "none" ) {      
        fadeOut(logDiv,200);
        fadeOut(deliveryStatusDiv,200); 
        fadeIn(bottomBarDiv,200);
        /*fadeIn(zoomDiv,200);
        fadeIn(sensorDiv,200);
        fadeIn(bottomBarDiv,200);
        fadeIn(cameracontrol,200);
        fadeIn(userlistbuttonDiv ,200);
        fadeIn(radiolistbuttonDiv ,200);
        fadeIn(videoconferenceButton ,200);
        // fadeIn(reticulumListblockDiv ,200);
        fadeIn(reticulumListButtonDiv ,200);
        fadeIn(manualGpsbuttonDiv ,200); */
        
      } else {
        fadeIn(logDiv,200);
        /*
        fadeOut(zoomDiv,200);
        fadeOut(sensorDiv,200);
        fadeOut(cameracontrol,200);
        fadeOut(userlistbuttonDiv,200);
        fadeOut(radiolistbuttonDiv ,200);
        fadeOut(radiolistblockDiv ,200);
        fadeOut(videoconferenceButton ,200);
        fadeOut(reticulumListblockDiv ,200);
        fadeOut(reticulumListButtonDiv ,200);
        fadeOut(deliveryStatusDiv ,200);
        // fadeOut(manualGpsbuttonDiv ,200);
        */
        
      }
    }
}

var scrolling = function(e, c) {
  e.scrollIntoView();
  if (c < 5) setTimeout(scrolling, 300, e, c + 1);
};
var ensureVisible = function(e) {
  setTimeout(scrolling, 300, e, 0);
};


// fade in/out experiment
function fadeInTo09( elem, ms,opacityTarget )
{
  if( ! elem )
    return;
  elem.style.opacity = 0;
  elem.style.filter = "alpha(opacity=0)";
  elem.style.display = "inline-block";
  elem.style.visibility = "visible";

  if( ms )
  {
    var opacity = 0;
    var timer = setInterval( function() {
      opacity += 50 / ms;
      if( opacity >= opacityTarget )
      {
        clearInterval(timer);
        opacity = opacityTarget;
      }
      elem.style.opacity = opacity;
      elem.style.filter = "alpha(opacity=" + opacity * 100 + ")";
    }, 50 );
  }
  else
  {
    elem.style.opacity = opacityTarget;
    elem.style.filter = "alpha(opacity=0.9)";
  }
}

function fadeOutFrom09( elem, ms,opacityTarget )
{
  if( ! elem )
    return;

  if( ms )
  {
    var opacity = opacityTarget;
    var timer = setInterval( function() {
      opacity -= 50 / ms;
      if( opacity <= 0 )
      {
        clearInterval(timer);
        opacity = 0;
        elem.style.display = "none";
        elem.style.visibility = "hidden";
      }
      elem.style.opacity = opacity;
      elem.style.filter = "alpha(opacity=" + opacity * 100 + ")";
    }, 50 );
  }
  else
  {
    elem.style.opacity = 0;
    elem.style.filter = "alpha(opacity=0)";
    elem.style.display = "none";
    elem.style.visibility = "hidden";
  }
}

// fade in/out experiment
function fadeIn( elem, ms )
{
  if( ! elem )
    return;

  elem.style.opacity = 0;
  elem.style.filter = "alpha(opacity=0)";
  elem.style.display = "inline-block";
  elem.style.visibility = "visible";

  if( ms )
  {
    var opacity = 0;
    var timer = setInterval( function() {
      opacity += 50 / ms;
      if( opacity >= 1 )
      {
        clearInterval(timer);
        opacity = 1;
      }
      elem.style.opacity = opacity;
      elem.style.filter = "alpha(opacity=" + opacity * 100 + ")";
    }, 50 );
  }
  else
  {
    elem.style.opacity = 1;
    elem.style.filter = "alpha(opacity=1)";
  }
}

function fadeOut( elem, ms )
{
  if( ! elem )
    return;

  if( ms )
  {
    var opacity = 1;
    var timer = setInterval( function() {
      opacity -= 50 / ms;
      if( opacity <= 0 )
      {
        clearInterval(timer);
        opacity = 0;
        elem.style.display = "none";
        elem.style.visibility = "hidden";
      }
      elem.style.opacity = opacity;
      elem.style.filter = "alpha(opacity=" + opacity * 100 + ")";
    }, 50 );
  }
  else
  {
    elem.style.opacity = 0;
    elem.style.filter = "alpha(opacity=0)";
    elem.style.display = "none";
    elem.style.visibility = "hidden";
  }
}

function isHidden(el) {
    return (el.offsetParent === null)
}

// 
// Shared drag symbol updates
// 
function onDrag() {
    const lngLat = dragMarker.getLngLat();
    var dragLocationPayload = callSign + `|dragMarker|${lngLat.lng},${lngLat.lat}|dragged` + '\n';
    // NOTE: On meshtastic branch, we disable drag delivery over messaging channel
    // reticulumMsgSocket.send( dragLocationPayload ); 
    // TODO: Handle meshtasticMsgSocket.send( );
}
    
function onDragEnd() {
    const lngLat = dragMarker.getLngLat();
    var dragLocationPayload = callSign + `|dragMarker|${lngLat.lng},${lngLat.lat}|released` + '\n';
    // NOTE: On meshtastic  & reticulum branch, we disable drag delivery over messaging channel
    // console.log("Drag: ", dragLocationPayload);
    // reticulumMsgSocket.send( dragLocationPayload );
    // TODO: Handle meshtasticMsgSocket.send( );
}

//
// Show features for debugging, if you enabled this
// change display: [block/none] on edgemap-m.css: #features 
// 
function showFeatures(e)
{
        const features = map.queryRenderedFeatures(e.point);
        // Limit the number of properties we're displaying for
        // legibility and performance
        const displayProperties = [
            'type',
            'properties',
            'id',
            'layer',
            'source',
            'sourceLayer',
            'state'
        ];
        const displayFeatures = features.map((feat) => {
            const displayFeat = {};
            displayProperties.forEach((prop) => {
                displayFeat[prop] = feat[prop];
            });
            return displayFeat;
        });
        document.getElementById('features').innerHTML = JSON.stringify(
            displayFeatures,
            null,
            2
        );
}

function toggleHillShadow() {
    if ( isHidden(logDiv) ) {
        const visibility = map.getLayoutProperty(
            "hills",
            'visibility'
        );
        if (visibility === 'visible') {
            map.setLayoutProperty("hills", 'visibility', 'none');
            map.setTerrain(null);
        } else {
            map.setLayoutProperty("hills", 'visibility', 'visible');
            map.setTerrain({ source: 'terrainSource' });
        }   
    }
}

//
// https://stackoverflow.com/questions/11475146/javascript-regex-to-validate-gps-coordinates
//
const regexLat = /^(-?[1-8]?\d(?:\.\d{1,18})?|90(?:\.0{1,18})?)$/;
const regexLon = /^(-?(?:1[0-7]|[1-9])?\d(?:\.\d{1,18})?|180(?:\.0{1,18})?)$/;

function check_lat_lon(lat, lon) {
  let validLat = regexLat.test(lat);
  let validLon = regexLon.test(lon);
  return (validLat && validLon);
}




// 
// Loads possibly persisted call sign at:
// /opt/edgemap-persist/callsign.txt
//
function loadCallSign() {
    fetch('load_callsign.php')
    .then(response => response.json())
    .then(data => {
        callSign = data.data;
        document.getElementById('myCallSign').value = data.data;
        document.getElementById('callSignDisplay').innerHTML = data.data;
        return data.data;
    })
    .catch(error => {
        console.error('Error:', error);
        return;
    });
}

// 
// Work in progress
//
// TODO: Erase sensors. Now we need to erase file under /opt/edgemap-persist/
// 

function sensorDefine() {
    
    var sensorDescription = document.getElementById('sensorNameInput').value;
    var sensorLocation = document.getElementById('sensorLat').innerHTML + "," + document.getElementById('sensorLon').innerHTML;
    console.log("sensorDefine() ",sensorToBeCreated, sensorDescription,sensorLocation);
    
    fetch('save_sensor.php?id='+sensorToBeCreated, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: [sensorDescription,',',sensorLocation] })
    })
    .then(response => response.text())
    .then(data => {
        console.log('Sensor created');
    })
    .catch(error => {
        console.error('Sensor create error:', error);
    });
    keyEventListener=1;
    unknownSensorCreateInProgress=0;
    sensorClose();
    
}
function sensorClose() {
    const elementOpacity=0.8;
    fadeOutFrom09(document.getElementById("sensorNotify"),400,elementOpacity);
    document.getElementById('sensorLat').innerHTML = "";
    document.getElementById('sensorLon').innerHTML = "";
    document.getElementById('sensorLatLonComma').innerHTML = "";
    document.getElementById("sensor-create-input").style.display = "none";
    document.getElementById("sensorNameInput").value = ""; 
}

function sensorNotifyMessage(message, timeout) {
    const elementOpacity=0.8;
    fadeInTo09(document.getElementById("sensorNotify") ,400,elementOpacity);
    document.getElementById("sensor-define-button").style.display = "none";
    document.getElementById("sensor-create-input").style.display = "none";
    document.getElementById("sensorMessage").innerHTML = message;
    if( timeout > 0 ) {
        setTimeout(() => {
            fadeOutFrom09(document.getElementById("sensorNotify"),400,elementOpacity);
        }, timeout);
    }
}

function unknownSensorNotifyMessage(message,id,timeout) {
    const elementOpacity=0.8;
    fadeInTo09(document.getElementById("sensorNotify") ,400,elementOpacity);
    document.getElementById("sensorMessage").innerHTML = message;
    document.getElementById("sensor-define-button").style.display = "block";
    document.getElementById('sensorLat').innerHTML = "";
    document.getElementById('sensorLon').innerHTML = "";
    document.getElementById('sensorLatLonComma').innerHTML = "";
    document.getElementById('sensor-create-input-placeholder').style.display = "block";
    document.getElementById('sensor-create-input-placeholder').innerHTML = "Click on map to create new";
    document.getElementById("sensor-create-input").style.display = "none"; 
    // Pass sensor ID with global variable
    sensorToBeCreated = id;
    keyEventListener=0;
    unknownSensorCreateInProgress=1;
    
    if (timeout > 0 ) {
        setTimeout(() => {
                fadeOut(document.getElementById("sensorNotify") ,400);
        }, timeout);
    }
}

// event:   0 = alarm, 1 = periodic notify
function loadSensor(id, event, state) {
    
    // Alarm
    if (event == 0) {
        fetch('load_sensor.php?id=' + id )
        .then(response => response.json())
        .then(data => {
            if ( data.data == "no-sensor" ) {
                unknownSensorNotifyMessage( "Unknown sensor alarm: "+id,id, 0);
            } else {
                const sensorDataArray = data.data.split(",");
                addSensorIcon(sensorDataArray[2],sensorDataArray[1],sensorDataArray[0]);
                sensorNotifyMessage( "Sensor alarm: " +  sensorDataArray[0] + "<br>" + sensorDataArray[1] + "," + sensorDataArray[2], 0);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            return 0;
        });
    }
    
    // Periodic
    if (event == 1) {
        fetch('load_sensor.php?id=' + id )
        .then(response => response.json())
        .then(data => {
            if ( data.data == "no-sensor" ) {
                sensorNotifyMessage( "Periodic notify: unknown sensor: ", 5000);
            } else {
                const sensorDataArray = data.data.split(",");
                sensorNotifyMessage( "Periodic notify from: " + sensorDataArray[0] + "<br>" + sensorDataArray[1] + "," + sensorDataArray[2], 5000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            return 0;
        });
    }
}

// Work in progress: This supports only one sensor at the moment.
async function addSensorIcon(lon,lat,sensorText) {
    
    if ( ! map.getLayer('sensorIconLayer') ) {
        image = await map.loadImage('img/sensor-icon.png');
        map.addImage('sensor-icon', image.data);
        map.addSource('sensorPoint', {
            'type': 'geojson',
            'data': {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [lon, lat]
                        }
                    }
                ]
            }
        });
        
        map.addLayer({
            'id': 'sensorIconLayer',
            'type': 'symbol',
            'source': 'sensorPoint',
            'layout': {
                'icon-image': 'sensor-icon',
                'icon-size': 0.35,
                'text-font': ['Open Sans Regular'],
                'text-size': 12,
                'text-anchor': 'top',
                'text-offset': [0,1],
                'text-transform': "uppercase",
                'text-letter-spacing': 0.10,
                'text-field': sensorText
            },
            "paint": {
                "text-color": "#F02",
                "text-halo-color": "#fFF",
                "text-halo-width": 2
            },
        });
        map.flyTo({
            center: [lon,lat],
            zoom: 17,
            speed: 0.6,
            curve: 1,
            essential: true
        });
    } else {
        // Sensor is created, let's update just detection counter if multiple alarms arrives
        var sensorTextField = map.getLayoutProperty('sensorIconLayer', 'text-field');
        const sensorTextArray = sensorTextField.split("x");
        if ( sensorTextArray[1] ) {
            var count=sensorTextArray[1];
            count++;
            var setSensorTextField = sensorText + ' x ' + count;
            map.setLayoutProperty('sensorIconLayer', 'text-field', setSensorTextField);
        } else {
            var count=2;
            var setSensorTextField = sensorText + ' x ' + count;
            map.setLayoutProperty('sensorIconLayer', 'text-field', setSensorTextField);
        }
    }
}

function removeSensorIcon() {
    if (map.getImage("sensor-icon")) {
        map.removeImage('sensor-icon');
    }
    if (map.getLayer("sensorIconLayer")) {
        map.removeLayer('sensorIconLayer');
    }
    if (map.getSource("sensorPoint")) {
        map.removeSource('sensorPoint');
    }
}

// manual location manualLocationNotify
function setManualLocationNotifyMessage() {
    message="Set your location manually";
    const elementOpacity=0.8;
    fadeInTo09(document.getElementById("manualLocationNotify") ,400,elementOpacity);
    document.getElementById("manualLocation-Message").innerHTML = message;
    document.getElementById("manualLocation-define-button").style.display = "block";
    document.getElementById('manualLocation-Lat').innerHTML = "";
    document.getElementById('manualLocation-Lon').innerHTML = "";
    document.getElementById('manualLocation-LatLonComma').innerHTML = "";
    document.getElementById('manualLocation-create-input-placeholder').style.display = "block";
    document.getElementById('manualLocation-create-input-placeholder').innerHTML = "Click on map to pick location";
    document.getElementById("manualLocation-create-input").style.display = "none"; 
    keyEventListener=0;
    manualLocationCreateInProgress=1;
}

function manualLocationSet() {
    var manualLocationValue = document.getElementById('manualLocation-Lat').innerHTML + "," + document.getElementById('manualLocation-Lon').innerHTML;
    fetch('save_manual_location.php', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: [manualLocationValue] })
    })
    .then(response => response.text())
    .then(data => {
        console.log('Position saved!');
    })
    .catch(error => {
        console.error('Position save error:', error);
    });
    keyEventListener=1;
    unknownSensorCreateInProgress=0;
    manualLocationClose();
}

function manualLocationErase() {
    
    fetch('erase_manual_location.php', {
        method: 'GET'
    })
    .then(response => response.text())
    .then(data => {
        console.log('Manual location erased');
    })
    .catch(error => {
        console.error('Manual location erase error:', error);
    });
    keyEventListener=1;
    unknownSensorCreateInProgress=0;
    manualLocationClose();
}

function manualLocationClose() {
    const elementOpacity=0.8;
    fadeOutFrom09(document.getElementById("manualLocationNotify"),400,elementOpacity);
    document.getElementById('manualLocation-Lat').innerHTML = "";
    document.getElementById('manualLocation-Lon').innerHTML = "";
    document.getElementById('manualLocation-LatLonComma').innerHTML = "";
    document.getElementById("manualLocation-create-input-placeholder").style.display = "none";
}


function clickSendImageForm() {
    console.log("clickSendImageForm()");
    console.log("We need to re-design image upload, because usage model has changed a lot.");
    // document.getElementById("fileToUpload").click();
}

function submitCoordinateSearch() {
    let inputValue = document.getElementById('coordinateInput').value;
    const coordValue = inputValue.split(",");
    console.log("AddDot: ",coordValue[1],coordValue[0]);
    addDot(coordValue[1],coordValue[0]);
    closeCoordinateSearchEntryBox();
    document.getElementById('coordinateInput').value="";   
}

//
// Place holder function to implement proper control towards system
// 
function systemControl(action) {
    // console.log("systemControl: ", action);
    page_url = 'control.php?id=' + action;
    fetch(page_url) 
        .then(response => response.text()) 
        .then(data => {
            // console.log("returned data: ", data);
            notifyMessage(data, 10000);
        })
        .catch(error => console.error('Error loading control page:', error));
    
}





