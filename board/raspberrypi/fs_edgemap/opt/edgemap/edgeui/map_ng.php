<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>EdgeMap</title>
    <meta name="viewport" content="initial-scale=1,maximum-scale=1,user-scalable=no" />
    <script src="js/maplibre-gl.js"></script>
    <link href="js/maplibre-gl.css" rel="stylesheet" />
    <script src="protomaps-js/pmtiles.js"></script>
    <script src="js/milsymbol.js"></script>
    <script src="js/feather.js"></script>
    <script src="js/edgemap_ng.js"></script>
    <link rel="stylesheet" href="css/main.css">
    <link rel="stylesheet" href="css/RadialMenu.css">
    <link rel="stylesheet" href="css/RadialMenuCustom.css">
    <script src="js/RadialMenu.js"></script>
    <script src="js/main.js"></script>
    <link href="css/edgemap.css" rel="stylesheet" />
    
    <link rel="apple-touch-icon" sizes="180x180" href="favicon/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="favicon/favicon-16x16.png">
    <link rel="manifest" href="favicon/site.webmanifest">
    
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="app-icon/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">
    <script type="text/javascript" src="videoroom/js/adapter.min.js" ></script>
    <script type="text/javascript" src="videoroom/js/jquery.min.js" ></script>
    <script type="text/javascript" src="videoroom/js/jquery.blockUI.min.js" ></script>
    <script type="text/javascript" src="videoroom/js/spin.min.js" ></script>
    <script type="text/javascript" src="videoroom/janusv3.js" ></script>
    <script type="text/javascript" src="videoroom/videoroomtestv3.js"></script>

</head>
   
<body  style="background-color:#000000" >
    
    <div id="platform_status" class="space-holder" >
        <table style="border:0px solid; padding: 5px;">
            <tr><td style="padding-right: 15px;">Comms:</td><td>Active</td></tr>
            <tr><td>RF:</td><td>Active</td></tr>
            <tr><td>Crypto:</td><td>Plain</td></tr>
        </table>
    </div>
    
    <div id="platform_logo" class="space-logo" >
        <img src="img/edgemap-map-logo.png" width=100px>
    </div>
    
    <div id="platform_help" class="space-holder-left-bottom" >
        <table >
            <tr><td>Close dialog</td><td align="center">ESC</td></tr>
            <tr><td>Messages</td><td align="center">m</td></tr>
            <tr><td>Meshtastic radios</td><td align="center">r</td></tr>
            <tr><td>Reticulum radios</td><td align="center">R</td></tr>
            <tr><td>Terrain</td><td align="center">h</td></tr>
            <tr><td>Coordinate search</td><td align="center">f</td></tr>
        </table>
    </div>

    <div id="map"></div>
    
    <pre id="features"></pre>
    <pre id="coordinates" class="coordinates"></pre>
    
    <div id="leftVideo" >
        <img src="<?php echo $CAM[0]; ?>" id='cam1' width=100%;>
        <img src="<?php echo $CAM[1]; ?>" id='cam2' width=100%;>
        <img src="<?php echo $CAM[2]; ?>" id='cam3' width=100%;>
        <img src="<?php echo $CAM[3]; ?>" id='cam4' width=100%;>
        <img src="<?php echo $CAM[4]; ?>" id='cam5' width=100%;>
    </div>
    <div id="rightVideo">
        <img src="<?php echo $CAM[4]; ?>" id='cam6' width=100%;>
        <img src="<?php echo $CAM[3]; ?>" id='cam7' width=100%;>
        <img src="<?php echo $CAM[2]; ?>" id='cam8' width=100%;>
        <img src="<?php echo $CAM[1]; ?>" id='cam9' width=100%;>
        <img src="<?php echo $CAM[0]; ?>" id='cam10' width=100%;>
    </div>
    
    <div class="map-top-status-icon-overlay">
    <center >
        <div class="icon-container-new" >
                
            <img id="messagingSocketStatus" class="has-tooltip" src="icons/reticulum-message-green.png" width=20px;>
             <div class="tooltip" id="">Message socket connected</div>
            <img id="messagingSocketStatusRed" class="has-tooltip"  src="icons/reticulum-message-red.png" width=20px;>
             <div class="tooltip" id="">Message socket disconnected.</div>
            
            <img id="statusSocketStatus" class="has-tooltip" src="icons/reticulum-green.png" width=20px;>
             <div class="tooltip" id="">Status socket connected</div>
            <img id="statusSocketStatusRed" class="has-tooltip"  src="icons/reticulum-red.png" width=20px;>
             <div class="tooltip" id="">Status socket disconnected.</div>
            
            <img id="securePttStatus" class="has-tooltip" src="icons/ptt-green.png" width=20px;>
             <div class="tooltip" id="">SecurePTT status socket connected</div>
            <img id="securePttStatusRed" class="has-tooltip" src="icons/ptt-red.png" width=20px;>
              <div class="tooltip" id="">SecurePTT status socket disconnected</div>
            
            <img id="gpsSocketStatus" class="has-tooltip" src="icons/gnss-green.png" width=20px;>
             <div class="tooltip" id="">Local GNSS socket connected</div>
            <img id="gpsSocketStatusRed" class="has-tooltip" src="icons/gnss-red.png" width=20px;>
             <div class="tooltip" id="">Local GNSS socket disconnected</div>
            
            <img id="highRateSocketStatus" class="has-tooltip" src="icons/drone-green.png" width=20px;>
             <div class="tooltip" id="">Highrate socket connected.</div>
            <img id="highRateSocketStatusRed" class="has-tooltip" src="icons/drone-red.png" width=20px;>
             <div class="tooltip" id="">Highrate socket disconnected.</div>
             
            <img id="trackingIndicator" class="has-tooltip" src="icons/tracking-green.png" width=20px;>
             <div class="tooltip" id="">Tracking connected.</div>
            <img id="trackingIndicatorRed" class="has-tooltip" src="icons/tracking-red.png" width=20px;>
             <div class="tooltip" id="">Tracking disconnected.</div>
                 
        </div>
        <table style="display: none;">
            <tr><td id="securePttTx" class="mapSecurepttTransmissionStatus">TX</div></td> <td> </td></tr>  
            <tr><td id="securePttRx" class="mapSecurepttTransmissionStatus">RX</div></td> <td></td></tr>
        </table>
    </center>
    </div>
    
    
    
    <div class="map-top-callsign-overlay">
        <center>
            <span id="callSignDisplay" style=" padding-top:5px;"></span>
        </center>
    </div>
    
    <div class="map-top-gpslocation-overlay">
        <center>
            <span id="gpsDisplay"  onClick="sendMyGpsLocation();"></span>
        </center>
    </div>
    
    <div class="map-top-reticulum-overlay">
        <center>
            <span id="reticulumAnnounceNotify"  onClick="" ></span>
        </center>
    </div>
    
    
    <div id="mapClickLatlonSection" class="map-top-latlon-overlay" style="display: none;" >
        <center>
            <span id="lat" onclick="getCoordinatesToClipboard()" ></span><span id="coordinateComma">,</span><span id="lon" onclick="getCoordinatesToClipboard()"></span>
            <span id="copyNotifyText"></span>
        </center>
    </div>
    
    <div class="map-top-reloadbutton-overlay" onClick="reloadPage();">
        <center>
            <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="-3 -3 25 25">
                <g fill="none"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4.75 10.75h-3m12.5-2c0 3-2.798 5.5-6.25 5.5c-3.75 0-6.25-3.5-6.25-3.5v3.5m9.5-9h3m-12.5 2c0-3 2.798-5.5 6.25-5.5c3.75 0 6.25 3.5 6.25 3.5v-3.5"/></g>
            </svg>
        </center>
    </div>
    
    <div id="topRightMenuButton" class="map-top-menubutton-overlay">
        <svg xmlns="http://www.w3.org/2000/svg" width="29" height="29" viewBox="-3 -3 25 25">
        <g fill="none"><path d="m12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035q-.016-.005-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093q.019.005.029-.008l.004-.014l-.034-.614q-.005-.018-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01z"/><path fill="currentColor" d="M20 17.5a1.5 1.5 0 0 1 .144 2.993L20 20.5H4a1.5 1.5 0 0 1-.144-2.993L4 17.5zm0-7a1.5 1.5 0 0 1 0 3H4a1.5 1.5 0 0 1 0-3zm0-7a1.5 1.5 0 0 1 0 3H4a1.5 1.5 0 1 1 0-3z"/></g>
        </svg>
    </div>
    
    <div class="map-right-upload-overlay" id="cameracontrol" style="display: none;">
        <div class="map-right-upload-overlay-inner">
            <div id="legend" class="legend">
                    <iframe name="dummyframe" id="dummyframe" style="display: none;">X</iframe>
                    <form id="uploadform" action="upload.php" method="post" enctype="multipart/form-data" target="dummyframe">
                      <center>
                      <input type="file" name="fileToUpload" id="fileToUpload" onchange="submitImage();" hidden>
                      <input type="hidden" name="lat" value="" size ="40" />
                      <input type="hidden" name="lon" value="" size ="40" />
                      <input type="hidden" name="callsign" value="" size ="40" />
                      <label for="fileToUpload"><i data-feather="camera" class="feather-normal"></i></label>
                      </center>
                    </form>
            </div>
            <div><span id="gpsStatus"></span></div>
        </div>
    </div>
    
    

    <div class="notify-box" id="info-box">
        <center>
        EdgeMap - off-line-map for resilience
        </center>
        <div class ="notify-box-small-content">
            <center>
            <p>
            Based on following open source components:
            </p>
            <p>
                MapLibre GL JS <a href="https://github.com/maplibre/maplibre-gl-js"><i data-feather="github" class="feather-small"></i></a>
                Milsymbol <a href="https://github.com/spatialillusions/milsymbol"><i data-feather="github" class="feather-small"></i></a><br>
                Feather icons <a href="https://github.com/feathericons/feather"><i data-feather="github" class="feather-small"></i></a>
                Zoneminder <a href="https://github.com/ZoneMinder/ZoneMinder/"><i data-feather="github" class="feather-small"></i></a>
                protomaps <a href="https://protomaps.com/"><i data-feather="link" class="feather-small"></i></a><br>
                Map data © OpenStreetMap contributors <a href="https://www.openstreetmap.org/copyright/"><i data-feather="link" class="feather-small"></i></a>
            </p>
            </center>
        </div>
            <center><div class ="notify-box-small-content">Terrain data attribution:</div></center>
            <div class="attribution-div">
            * ArcticDEM terrain data DEM(s) were created from DigitalGlobe, Inc., imagery and funded under National Science Foundation awards 1043681, 1559691, and 1542736;
            * Australia terrain data © Commonwealth of Australia (Geoscience Australia) 2017;
            * Austria terrain data © offene Daten Österreichs – Digitales Geländemodell (DGM) Österreich;
            * Canada terrain data contains information licensed under the Open Government Licence – Canada;
            * Europe terrain data produced using Copernicus data and information funded by the European Union - EU-DEM layers;
            * Global ETOPO1 terrain data U.S. National Oceanic and Atmospheric Administration
            * Mexico terrain data source: INEGI, Continental relief, 2016;
            * New Zealand terrain data Copyright 2011 Crown copyright (c) Land Information New Zealand and the New Zealand Government (All rights reserved);
            * Norway terrain data © Kartverket;
            * United Kingdom terrain data © Environment Agency copyright and/or database right 2015. All rights reserved;
            * United States 3DEP (formerly NED) and global GMTED2010 and SRTM terrain data courtesy of the U.S. Geological Survey.
            </div>
        <center>
            <p style="font-size:16px" >© Resilience Theatre 2023 <a href="#"><i data-feather="link" class="feather-small"></i></a></p>
            <button class="attribution-button" id="infobox-close"><i data-feather="x-circle" class="feather-normal"></i> Close</button>
        </center>
    </div>


    <div class="coordinateSearch" id="coordinateSearchEntry" >
            <input id="coordinateInput" type="text" placeholder="[latitude,longitude]" class="coordinateSearchInput" maxlength="20" onkeypress="handleKeyPress(event)" onfocus="ensureVisible(this)">
    </div>
    

    <div class="callSignEntry" id="callSignEntry" >
        <table border=0 width=100%>
            <tr>
                <td width=90%>
                    <span class="callsignTitle">Callsign:</span><input id="myCallSign" type="text" class="callSignInput" maxlength="5" >
                </td>
                <td>
                
                <i data-feather="check-circle" class="feather-submitCallSignEntry" onClick='closeCallSignEntryBox();' ></i> 
                </td>
            </tr>
        </table>	
    </div>

    <div class="delivery-status" id="delivery-status-window">	
    <div id="logo" class="toprightlogoreticulumblock"><img src="img/rnsg.png" width=40px; ></img></div>
    <div id="delivery_status_header"></div>
    <div id="delivery_status"></div>
    </div>

    <div class="log-window" id="log-window">	
        <table width=100% border=0>
        <tr>
            <td width=82% > 
                <div id="msgChannelLog" class="incomingMsg"></div>
            </td>
            <td valign=top align=center>
                <i data-feather="x-circle" class="feather-closeMsgEntry" onClick='closeMessageEntryBox();' ></i> <p>
                <i data-feather="map-pin" class="feather-cmdButtons" onClick='createNewDragableMarker();'></i><p>
                <i data-feather="trash" class="feather-cmdButtons" onClick='eraseMsgLog();' ></i><p>
                <i data-feather="at-sign" class="feather-cmdButtons" onClick='openCallSignEntryBox();'></i>
            </td>
        </tr>
        </table>
        <input type="text" id="msgInput" type="text" class="messageInputField" onfocus="ensureVisible(this)"  >
        <button id="sendMsg" class="msgbutton" onClick='' title='send' ><i data-feather="send" class="feather-msgbutton"></i></button>
    </div>

    <div class="map-bottom-log-entries" id="bottomLog" style="display: none;">
    <table width=100% border=0>
        <tr>
        <td ><i data-feather="info" id="notifyMessageIcon" class="feather-submitCallSignEntry"></i></td>
        <td width=80%><div id="notifyMessage"></div></td>
        </tr>
    </table>
    </div>
    
    <div class="map-bottom-sensor-entries" id="sensorNotify" style="display: none;">
    <table width=100% border=0>
        <tr valign="top">
            <td ><i data-feather="alert-triangle" id="sensorNotifyMessageIcon" class="feather-submitCallSignEntry"></i></td>
            <td width=90%>
                <div class="sensor-message-style" id="sensorMessage"></div>
                
                <div id="sensor-create-input-placeholder"></div>
                <div id="sensor-create-input">
                    <table border=0 width=80%>
                        <tr>
                            <td><span id="sensorLocationTooltip"></span></td>
                            <td><span id="sensorLat"></span><span id="sensorLatLonComma"></span><span id="sensorLon"></span></td>
                        </tr>
                        <tr valign="top">
                            <td valign="top"><span id="sensorNameEntryDesc">Desc:</span></td>
                            <td valign="top"><span id="sensorNameEntryInput"><input type="text" id="sensorNameInput" type="text" class="sensorNameInputStyle"></span></td>
                        </tr>
                    </table>
                </div>
                <div class="sensor-define-button-style" id="sensor-define-button" style="display: block;" onclick="sensorDefine();"><center>Create</center></div>
                <div class="sensor-close-button-style" id="sensor-close-button" style="display: block;" onclick="sensorClose();"><center>Close</center></div>
            </td>
        </tr>
    </table>
    </div>
    
    
    
    
        <div class="map-bottom-manualLocation-entries" id="manualLocationNotify" style="display: none;">
        <table width=100% border=0>
            <tr valign="top">
                <td ><i data-feather="target" id="manualLocation-Icon" class="feather-submitCallSignEntry"></i></td>
                <td width=90%>
                    <div class="manualLocation-message-style" id="manualLocation-Message"></div>
                    
                    <div id="manualLocation-create-input-placeholder"></div>
                    <div id="manualLocation-create-input">
                        <table border=0 width=80%>
                            <tr>
                                <td><span id="manualLocation-Tooltip"></span></td>
                                <td><span id="manualLocation-Lat"></span><span id="manualLocation-LatLonComma"></span><span id="manualLocation-Lon"></span></td>
                            </tr>
                            
                        </table>
                    </div>
                    <div class="manualLocation-define-button-style" id="manualLocation-define-button" style="display: block;" onclick="manualLocationErase();"><center>Unset</center></div>
                    <div class="manualLocation-close-button-style" id="manualLocation-close-button" style="display: block;" onclick="manualLocationSet();"><center>Set</center></div>
                </td>
            </tr>
        </table>
        </div>

    
    <div class="map-videoroom-overlay" id="videoBlock" style="display: none;">
        <div class="map-videoroom-title"></div>
        <div class="map-videoroom-ctrl-buttons" id="videolocalbuttons"></div>
        <div class="videoConferenceVideoDisplay" id="videolocal"></div>
        <div class="map-videoroom-title">Peers:</div>
        <div class="videoConferenceVideoDisplay" id="videoremote1"></div>
        <div class="videoConferenceVideoDisplay" id="videoremote2"></div>
        <div class="videoConferenceVideoDisplay" id="videoremote3"></div>
        <div class="videoConferenceVideoDisplay" id="videoremote4"></div>
        <div class="videoConferenceVideoDisplay" id="videoremote5"></div>
    </div>
    
    
    <div class="radiolistblock" id="radiolistblock" style="display: none;">
        <div id="logo" class="toprightlogoradiolistblock"><img src="img/meshtastic-logo.png" width=35px; ></img></div>
        <div id="radiolist"></div>
    </div>
    
    <div class="reticulumlistblock" id="reticulumlistblock" style="display: none;">
        <div id="logo" class="toprightlogoreticulumblock"><img src="img/rnsg.png" width=40px; ></img></div>
        <div id="reticulumlist"></div>
    </div>
    
    <div id="lat_highrate" style="display: none;"></div>
    <div id="lon_highrate" style="display: none;"></div>
    <div id="name_highrate" style="display: none;"></div>
    <div id="lat_localgps" style="display: none;"></div>
    <div id="lon_localgps" style="display: none;"></div>
    <div id="speed_localgps" style="display: none;"></div>
    <div id="mode_localgps" style="display: none;"></div>
    

    
<script>    
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
 
    Features
    -----------------------------------------------------------------
    * Websocket highrate target.
    * Geolocate markers of peers, over msg channel.
    * Full world terrain.
    * Milsymbols as DOM element [1]
    * CoT targets from Taky via geojson
    * Sniper control demo (not enabled)
    * Protomaps OSM planet and raster satellite sources [3]
    * Requires gwsocket and tacmsgrouter for full messaging demo

    [1] https://www.spatialillusions.com/milsymbol/documentation.html
    [2] https://maplibre.org/maplibre-gl-js/docs/API/
    [3] https://protomaps.com/

    NOTE: This is NG (NextGen) version. Where aim is to simplify
    reticulum, meshtastic and possibly other transport network integration.
    Work in progress.

*/

    var map = new maplibregl.Map({
          container: 'map',
          zoom: 1,
          minZoom: 1,
          maxPitch: 85,
          hash: true,
          style: "styles/style-v4.json"
        });
    var currentStyle = "bright";


    const edgemapUiVersion = "v0.8";
    var intialZoomLevel=1;
	var symbolSize = 30;
    
    // geojson url
    var geojsonUrl = 'meshtastic_geojson.php?linkline=1';
    var geoJsonLayerActive = true;
	
	// One user created pin marker for a demo
	const mapPinMarker = [];
	const mapPinMarkerPopup = [];
	var mapPinMarkerCount = 0;
    
    // Sensor markers from message 
    const sensorMarker = [];
    const sensorMarkerPopup = [];

    // Image markers from message (in DEVELOPMENT)
    const imageMarker = [];
    const imageMarkerPopup = [];

	// Second way to handle draggable markers (try out)
	var dragMarkers = [];
	var dragPopups = [];
	var indexOfDraggedMarker;
	var lastDraggedMarkerId;

	//
	// Generate random callsign for a demo
    // 
	var callSign = genCallSign();
	document.getElementById('myCallSign').value = callSign;
    document.getElementById('callSignDisplay').innerHTML = callSign;
    
    // populate callsign and default lat,lon into image upload form
    const formInfo = document.forms['uploadform'];
    formInfo.callsign.value = callSign; 
    formInfo.lat.value = "-"; 
    formInfo.lon.value = "-"; 
    
    // Draggable marker for sharing over msg channel
    var dragMarker;
    var dragMarkerPopup = new maplibregl.Popup({offset: 35});

    // We have one highrate marker as an example 
    // staffComments: "Highrate".toUpperCase(),
	var highrateMarker;
	var highRateCreated=false;
    var milSymbolHighrate = new ms.Symbol("30030100001203000000", { size:20,
                dtg: "",
                additionalInformation: "Highrate 20 Hz".toUpperCase(),
                combatEffectiveness: "".toUpperCase(),
                type: "",
                padding: 5,
                infoColor: "#EE0000",
                infoBackgroundFrame: "#000000"
                });
    var milSymHighrateMarker = milSymbolHighrate.asDOM();
    //
    // localGpsMarker (development)
    //
    var localGpsMarker;
	var localGpsMarkerCreated=false;
    var milSymbolLocalGps = new ms.Symbol("SFGPUCR-----", { size:20,
                dtg: "",
                staffComments: "Local GPS".toUpperCase(),
                additionalInformation: "1 Hz".toUpperCase(),
                combatEffectiveness: "".toUpperCase(),
                type: "",
                padding: 5,
                infoColor: "#000000",
                infoBackground: "#CCFFCCD0"
                });
    var milSymbolLocalGpsMarker = milSymbolLocalGps.asDOM();
    // Local GPS fix status
    var localGpsFixStatus = 0;
    // Geolocate to trackMessage markers
    const trackMessageMarkers = []; 
    var lastKnownCoordinates;
    
    
    // Development variable for enabling / disabling messaging
    var messagingFeatureEnabled = 1
    
    // Remember to run gwsocket systemd service along enabling these:
    
    // Development variable for enabling / disabling highrate target
    var highrateFeatureEnabled = 0
    // Development variable for enabling / disabling securePTT
    var securepttFeatureEnabled = 0
    
    // We track 'radios' on mesh - not their location on map.
    // We don't want to enforce or use meshtastic internal
    // positioning reports (or capability to use GPS) since it's an OPSEC
    // issue.
    
    let meshtasticRadiosOnSystem = new meshtasticRadioList;
    let reticulumNodesOnSystem = new reticulumPeerList; 
    
    // Milsymbol for trackMessage
    const trackMessageMarkerGraph = new ms.Symbol("SFGPUCR-----", { size:20,
                dtg: "",
                staffComments: "".toUpperCase(),
                additionalInformation: "".toUpperCase(),
                combatEffectiveness: "".toUpperCase(),
                type: "",
                padding: 5,
                infoColor: "#000000",
                infoBackground: "#FFFFFFD0"
                });
    var trackMessageMarkerGraphDom = trackMessageMarkerGraph.asDOM();

    // Sensor globals
    var sensorToBeCreated=0;
    var keyEventListener=1;
    var unknownSensorCreateInProgress=0;
    
    // Manual location globals
    var manualLocationCreateInProgress=0;

    // Set sky as you like
    function setSkyFromUi() {
        map.setSky({
            'sky-color': "#0f0881",
            'sky-horizon-blend': 0.16,
            'horizon-color': "#ed333b",
            'horizon-fog-blend': 0.58,
            'fog-color': "#9a9996",
            'fog-ground-blend': 0.65
        });
    }

    // Create marker from messaging window
	function createNewDragableMarker() {
		newDragableMarker();
	}
    function getElementItem(selector) {
        return document.querySelector(selector);
    }
    
    // ==========
    // Websockets
    // ==========
    
    /*
    Since WebRTC requires TLS connection, our web sockets must be 
    served with security. There are two different set of systemd
    services for this to happen. Here is summary of used ports.
    
    Function                Plain   With SSL    FIFO
    ==========================================================
    Local GPS               7790    8790        /tmp/gpssocket
    Highrate marker         7890    8890
    messaging (ng)          7990    8990        /tmp/msgchannel /tmp/msgincoming 
    status  (ng)            7997    8997        /tmp/statusin
    
    old & to be removed:
    meshtastic messaging    7991    8991
    meshtastic status       7995    8995
    SecurePTT status        7996    8996
    
    */
    
    var messagingSocket;
    var messagingSocketConnected=false;
    
    var statusSocket;
    var statusSocketConnected=false;
    
    // TODO: Check highrate busy connect
    var highrateSocket;
    var highrateSocketConnected=false;
    var gpsSocket;
    var gpsSocketConnected=false;
    
    var wsProtocol = null;
    if(window.location.protocol === 'http:')
            wsProtocol = "ws://";
    else
            wsProtocol = "wss://";
    var wsHost = location.host;

    // ==================================
    // Websocket for locally attached GPS
    // ==================================
    if ( wsProtocol == "ws://" )
        gpsSocket = new WebSocket(wsProtocol+wsHost+':7790');
    if ( wsProtocol == "wss://" )
        gpsSocket = new WebSocket(wsProtocol+wsHost+':8790');
    
    gpsSocket.onopen = function(event) {
        document.getElementById('gpsSocketStatus').style="display:block; padding-top:5px;";
        document.getElementById('gpsSocketStatusRed').style="display:none;";
        gpsSocketConnected = true;
    };
    gpsSocket.onclose = function(event) {
        document.getElementById('gpsSocketStatusRed').style="display:block; padding-top:5px;";
        document.getElementById('gpsSocketStatus').style="display:none;";
        gpsSocketConnected=false;
    };
    
    gpsSocket.onmessage = function(event) {
            var displayString;
			var incomingMessage = event.data;
			var trimmedString = incomingMessage.substring(0, 80);
            const localGpsArray = trimmedString.split(",");
            if ( localGpsArray[0] == "n/a" ) 
                displayString = "GPS: No fix";
            if ( localGpsArray[0] == "None" ) 
                displayString = "GPS: No fix";
            if ( localGpsArray[0] == "2D" ) 
                displayString = "GPS: 2D fix";
            if ( localGpsArray[0] == "3D" ) 
                displayString = "GPS: 3D fix";
            if ( localGpsArray[0] == "Manual" ) 
                displayString = "GPS: Manual";
            document.getElementById("gpsDisplay").innerHTML = displayString;
            /*  localGpsArray[0] : text 
                localGpsArray[1] : enum
                gpsreader.c:                
                static char *mode_str[MODE_STR_NUM] = {
                    "n/a",
                    "None",
                    "2D",
                    "3D",
                    "Manual"
                }; */           
            if ( localGpsArray[1] == "0" || localGpsArray[1] == "1" ) {
                localGpsFixStatus = 0;
            }            
            if ( localGpsArray[1] == "2" || localGpsArray[1] == "3" || localGpsArray[1] == "4") {
                localGpsFixStatus = 1;
                // Update location only on valid fix
                getElementItem('#lat_localgps').innerHTML =  localGpsArray[5];
                getElementItem('#lon_localgps').innerHTML =  localGpsArray[4];
                getElementItem('#speed_localgps').innerHTML =  localGpsArray[6]; 
                getElementItem('#mode_localgps').innerHTML =  localGpsArray[0];
            }
            // Create marker when we have first valid fix from GPS
            // TODO: calculate offset: [30, 0] from .getanchor
			if ( localGpsMarkerCreated == false && localGpsFixStatus == 1 ) {
                localGpsMarker = new maplibregl.Marker({
                    element: milSymbolLocalGpsMarker,
                    offset: [30, 0]
				});
				requestAnimationFrame(animateLocalGpsMarker);
                localGpsMarkerCreated = true;
			}
    };
    
    // =============================
    // Websocket for highrate marker
    // =============================
    document.getElementById('highRateSocketStatus').style="display:none;";
    document.getElementById('highRateSocketStatusRed').style="display:block;";
    
    if ( highrateFeatureEnabled ) {
        if ( wsProtocol == "ws://" )
            highrateSocket = new WebSocket(wsProtocol+wsHost+':7890');
        if ( wsProtocol == "wss://" )
            highrateSocket = new WebSocket(wsProtocol+wsHost+':8890');
            
        highrateSocket.onopen = function(event) {
            document.getElementById('highRateSocketStatus').style="display:block;";
            document.getElementById('highRateSocketStatusRed').style="display:none;";
            highrateSocketConnected = true;
        };
        highrateSocket.onclose = function(event) {
            document.getElementById('highRateSocketStatus').style="display:none;";
            document.getElementById('highRateSocketStatusRed').style="display:block;";
            highrateSocketConnected=false;
        };
        highrateSocket.onmessage = function(event) {
                var incomingMessage = event.data;
                var trimmedString = incomingMessage.substring(0, 80);
                const positionArray = trimmedString.split(",");
                // TODO: Validate data better
                getElementItem('#lat_highrate').innerHTML =  positionArray[1];
                getElementItem('#lon_highrate').innerHTML =  positionArray[0];
                getElementItem('#name_highrate').innerHTML =  positionArray[2];
                var targetSymbol = positionArray[3];
                
                // Create highrate highrateMarker from first incoming message 
                if ( highRateCreated == false ) {
                    highrateMarker = new maplibregl.Marker({
                        element: milSymHighrateMarker
                    });
                    requestAnimationFrame(animateHighrateMarker);
                    highRateCreated = true;
                }
            };
    }
    
    // ============================
    // Websocket for messaging (ng)
    // ============================
    
    /* Work in progress to unify meshtastic and reticulum handling */
    
    if ( messagingFeatureEnabled ) {    
        //
        // messagingSocket (8990)
        //
        if ( wsProtocol == "ws://" )
            messagingSocket = new WebSocket(wsProtocol+wsHost+':7990');
        if ( wsProtocol == "wss://" )
            messagingSocket = new WebSocket(wsProtocol+wsHost+':8990');

        //
        // messagingSocket connect (8990)
        //
        messagingSocket.onopen = function(event) {
            document.getElementById('messagingSocketStatus').style="display:block; padding-left: 5px; padding-top:5px;"; 
            document.getElementById('messagingSocketStatusRed').style="display:none;";
            messagingSocketConnected = true;
        };
        //
        // messagingSocket disconnect (8990)
        //
        messagingSocket.onclose = function(event) {
            document.getElementById('messagingSocketStatus').style="display:none;";
            document.getElementById('messagingSocketStatusRed').style="display:block; padding-left: 5px; padding-top:5px;"; 
            notifyMessage("Message channel disconnected! Try reloading page.", 5000);
            messagingSocketConnected=false;
        };
        
        //
        // messagingSocket incoming (8990)
        //
        messagingSocket.onmessage = function(event) {
            var incomingMessage = event.data;
            var trimmedString = incomingMessage.substring(0, 200);
            const msgArray=trimmedString.split("|");
            const msgFrom =  msgArray[0];
            const msgType =  msgArray[1];
            const msgLocation =  msgArray[2];
            const msgMessage =  msgArray[3];
            
            if ( getElementItem('#myCallSign').value === msgFrom) {
                console.log("My own message detected, discarding.");
                return;
            }
            // Handle reticulum delivery note
            // delivery_message = "|delivery_note||+" + peer_callsign
            if ( msgType === "msg_delivery_ok" ) {
                console.log("Delivered: ", msgMessage)
                document.getElementById("delivery_status").innerHTML += "<span style='color:#0F0;'> "+msgMessage+"</span>";  
            }
            if ( msgType === "msg_delivery_timeout" ) {
                console.log("Message delivery timeout: ", msgMessage)
                document.getElementById("delivery_status").innerHTML += "<span style='color:#F00;'> "+msgMessage+"</span>"; 
            }
            if ( msgType === "msg_send_start" ) {
                console.log("About to send message: ", msgMessage, " nodes")
                document.getElementById("delivery_status").innerHTML = "Sending (" + msgMessage + "):";
                fadeIn(deliveryStatusDiv,400);
            }
            if ( msgType === "msg_delivery_complete" ) {
                console.log("Send is complete: ", msgMessage, " ")
                document.getElementById("delivery_status").innerHTML = "<div class='vertical-center'><h2>Complete! ( " + msgMessage + " seconds ) </h2></div>";
                fadeOut(deliveryStatusDiv,5000);
            }
            // 
            // meshpipe join (from meshtastic network)
            //
            if ( msgType === "meshpipe" ) {
               notifyMessage( "Node start: " + msgMessage, 5000);                   
            }
            //
            // Join message demo
            //
            /*
            if ( msgType === "joinMessage" ) {
                
                if ( !peersOnMap.present(msgFrom) ) {
                    notifyMessage( msgFrom +" " +msgMessage, 5000);    
                }
                // Add (or update) peer with callsign and timestamp
                peersOnMap.add( msgFrom, Math.round(+new Date()/1000) );
                updatePeerListBlock(); 
            }*/
            if ( msgArray.length == 4 ) 
            {
                //
                // Geolocated peer marker
                //
                if ( msgType === "trackMarker" ) {
                    const location = msgLocation;
                    const locationNumbers = location.replace(/[\])}[{(]/g, '');
                    const locationArray = locationNumbers.split(",");
                    createTrackMarkerFromMessage(locationArray[0], locationArray[1],msgFrom,msgMessage);
                }
                //
                // Shared 'drag marker'
                //
                if ( msgType === "dragMarker" ) {                        
                    const location = msgLocation;
                    const locationNumbers = location.replace(/[\])}[{(]/g, '');
                    const locationArray = locationNumbers.split(",");
                    dragMarker.setLngLat([ locationArray[0], locationArray[1] ]);
                    dragMarkerPopup.setText(msgFrom + " " + msgMessage);
                    
                    if ( msgMessage.includes("dragged") ) {
                        if ( !dragMarkerPopup.isOpen() ) {
                            dragMarkerPopup.addTo(map);
                        }
                    } 
                     if ( msgMessage.includes("released") )  {
                        if ( dragMarkerPopup.isOpen() ) {
                            dragMarkerPopup.remove();
                        }
                    } 
                }
                //
                // Messaging 'drop in' marker
                //
                if ( msgType === "dropMarker" ) {
                    const location = msgLocation;
                    const locationNumbers = location.replace(/[\])}[{(]/g, '');
                    const locationArray = locationNumbers.split(",");
                    const markerText = "<b>" + msgFrom + "</b>:" + msgMessage + "<br>" + locationArray[1]+","+locationArray[0];		
                    createMarkerFromMessage(mapPinMarkerCount, locationArray[0], locationArray[1],markerText );
                    mapPinMarkerCount++;                        
                }
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
                //
                // Image marker: [FROM]|imageMarker|[LAT,LON]|[FILENAME]
                // 
                // Based on: https://stackoverflow.com/questions/47798971/several-modal-images-on-page
                //
                if ( msgType == "imageMarker" ) {
                    const location = msgLocation;
                    const locationNumbers = location.replace(/[\])}[{(]/g, '');
                    const locationArray = locationNumbers.split(",");   
                    createImageMarker(msgFrom,locationArray[0], locationArray[1],msgMessage.slice(0,-2));
                        var modal = document.getElementById('myModal');
                        var images = document.getElementsByClassName('myImages');
                        var modalImg = document.getElementById("img01");
                        var captionText = document.getElementById("caption");
                        for (var i = 0; i < images.length; i++) {
                          var img = images[i];
                          img.onclick = function(evt) {
                            modal.style.display = "block";
                            modalImg.src = this.alt; 
                            captionText.innerHTML = "Full size image";
                          }
                        }
                        var span = document.getElementsByClassName("close")[0];
                        span.onclick = function() {
                          modal.style.display = "none";
                           modalImg.src = "";
                        } 
                        notifyMessage("Image received from " + msgFrom , 5000);
                }
            }
            //
            // Normal message 
            // TODO: sanitize, validate & parse etc (this is just an demo)
            //
            if ( msgArray.length != 4 && msgType != "dragMarker" && msgType != "trackMarker" && msgType != "sensorMarker" && msgType != "imageMarker" && msgType != "joinMessage" && msgType != "sensor" ) {
                openMessageEntryBox(); 
                getElementItem('#msgChannelLog').innerHTML += trimmedString;
                getElementItem('#msgChannelLog').innerHTML += "<br>";
                var scrollElement = document.getElementById('msgChannelLog');
                scrollElement.scrollTop = scrollElement.scrollHeight;
            }
        };
    }


    // =================================================
    // messagingSocket outgoing
    // ==================================================
    var input = document.getElementById("msgInput");
    input.addEventListener("keyup", function(event) {
        if (event.keyCode === 13) {
            event.preventDefault();
            document.getElementById("sendMsg").click();
        }
    }); 
    
    getElementItem('#sendMsg').onclick = function(e) {
        console.log("Send message debug: ", getElementItem('#myCallSign').value);
        var msgPayload = getElementItem('#myCallSign').value + '|' + getElementItem('#msgInput').value + '\n';       
        
        // This is for reticulum ACK message demonstration
        // Currently disabled on nextgen approach, to be removed.
        if ( 0 ) {
            document.getElementById("delivery_status").innerHTML = ""
            fadeIn(deliveryStatusDiv,400);
            // fireup timeout for fadeout
            window.setInterval(function () {
            fadeOut(deliveryStatusDiv,1000);
            }, 20000 );
        }
        
        // Send based on socket connection
        sendMessageToAllBearers( msgPayload );
        localSensorMarkerCreate( msgPayload );

        getElementItem('#msgChannelLog').innerHTML += msgPayload  + '<br>';
        getElementItem('#msgInput').value = '';
        var scrollElement = document.getElementById('msgChannelLog');
        scrollElement.scrollTop = scrollElement.scrollHeight;
        // If marker dragend has filled message field, allow appended content to be
        // updated into dragged marker popup. 
        // lastDraggedMarkerId is set by 'dragend' inline function.
        var draggedMarkerID = lastDraggedMarkerId; 
        // Grab index where ID is found. TODO: Handle error state
        var grabbedIndex;
        for ( loop=0; loop < dragMarkers.length ; loop++) {	
            // console.log("Element ID ",loop," ID:", dragMarkers[loop]._element.id );
            if ( draggedMarkerID.localeCompare(dragMarkers[loop]._element.id) == 0 ) {
                grabbedIndex = loop;
                dragMarkers[grabbedIndex].setPopup(new maplibregl.Popup({ closeOnClick: false, }).setHTML(msgPayload)); 
                dragMarkers[grabbedIndex].togglePopup();
                lastDraggedMarkerId = ""; 
            }
        }
    };
    
    // =================================
    // Secureptt status (/tmp/secureptt)
    // =================================
    
    if ( securepttFeatureEnabled ) {    
        if ( wsProtocol == "ws://" )
            securePttStatusSocket = new WebSocket(wsProtocol+wsHost+':7996');
        if ( wsProtocol == "wss://" )
            securePttStatusSocket = new WebSocket(wsProtocol+wsHost+':8996');
            
        securePttStatusSocket.onopen = function(event) {
            document.getElementById('securePttStatus').style="display:block; padding-top:5px;";
            document.getElementById('securePttStatusRed').style="display:none; padding-top:5px;";
            
            var style="font: 8px 'Helvetica Neue', Arial, Helvetica, sans-serif;padding: 1px;border: 1px solid #0E0;color: #0F0;background-color: transparent;";
            document.getElementById('securePttTx').style = style;
            document.getElementById('securePttRx').style = style;
        };
        securePttStatusSocket.onclose = function(event) {
            document.getElementById('securePttStatus').style="display:none;";
            document.getElementById('securePttStatusRed').style="display:block; padding-top:5px;";
            document.getElementById('securePttTx').style = "display:none;"
            document.getElementById('securePttRx').style = "display:none;"
        };
        
        securePttStatusSocket.onmessage = function(event) {
            var incomingMessage = event.data;
            var trimmedString = incomingMessage.substring(0, 80);
            if ( trimmedString === "tx-on" )
            {
                var style="font: 8px 'Helvetica Neue', Arial, Helvetica, sans-serif;padding: 1px;border: 1px solid #0E0;color: #0F0;background-color: #D00;";
                document.getElementById('securePttTx').style = style;
            }
            if ( trimmedString === "tx-off" )
            {
                var style="font: 8px 'Helvetica Neue', Arial, Helvetica, sans-serif;padding: 1px;border: 1px solid #0E0;color: #0F0;background-color: transparent;";
                document.getElementById('securePttTx').style = style;
            }
            if ( trimmedString === "rx-on" )
            {
                var style="font: 8px 'Helvetica Neue', Arial, Helvetica, sans-serif;padding: 1px;border: 1px solid #0E0;color: #0F0;background-color: #D00;";
                document.getElementById('securePttRx').style = style;
            }
            if ( trimmedString === "rx-off" )
            {
                var style="font: 8px 'Helvetica Neue', Arial, Helvetica, sans-serif;padding: 1px;border: 1px solid #0E0;color: #0F0;background-color: transparent;";
                document.getElementById('securePttRx').style = style;
            }
        };
    }

    
    // ===================
    // statusSocket (8997)
    // ===================
    if ( messagingFeatureEnabled ) {
        if ( wsProtocol == "ws://" )
            statusSocket = new WebSocket(wsProtocol+wsHost+':7997');
        if ( wsProtocol == "wss://" )
            statusSocket = new WebSocket(wsProtocol+wsHost+':8997');
            
        statusSocket.onopen = function(event) {
            document.getElementById('statusSocketStatus').style="display:block; padding-top:5px;"; 
            document.getElementById('statusSocketStatusRed').style="display:none;";
            statusSocketConnected=true;
        };
        statusSocket.onclose = function(event) {
            document.getElementById('statusSocketStatusRed').style="display:block; padding-top:5px;";
            document.getElementById('statusSocketStatus').style="display:none;";
            statusSocketConnected=false;
        };
        
        statusSocket.onmessage = function(event) {
            var incomingMessage = event.data;
            var trimmedString = incomingMessage.substring(0, 80);
            // console.log("DEBUG: ", trimmedString)
            const nodeArray = trimmedString.split(",");
            
            // meshtastic
            if ( nodeArray[0] === "peernode" )
            {
                meshtasticRadiosOnSystem.add( nodeArray[1], Math.round(+new Date()/1000),nodeArray[2],nodeArray[3],nodeArray[4],nodeArray[5],nodeArray[6] );
                updateMeshtasticRadioListBlock(); 
            }
            
            // reticulumnode,[callsign],[timestamp],[hash]
            if ( nodeArray[0] === "reticulumnode" )
            {
                // console.log("reticulumNodesOnSystem.add() : ", nodeArray[1],nodeArray[2],nodeArray[3],nodeArray[4],nodeArray[5],nodeArray[6],nodeArray[7] );
                reticulumNodesOnSystem.add( nodeArray[1],nodeArray[2],nodeArray[3],nodeArray[4],nodeArray[5],nodeArray[6],nodeArray[7] ); 
                updateReticulumBlock(); 
            }
            fadeIn(reticulumNotifyDotDiv,200);
            if ( ! isHidden(reticulumListblockDiv) ) {
                fadeOut(reticulumNotifyDotDiv,10000);
            }
            // announcereceived,[callsign],[hash]
            if ( nodeArray[0] === "announcereceived" ) {
                // notifyMessage("Announce from " + nodeArray[1], 5000);
                // 
                document.getElementById("reticulumAnnounceNotify").innerHTML = nodeArray[1];
            }
            // message-ack,[callsign]
            if ( nodeArray[0] === "message-ack" ) {
                delivery_ack_node = nodeArray[1];
                document.getElementById("delivery_status_header").innerHTML = "Delivery acknowledge from:";
                document.getElementById("delivery_status").innerHTML += "<span style='color:#0F0;'> "+delivery_ack_node+"</span>";  
            }
            if ( nodeArray[0] === "client_count" ) { 
                clients_connected = nodeArray[1];
                notifyMessage("Clients connected: " + clients_connected, 5000);
            }
        };
    
    }

    // Hide development icons
    document.getElementById('trackingIndicator').style="display:none;"; 
    document.getElementById('trackingIndicatorRed').style="display:none;";
    document.getElementById('messagingSocketStatus').style="display:none;";
    document.getElementById('statusSocketStatus').style="display:none;";
    document.getElementById('messagingSocketStatusRed').style="display:none;";
    document.getElementById('statusSocketStatusRed').style="display:none;";

    //
    // 'info window' open and close logic
    //
    /*
    const targetDiv = document.getElementById("info-box");
    const btn = document.getElementById("infobox-close");
    const infoIcon = document.getElementById("info-icon");
    btn.onclick = function () {
      if (targetDiv.style.display !== "none") {
        targetDiv.style.display = "none";
      } else {
        targetDiv.style.display = "block";
      }
    };
    infoIcon.onclick = function () {
      if ( targetDiv.style.display == "" )
      {
          targetDiv.style.display = "block";
      } else {
          if (targetDiv.style.display !== "none" ) {
            targetDiv.style.display = "none";
          } else {
            targetDiv.style.display = "block";
          }
        }
    };*/
	
    //
    // 'log-window' open and close logic variables
    //
    const logIcon = document.getElementById("log-icon");
    const logDiv = document.getElementById("log-window");
    const bottomBarDiv = document.getElementById("bottomBar");
    const callSignEntryBoxDiv =  document.getElementById("callSignEntry");
    const coordinateEntryBoxDiv =  document.getElementById("coordinateSearchEntry");
    const languageSelectDialogDiv =  document.getElementById("languageSelectDialog");     
    const peerlistblockDiv =  document.getElementById("peerlistblock"); 
    const radiolistblockDiv =  document.getElementById("radiolistblock");
    const userlistbuttonDiv = document.getElementById("userlistbutton");   
    const radiolistbuttonDiv = document.getElementById("meshtasticButton");
    const radioNotifyDotDiv = document.getElementById("radioNotifyDot"); 
    const reticulumNotifyDotDiv = document.getElementById("reticulumNotifyDot");    // DEV
    const reticulumListblockDiv =  document.getElementById("reticulumlistblock");   // DEV
    const reticulumListButtonDiv = document.getElementById("reticulumButton");      // DEV
    const videoConferenceDiv = document.getElementById("videoBlock");
    const deliveryStatusDiv = document.getElementById("delivery-status-window"); 
    const mapClickLatlonSectionDiv = document.getElementById("mapClickLatlonSection");
    
    //
    // Set rtl text plugin and pmtiles protocol
    //
    maplibregl.setRTLTextPlugin('js/mapbox-gl-rtl-text.js',null,true);
    let protocol = new pmtiles.Protocol();
    maplibregl.addProtocol("pmtiles",protocol.tile);

    //
    // Drag marker
    //
    dragMarker = new maplibregl.Marker({
        draggable: true
    });    
    dragMarker.setLngLat([0,0]);
    dragMarker.setPopup(dragMarkerPopup);
    dragMarkerPopup.setText("shared marker");
    dragMarkerPopup.addTo(map);
    dragMarker.on('dragend', onDragEnd);
    dragMarker.on('drag', onDrag);
    // dragMarker.addTo(map);
    
    //
    // Reference draggable marker with MilSymbols
    //
    // Use as template or test terrain model with it
    // 
    var graphMarker;
    var graphMarkerPopup = new maplibregl.Popup({offset: 35});
    const milSymbolGraph = new ms.Symbol("SFGPUCR-----", { size:20,
                dtg: "",
                staffComments: "".toUpperCase(),
                additionalInformation: "".toUpperCase(),
                combatEffectiveness: "READY".toUpperCase(),
                type: "",
                padding: 5
                }).asDOM();
    graphMarker = new maplibregl.Marker({
        element: milSymbolGraph,
        draggable: true
    });    
    graphMarker.setLngLat([15,15]);
    graphMarker.setPopup(graphMarkerPopup);
    graphMarkerPopup.setText("Graphical marker");
    // Uncomment this to add symbol to map:
    // graphMarker.addTo(map);

    //
    // PNG from milsymbols to statusbar (not in use)
    //
    var milSymbolTest = new ms.Symbol("SFGCUCR-----", { size:10,
            dtg: "",
            staffComments: "".toUpperCase(),
            additionalInformation: "".toUpperCase(),
            combatEffectiveness: "".toUpperCase(),
            type: "".toUpperCase(),
            padding: 5
        }).asCanvas().toDataURL();
    //document.getElementById('debugImage').src = milSymbolTest;
    //document.getElementById('debugImage').style="display:none;";


    // Update meshtastic and reticulum nodes every 30 s to UI
    // Note: updateReticulumBlock() has also age checking 
    window.setInterval(function () {
        checkMeshtasticRadioExpiry();
        updateMeshtasticRadioListBlock();
        if ( messagingFeatureEnabled ) {
            checkReticulumRadioExpiry();
            updateReticulumBlock(); 
        }
    }, 30000 );

    //
    // Interval loading function for geojson
    //
    var mapLoaded = false;
    var request = new XMLHttpRequest();
    window.setInterval(function () {

        if ( geoJsonLayerActive && mapLoaded ) {

            //
            // Get geojson
            // NOTE: You need cotsim -> curlcot -> taky for this to work
            // getElementItem('#myCallSign').value
            var geojsonUrlwithCallSign = 'meshtastic_geojson.php?linkline=1&myCallSign=' + getElementItem('#myCallSign').value;
            // request.open('GET', geojsonUrl, true);
            request.open('GET', geojsonUrlwithCallSign, true);
            request.onload = function () {
                    if (this.status >= 200 && this.status < 400) {
                        // 
                        // First 'geojson' parse to create symbol images
                        // 
                        if ( this.response == "" ) {
                            return;
                        }
                        var name;
                        var another = JSON.parse(this.response, function (key, value) {			
                            if ( key == "targetName" ) {
                                name = value;
                                if ( !map.hasImage( value ) ) {
                                    createImage( value );
                                }
                            }
                            // Update image with timestamp
                            // NOTE: this is not active in demo
                            if ( key == "time-stamp" ) {
                                // Test to calculate 'age' of fix. Not in use.
                                // Note: cotsim, curlcot does not provide time
                                // on test tracks! Just location.
                                let currentTime = new Date();
                                let expireTime = new Date(value);
                                let ageSeconds = (currentTime - expireTime ) / (1000 );
                                roundedAge = Math.round(ageSeconds);
                                roundedAgeString = roundedAge.toString();
                                updateImage(name, value, roundedAgeString );
                            }
                        });
                        //
                        // Second: set 'json' to 'drone' source.
                        //
                        var json = JSON.parse(this.response);
                        if (  map.getSource('drone') ) {
                            map.getSource('drone').setData(json);
                        }
                        // Time of update to UI
                        // var today = new Date();
                        // document.getElementById('status').innerHTML = today.toISOString();
                        // indicator.style.backgroundColor = 'transparent';
                    }
                    
                };
            request.send();
        } else {
            // console.log("Map not loaded yet or geoJsonLayer is false");
        }
    }, 4000 );
    
    //
    // Set an event listener that will fire
    // when the map has finished loading
    //
    map.on('load', function () {
        // notifyMessage("EdgeMap "+ edgemapUiVersion +" ready!", 5000);
        fadeIn(document.getElementById("platform_status") ,1000);
        fadeIn(document.getElementById("platform_help") ,1000);
        fadeIn(document.getElementById("platform_logo") ,1000);
        if ( geoJsonLayerActive  ) {
            console.log("Activating geojson layer")
            // 
            // 'drone' is target layer for geojson data
            // TODO: Calculating icon-offset for symbology text changes 
            // 
            map.addSource('drone', { type: 'geojson', data: geojsonUrl });
            map.addLayer({
                'id': 'drone',
                'type': 'symbol',
                'source': 'drone',
                'layout': {
                    'icon-image': ['get', 'targetName'], 
                    'icon-anchor': 'center',
                    'icon-offset': [0,0],   
                    'icon-allow-overlap': true,
                    'icon-ignore-placement': true, 
                    'text-allow-overlap': true,
                    'text-field': ['get', 'targetName'],
                    'text-font': [
                    'Noto Sans Regular'
                    ],
                    'text-offset': [0, 1.2],
                    'text-anchor': 'top'
                    },
                    'paint': {
                      "text-color": "#00f",
                      "text-halo-color": "#eee",
                      "text-halo-width": 2,
                      "text-halo-blur": 2
                    },
                    'filter': ['==', '$type', 'Point']
            });
            // Enable tails for targets
            // showTails();
        }
        console.log("Map loaded.");
        map.setTerrain(null);
        loadCallSign();
        mapLoaded = true;
        setSkyFromUi();
        // Fade out help
        window.setInterval(function () {
        fadeOut(document.getElementById("platform_help") ,1000);
        fadeOut(document.getElementById("platform_logo") ,1000);
        }, 15000 );
        
        showTails();
        
    });
    
    // 
    // map feature debug if off by default (use D to enable)
    //
    document.getElementById('features').style.display = 'none';     
    
    // ====================================
    // Geolocate (requires TLS)
    // Firefox: about:config => geo.enabled
    // ====================================
    
    // Initialize and add the geolocate control
    let geolocate = new maplibregl.GeolocateControl({
      positionOptions: {
          enableHighAccuracy: true
      },
      trackUserLocation: true
    });

    // This control is disabled because we use only locally connected GPS
    // (or manually set) location. Browser location usage is TLS nightmare
    // and activates lot of emissions towards IP network.
    // map.addControl(geolocate);
    
    // Callback functions for geolocation
    geolocate.on('trackuserlocationstart', function() {
      document.getElementById('trackingIndicator').style="display:block;";
      document.getElementById('trackingIndicatorRed').style="display:none;";
      document.getElementById('gpsStatus').innerHTML = "GPS";
    });
    // On 'track end' deliver last known coordinates and 'Stopped' message
    geolocate.on('trackuserlocationend', function() {
        document.getElementById('trackingIndicator').style="display:none;"; 
        document.getElementById('trackingIndicatorRed').style="display:block;";
        document.getElementById('gpsStatus').innerHTML = "";      
        // NOTE: On meshtastic branch we disable sending geolocation. Bandwidth issue.
        // sendMessageToAllBearers( callSign + `|trackMarker|${lastKnownCoordinates.longitude},${lastKnownCoordinates.latitude}|Stopped` + '\n' );
    });

    // Call back for position updates, fire 'trackMarker' message from these
    geolocate.on('geolocate', function(pos) {
        const crd = pos.coords;
        lastKnownCoordinates = pos.coords;
        // Populate image upload form fields, just in case someone
        // likes to take and send a photo
        const formInfo = document.forms['uploadform'];
        formInfo.lat.value = `${crd.latitude}`;
        formInfo.lon.value = `${crd.longitude}`;
        document.getElementById('gpsStatus').innerHTML = "GPS";
        // Create & send trackMarker message when geolocate is active
        // NOTE: On meshtastic branch we have disabled geolocation send to other memebers. Bandwidth issue.
        // sendMessageToAllBearers ( callSign + `|trackMarker|${crd.longitude},${crd.latitude}|tracking` + '\n' );
    });

    // Sprite loading request transform, see styles/style.json
    map.setTransformRequest( (url, resourceType) => {
            if (/^local:\/\//.test(url)) {
                return { url: new URL(url.substr('local://'.length), location.protocol+'//'+location.host).href };
            }
        }
    );
    
    feather.replace();
    
    // Capture click coordinates to UI 
    map.on('mousedown', function (e) {	
        JSON.parse(JSON.stringify(e.lngLat.wrap()) , (key, value) => {
          if ( key == 'lat' ) {
              let uLat = value.toString();
              document.getElementById('lat').innerHTML = uLat.substring(0,10);
                if ( unknownSensorCreateInProgress == 1 ) {
                  document.getElementById('sensorLat').innerHTML = uLat.substring(0,10);
                  document.getElementById('sensorLatLonComma').innerHTML = ",";
                  document.getElementById('sensorLocationTooltip').innerHTML = "Pos: ";
                  document.getElementById('sensor-create-input-placeholder').style.display = "none";
                  document.getElementById('sensor-create-input').style.display = "block";
                }
                if ( manualLocationCreateInProgress == 1 ) {
                  document.getElementById('manualLocation-Lat').innerHTML = uLat.substring(0,10);
                  document.getElementById('manualLocation-LatLonComma').innerHTML = ",";
                  document.getElementById('manualLocation-Tooltip').innerHTML = "Pos: ";
                  document.getElementById('manualLocation-create-input-placeholder').style.display = "none";
                  document.getElementById('manualLocation-create-input').style.display = "block";
                }
          }
          if ( key == 'lng' ) {
              let uLon = value.toString();
                document.getElementById('lon').innerHTML = uLon.substring(0,10);
                document.getElementById("copyNotifyText").innerHTML = "";
                document.getElementById("coordinateComma").innerHTML = ",";
                if ( document.getElementById("mapClickLatlonSection").style.visibility != "visible") {
                    fadeIn( document.getElementById("mapClickLatlonSection"), 400 );
                }
              
                if ( unknownSensorCreateInProgress == 1 ) {
                    document.getElementById('sensorLon').innerHTML = uLon.substring(0,10);
                }
                if ( manualLocationCreateInProgress == 1 ) {
                    document.getElementById('manualLocation-Lon').innerHTML = uLon.substring(0,10);
                }
          }
        });	
    });
    
    map.on('zoom', function () {
            let zoom = map.getZoom();
    });
   
    // Testing new menu, let's hide old - do this proper when done
    
    /*fadeOut(zoomDiv,120);
    fadeOut(sensorDiv,120);
    // fadeOut(bottomBarDiv,120);
    fadeOut(cameracontrol,120);
    fadeOut(userlistbuttonDiv ,120);
    fadeOut(radiolistbuttonDiv ,120);
    fadeOut(radiolistblockDiv ,120);
    fadeOut(videoconferenceButton ,120);
    fadeOut(reticulumListblockDiv ,120);
    fadeOut(reticulumListButtonDiv ,120);
    fadeOut(manualGpsbuttonDiv ,120);
    */
    
    // Radial menu test
    // REMOVED FOR NG

    //
    // Keypress functions
    //
    function handleKeyPress(e){
        if (keyEventListener) {
         var key=e.keyCode || e.which;
          if (key==13){
            let inputValue = document.getElementById('coordinateInput').value;
            const coordValue = inputValue.split(",");
            if ( check_lat_lon(coordValue[1],coordValue[0]) == true) {
                console.log("AddDot: ",coordValue[1],coordValue[0]);
                removeDot();
                addDot(coordValue[1],coordValue[0]);
            }
            document.getElementById('coordinateInput').value="";   
            closeCoordinateSearchEntryBox();
          }
      }
    }

    document.addEventListener("keyup", function(event) {
        const key = event.key;
        
        if (keyEventListener) {
        
            // Messaging
            if (key === "m") {
               if ( isHidden(logDiv) ) openMessageEntryBox();
            }
            // SVG Menu test
            if (key === "s") {
               // svgMenu.open();
            }
            // Meshtastic list
            if (key === "r") {
               if ( isHidden(radiolistblockDiv) || isHidden(logDiv) ) {
                   openRadioList();
               }
            }
            
            // Reticulum list
            if (key === "R") {
               if ( isHidden(reticulumListblockDiv) || isHidden(logDiv) ) {
                   openReticulumList();
               }
            }
            
            
            // Enable map features debugging if needed
            if (key === "D") {
                if ( isHidden(logDiv) ) { 
                    if ( document.getElementById('features').style.display === 'block' ) {
                        document.getElementById('features').style.display = 'none'; 
                        map.off('mousemove', showFeatures );
                    } else {
                        document.getElementById('features').style.display = 'block'; 
                        map.on('mousemove', showFeatures );
                    }
                }
            }
            // Open coordinate find only if message entry (logDiv) is hidden
            if (key === "f") {   
                if ( isHidden(logDiv) ) {
                    removeDot();
                    openCoordinateSearchEntryBox();
                    document.getElementById('coordinateInput').value="";
                }
            }
            if (key === "Escape") {
                document.getElementById('coordinateInput').value="";   
                if ( !isHidden(coordinateEntryBoxDiv) ) closeCoordinateSearchEntryBox();
                // if ( !isHidden(languageSelectDialogDiv) ) closeLanguageSelectBox(); // REMOVE
                if ( !isHidden(logDiv) ) closeMessageEntryBox();
                if ( !isHidden(radiolistblockDiv) ) closeRadioList();
                if ( !isHidden(reticulumListblockDiv) ) closeReticulumList();
            }
            if (key === "h") {
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
        }
    });
    
</script>

<div style="position: absolute; top: -9999px; left: -9999px;">

    <svg id="svg-icon-my-location"  xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="#0F0" d="M11 22.95v-2q-3.125-.35-5.363-2.587T3.05 13h-2v-2h2q.35-3.125 2.588-5.363T11 3.05v-2h2v2q3.125.35 5.363 2.588T20.95 11h2v2h-2q-.35 3.125-2.587 5.363T13 20.95v2zM12 19q2.9 0 4.95-2.05T19 12t-2.05-4.95T12 5T7.05 7.05T5 12t2.05 4.95T12 19m0-3q-1.65 0-2.825-1.175T8 12t1.175-2.825T12 8t2.825 1.175T16 12t-1.175 2.825T12 16m0-2q.825 0 1.413-.587T14 12t-.587-1.412T12 10t-1.412.588T10 12t.588 1.413T12 14m0-2"/></svg>
    <svg id="svg-icon-camera" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="#0F0" d="M20.6 6.325q0-1.65-1.137-2.787T16.675 2.4q-.275 0-.475-.212T16 1.7t.2-.475t.475-.2q2.2 0 3.75 1.55t1.55 3.75q0 .275-.2.475T21.3 7t-.488-.2t-.212-.475m-2.7.025q0-.525-.362-.887T16.65 5.1q-.275 0-.462-.212T16 4.4t.2-.475t.475-.2q1.075 0 1.838.763t.762 1.837q0 .275-.2.475T18.6 7t-.488-.187t-.212-.463M4 21q-.825 0-1.412-.587T2 19V7q0-.825.588-1.412T4 5h3.15L8.4 3.65q.275-.3.663-.475T9.875 3H14q.425 0 .713.288T15 4t-.288.713T14 5H9.875L8.05 7H4v12h16V9q0-.425.288-.712T21 8t.713.288T22 9v10q0 .825-.587 1.413T20 21zm8-3.5q1.875 0 3.188-1.312T16.5 13t-1.312-3.187T12 8.5T8.813 9.813T7.5 13t1.313 3.188T12 17.5m0-2q-1.05 0-1.775-.725T9.5 13t.725-1.775T12 10.5t1.775.725T14.5 13t-.725 1.775T12 15.5"/></svg>
    <svg id="svg-icon-meshtastic" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 48 48"><path fill="none" stroke="#0F0" stroke-width=".4em" stroke-linecap="round" stroke-linejoin="round" d="m5.5 32.667l13-17.334m26 17.334l-13-17.334l-13 17.334"/></svg>
    <svg id="svg-icon-reticulum" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 512 512"><path fill="#0F0" d="M363.6 36.48c-22.2 0-40 17.8-40 40c0 22.23 17.8 40.02 40 40.02s40-17.79 40-40.02c0-22.2-17.8-40-40-40m-56.7 51.97c-53.2 18.95-108.7 34.95-169 45.25c1.8 4.6 2.8 9.6 2.8 14.8c0 4.8-.8 9.4-2.4 13.6c96.2 12.9 182.8 36 257.8 71.9c1.6-5.9 4.5-11.3 8.3-15.9c-71.2-34.3-152.4-57.2-241.5-70.7c53.2-10.6 102.8-25.4 150.4-42.2c-3-5.2-5.2-10.79-6.4-16.75m97.8 28.85c-4.3 4.3-9.2 8-14.6 10.8c15.3 24.8 26 50.6 31.8 77.8c4.3-1.5 9-2.4 13.8-2.4c1.4 0 2.8.1 4.1.2c-6.3-30.3-18.2-59.1-35.1-86.4m-305 8.2c-12.81 0-23 10.2-23 23s10.19 23 23 23c12.8 0 23-10.2 23-23s-10.2-23-23-23m34.7 44.6c-3.2 5.2-7.5 9.6-12.6 12.9c32.1 32.6 66.1 65.9 120.6 80.4c0-.9-.1-1.9-.1-2.8c0-5.3 1.3-10.3 3.5-14.8c-49.5-13.5-80-43.8-111.4-75.7m-57 12.7c-21.76 67.8-27.12 137.2-32.29 206c2.13-.5 4.34-.7 6.6-.7c3.99 0 7.81.7 11.35 2.1c5.19-68.4 10.57-136 31.29-201.1c-6.18-.8-11.94-3-16.95-6.3m358.3 38.7c-12.8 0-23 10.2-23 23s10.2 23 23 23s23-10.2 23-23s-10.2-23-23-23m-41 22.2c-28.4 5.8-56.6 10.8-86 10.5c.4 2.1.6 4.2.6 6.4c0 4-.7 7.9-2.1 11.5c32 .6 62-4.7 91.2-10.8c-2.4-5.1-3.7-10.8-3.7-16.8zm-118.9 1.4c-8.7 0-15.5 6.8-15.5 15.5s6.8 15.5 15.5 15.5s15.5-6.8 15.5-15.5s-6.8-15.5-15.5-15.5M399 262.7c-55.6 45.9-106.6 94.4-143.1 150.7c5.9 1.8 11.2 5 15.6 9.1c34.9-53.5 84.2-100.8 138.8-145.9c-4.7-3.7-8.6-8.5-11.3-13.9m-152 15c-47.9 46.4-109.6 83.2-172.85 119.5c4.36 4.2 7.56 9.6 9.05 15.6C146.8 376.4 210 338.9 260 290.1c-5.4-2.9-9.9-7.2-13-12.4m179.4 6.7c1.3 28.8 6 57.3 14.3 85.2c4.8-3.4 10.7-5.6 17-6c-7.6-26-11.9-52.3-13.2-79.1c-2.9.7-5.8 1-8.8 1c-3.2 0-6.3-.4-9.3-1.1m33.3 97.1c-8.4 0-15 6.6-15 15s6.6 15 15 15s15-6.6 15-15s-6.6-15-15-15M51.71 406.1c-8.07 0-14.42 6.4-14.42 14.4c0 8.1 6.35 14.5 14.42 14.5s14.42-6.4 14.42-14.5c0-8-6.35-14.4-14.42-14.4m376.49.3c-44.7 24.5-93.8 32.6-144.9 35.6c.9 3.4 1.4 6.9 1.4 10.5c0 2.6-.3 5.1-.7 7.5c53.1-3.1 105.8-11.6 154.3-38.5c-4.7-4-8.2-9.2-10.1-15.1M83.91 416.8c.14 1.2.22 2.4.22 3.7c0 5-1.15 9.7-3.19 14l121.86 20.3c-.1-.8-.1-1.5-.1-2.3c0-5.4 1.1-10.6 3-15.4zm159.79 12.7c-12.8 0-23 10.2-23 23s10.2 23 23 23s23-10.2 23-23s-10.2-23-23-23"/></svg>
    <svg id="svg-icon-message" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24"><path fill="#0F0" d="M8 11q.425 0 .713-.288T9 10t-.288-.712T8 9t-.712.288T7 10t.288.713T8 11m4 0q.425 0 .713-.288T13 10t-.288-.712T12 9t-.712.288T11 10t.288.713T12 11m4 0q.425 0 .713-.288T17 10t-.288-.712T16 9t-.712.288T15 10t.288.713T16 11M2 22V4q0-.825.588-1.412T4 2h16q.825 0 1.413.588T22 4v12q0 .825-.587 1.413T20 18H6zm3.15-6H20V4H4v13.125zM4 16V4z"/></svg>
    <svg id="svg-icon-terrain" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 24 24"><path fill="#0F0" d="m14 6l-4.22 5.63l1.25 1.67L14 9.33L19 16h-8.46l-4.01-5.37L1 18h22zM5 16l1.52-2.03L8.04 16z"/></svg>
    <svg id="svg-icon-more" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 16 16"><path fill="#0F0" d="M3 8a5 5 0 1 1 10 0A5 5 0 0 1 3 8m5-6a6 6 0 1 0 0 12A6 6 0 0 0 8 2m0 7a1 1 0 1 0 0-2a1 1 0 0 0 0 2m4-1a1 1 0 1 1-2 0a1 1 0 0 1 2 0M5 9a1 1 0 1 0 0-2a1 1 0 0 0 0 2"/></svg>
    <svg id="svg-icon-language" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 512 512"><path fill="#0F0" d="m478.33 433.6l-90-218a22 22 0 0 0-40.67 0l-90 218a22 22 0 1 0 40.67 16.79L316.66 406h102.67l18.33 44.39A22 22 0 0 0 458 464a22 22 0 0 0 20.32-30.4ZM334.83 362L368 281.65L401.17 362Zm-66.99-19.08a22 22 0 0 0-4.89-30.7c-.2-.15-15-11.13-36.49-34.73c39.65-53.68 62.11-114.75 71.27-143.49H330a22 22 0 0 0 0-44H214V70a22 22 0 0 0-44 0v20H54a22 22 0 0 0 0 44h197.25c-9.52 26.95-27.05 69.5-53.79 108.36c-31.41-41.68-43.08-68.65-43.17-68.87a22 22 0 0 0-40.58 17c.58 1.38 14.55 34.23 52.86 83.93c.92 1.19 1.83 2.35 2.74 3.51c-39.24 44.35-77.74 71.86-93.85 80.74a22 22 0 1 0 21.07 38.63c2.16-1.18 48.6-26.89 101.63-85.59c22.52 24.08 38 35.44 38.93 36.1a22 22 0 0 0 30.75-4.9Z"/></svg>
    <svg id="svg-icon-coordinate-search" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 24 24"><g fill="none" stroke="#0F0" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M21 12a9 9 0 1 0-9 9M3.6 9h16.8M3.6 15h7.9"/><path d="M11.5 3a17 17 0 0 0 0 18m1-18a17 17 0 0 1 2.574 8.62M15 18a3 3 0 1 0 6 0a3 3 0 1 0-6 0m5.2 2.2L22 22"/></g></svg>
    <svg id="svg-icon-about" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 24 24"><path fill="#0F0" d="M11 9h2V7h-2m1 13c-4.41 0-8-3.59-8-8s3.59-8 8-8s8 3.59 8 8s-3.59 8-8 8m0-18A10 10 0 0 0 2 12a10 10 0 0 0 10 10a10 10 0 0 0 10-10A10 10 0 0 0 12 2m-1 15h2v-6h-2z"/></svg>
    <svg id="svg-icon-language-en" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 36 36"><path fill="#00247d" d="M0 9.059V13h5.628zM4.664 31H13v-5.837zM23 25.164V31h8.335zM0 23v3.941L5.63 23zM31.337 5H23v5.837zM36 26.942V23h-5.631zM36 13V9.059L30.371 13zM13 5H4.664L13 10.837z"/><path fill="#cf1b2b" d="m25.14 23l9.712 6.801a4 4 0 0 0 .99-1.749L28.627 23zM13 23h-2.141l-9.711 6.8c.521.53 1.189.909 1.938 1.085L13 23.943zm10-10h2.141l9.711-6.8a4 4 0 0 0-1.937-1.085L23 12.057zm-12.141 0L1.148 6.2a4 4 0 0 0-.991 1.749L7.372 13z"/><path fill="#eee" d="M36 21H21v10h2v-5.836L31.335 31H32a4 4 0 0 0 2.852-1.199L25.14 23h3.487l7.215 5.052c.093-.337.158-.686.158-1.052v-.058L30.369 23H36zM0 21v2h5.63L0 26.941V27c0 1.091.439 2.078 1.148 2.8l9.711-6.8H13v.943l-9.914 6.941c.294.07.598.116.914.116h.664L13 25.163V31h2V21zM36 9a3.98 3.98 0 0 0-1.148-2.8L25.141 13H23v-.943l9.915-6.942A4 4 0 0 0 32 5h-.663L23 10.837V5h-2v10h15v-2h-5.629L36 9.059zM13 5v5.837L4.664 5H4a4 4 0 0 0-2.852 1.2l9.711 6.8H7.372L.157 7.949A4 4 0 0 0 0 9v.059L5.628 13H0v2h15V5z"/><path fill="#cf1b2b" d="M21 15V5h-6v10H0v6h15v10h6V21h15v-6z"/></svg>
    <svg id="svg-icon-language-zh" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 36 36"><path fill="#de2910" d="M36 27a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4V9a4 4 0 0 1 4-4h28a4 4 0 0 1 4 4z"/><path fill="#ffde02" d="m11.136 8.977l.736.356l.589-.566l-.111.81l.72.386l-.804.144l-.144.804l-.386-.72l-.81.111l.566-.589zm4.665 2.941l-.356.735l.566.59l-.809-.112l-.386.721l-.144-.805l-.805-.144l.721-.386l-.112-.809l.59.566zm-.957 3.779l.268.772l.817.017l-.651.493l.237.783l-.671-.467l-.671.467l.236-.783l-.651-.493l.817-.017zm-3.708 3.28l.736.356l.589-.566l-.111.81l.72.386l-.804.144l-.144.804l-.386-.72l-.81.111l.566-.589zM7 10.951l.929 2.671l2.826.058l-2.253 1.708l.819 2.706L7 16.479l-2.321 1.615l.819-2.706l-2.253-1.708l2.826-.058z"/></svg>
    <svg id="svg-icon-language-ukr" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 36 36"><path fill="#005bbb" d="M32 5H4a4 4 0 0 0-4 4v9h36V9a4 4 0 0 0-4-4"/><path fill="#ffd500" d="M36 27a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4v-9h36z"/></svg>
    <svg id="svg-icon-language-ar" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6v4m3 4h8q-2.518-3-4-3m-4-5v9.958c0 .963 0 1.444-.293 1.743S11.943 18 11 18h-1M7 6v9.958c0 .963 0 1.444-.293 1.743S5.943 18 5 18H4"/></svg>
    <svg id="svg-icon-language-de" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 36 36"><path fill="#ffcd05" d="M0 27a4 4 0 0 0 4 4h28a4 4 0 0 0 4-4v-4H0z"/><path fill="#ed1f24" d="M0 14h36v9H0z"/><path fill="#141414" d="M32 5H4a4 4 0 0 0-4 4v5h36V9a4 4 0 0 0-4-4"/></svg>
    <svg id="svg-icon-language-es" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 36 36"><path fill="#c60a1d" d="M36 27a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4V9a4 4 0 0 1 4-4h28a4 4 0 0 1 4 4z"/><path fill="#ffc400" d="M0 12h36v12H0z"/><path fill="#ea596e" d="M9 17v3a3 3 0 1 0 6 0v-3z"/><path fill="#f4a2b2" d="M12 16h3v3h-3z"/><path fill="#dd2e44" d="M9 16h3v3H9z"/><ellipse cx="12" cy="14.5" fill="#ea596e" rx="3" ry="1.5"/><ellipse cx="12" cy="13.75" fill="#ffac33" rx="3" ry=".75"/><path fill="#99aab5" d="M7 16h1v7H7zm9 0h1v7h-1z"/><path fill="#66757f" d="M6 22h3v1H6zm9 0h3v1h-3zm-8-7h1v1H7zm9 0h1v1h-1z"/></svg>
    <svg id="svg-icon-language-fr" xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 36 36"><path fill="#ed2939" d="M36 27a4 4 0 0 1-4 4h-8V5h8a4 4 0 0 1 4 4z"/><path fill="#002495" d="M4 5a4 4 0 0 0-4 4v18a4 4 0 0 0 4 4h8V5z"/><path fill="#eee" d="M12 5h12v26H12z"/></svg>
    <svg id="svg-icon-language-ru"  xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 36 36"><path fill="#ce2028" d="M36 27a4 4 0 0 1-4 4H4a4 4 0 0 1-4-4v-4h36z"/><path fill="#22408c" d="M0 13h36v10H0z"/><path fill="#eee" d="M32 5H4a4 4 0 0 0-4 4v4h36V9a4 4 0 0 0-4-4"/></svg>
    <svg id="svg-icon-language-he"  xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M7 6c2.333 5.143 6.611 6.857 9.333 12"/><path d="M13.667 14c2.505-1.5 2.666-4.141 2.666-5.333C16.333 6.889 15.89 6 15.89 6M7.485 18S7 17.095 7 15.286c0-1.172.164-3.722 2.641-5.27"/></g></svg>
    
    <svg id="svg-icon-meshtasticMsgsocket-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#0F0" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9h8m-8 4h6m-1 7l-1 1l-3-3H6a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v5.5M19 16l-2 3h4l-2 3"/></svg>
    <svg id="svg-icon-reticulumMsgsocket-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#0F0" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9h8m-8 4h6m-2 8l-1-1l-2-2H6a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v6m-1 8l2-2l-2-2m-3 0l-2 2l2 2"/></svg>
    <svg id="svg-icon-ptt-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#0F0" d="M9 2a1 1 0 0 0-1 1v17c0 1.11.89 2 2 2h5c1.11 0 2-.89 2-2V9c0-1.11-.89-2-2-2h-5V3a1 1 0 0 0-1-1m1 7h5v4h-5z"/></svg>
    <svg id="svg-icon-gnss-topbar" xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 100 100"><path fill="#0F0" d="M41.979 0C29.724.005 19.283 4.451 17.322 10.5h49.356C64.716 4.447 54.263 0 42 0ZM17.322 14.5c1.752 5.405 10.335 9.61 21.178 10.377V100h7v-2.828c5.832-.264 9.863-.495 11.822-2.14c1.96-1.647 5.939-2.275 8.998-2.198v5.486c0 .928.752 1.68 1.68 1.68h7.71v-1.68h14.9V100h7.71a1.68 1.68 0 0 0 1.68-1.68v-6.693h-1.68v-30.04H100V53.68A1.68 1.68 0 0 0 98.32 52H68a1.68 1.68 0 0 0-1.68 1.68v7.908H68v27.238c-7.951.135-10.084.933-12.951 2.914s-4.684 1.31-9.549 1.469V24.877c10.843-.767 19.426-4.972 21.178-10.377ZM72.4 58.08h21.52v35.84H72.4Zm2.628 3.473v13.56h16.32v-13.56Zm8.16 16.67a5.4 5.4 0 1 0 0 10.801a5.4 5.4 0 0 0 0-10.801" color="currentColor"/></svg>
    <svg id="svg-icon-meshtastic-topbar"xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 48 48"><path fill="none" stroke="#0F0" stroke-width=".4em" stroke-linecap="round" stroke-linejoin="round" d="m4.5 32.667l13-17.334m26 17.334l-13-17.334l-13 17.334"/></svg>
    <svg id="svg-icon-reticulum-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 48 48"><circle cx="22.04" cy="21.35" r="6.67" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="9.49" cy="12.19" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="29.01" cy="9.04" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="38.51" cy="25.38" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="35.77" cy="38.96" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12.51" cy="34.94" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m14.55 32.04l3.68-5.22M9.95 15.7l2.09 15.73m20.24 6.93l-16.29-2.82m21.82-6.69l-1.34 6.64M30.79 12.1l5.95 10.22m-23.72-10.7l12.5-2.02m-13.15 4.64l4.35 3.08m10.56-5.2l-1.92 3.43m9.73 8.95l-6.54-1.67m5.07 13.33l-7.37-9.64"/></svg>
    <svg id="svg-icon-highrate-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#0F0" d="M22 11h-1l-1-2h-6.25L16 12.5h-2L10.75 9H4c-.55 0-2-.45-2-1s1.5-2.5 3.5-2.5S7.67 6.5 9 7h12a1 1 0 0 1 1 1zM10.75 6.5L14 3h2l-2.25 3.5zM18 11V9.5h1.75L19 11zM3 19a1 1 0 0 1-1-1a1 1 0 0 1 1-1a4 4 0 0 1 4 4a1 1 0 0 1-1 1a1 1 0 0 1-1-1a2 2 0 0 0-2-2m8 2a1 1 0 0 1-1 1a1 1 0 0 1-1-1a6 6 0 0 0-6-6a1 1 0 0 1-1-1a1 1 0 0 1 1-1a8 8 0 0 1 8 8"/></svg>
    <svg id="svg-icon-tracking-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 1024 1024"><path fill="#0F0" d="m249.6 417.088l319.744 43.072l39.168 310.272L845.12 178.88zm-129.024 47.168a32 32 0 0 1-7.68-61.44l777.792-311.04a32 32 0 0 1 41.6 41.6l-310.336 775.68a32 32 0 0 1-61.44-7.808L512 516.992z"/></svg>    
    <svg id="svg-icon-meshtasticMsgsocket-red-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#F00" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9h8m-8 4h6m-1 7l-1 1l-3-3H6a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v5.5M19 16l-2 3h4l-2 3"/></svg>
    <svg id="svg-icon-reticulumMsgsocket-red-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#F00" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 9h8m-8 4h6m-2 8l-1-1l-2-2H6a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v6m-1 8l2-2l-2-2m-3 0l-2 2l2 2"/></svg>
    <svg id="svg-icon-ptt-red-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#F00" d="M9 2a1 1 0 0 0-1 1v17c0 1.11.89 2 2 2h5c1.11 0 2-.89 2-2V9c0-1.11-.89-2-2-2h-5V3a1 1 0 0 0-1-1m1 7h5v4h-5z"/></svg>
    <svg id="svg-icon-gnss-red-topbar" xmlns="http://www.w3.org/2000/svg" width="25" height="25" viewBox="0 0 100 100"><path fill="#F00" d="M41.979 0C29.724.005 19.283 4.451 17.322 10.5h49.356C64.716 4.447 54.263 0 42 0ZM17.322 14.5c1.752 5.405 10.335 9.61 21.178 10.377V100h7v-2.828c5.832-.264 9.863-.495 11.822-2.14c1.96-1.647 5.939-2.275 8.998-2.198v5.486c0 .928.752 1.68 1.68 1.68h7.71v-1.68h14.9V100h7.71a1.68 1.68 0 0 0 1.68-1.68v-6.693h-1.68v-30.04H100V53.68A1.68 1.68 0 0 0 98.32 52H68a1.68 1.68 0 0 0-1.68 1.68v7.908H68v27.238c-7.951.135-10.084.933-12.951 2.914s-4.684 1.31-9.549 1.469V24.877c10.843-.767 19.426-4.972 21.178-10.377ZM72.4 58.08h21.52v35.84H72.4Zm2.628 3.473v13.56h16.32v-13.56Zm8.16 16.67a5.4 5.4 0 1 0 0 10.801a5.4 5.4 0 0 0 0-10.801" color="currentColor"/></svg>
    <svg id="svg-icon-meshtastic-red-topbar"xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 48 48"><path fill="none" stroke="#F00" stroke-width=".4em" stroke-linecap="round" stroke-linejoin="round" d="m4.5 32.667l13-17.334m26 17.334l-13-17.334l-13 17.334"/></svg>
    <svg id="svg-icon-reticulum-red-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 48 48"><circle cx="22.04" cy="21.35" r="6.67" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="9.49" cy="12.19" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="29.01" cy="9.04" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="38.51" cy="25.38" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="35.77" cy="38.96" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12.51" cy="34.94" r="3.54" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"/><path fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="m14.55 32.04l3.68-5.22M9.95 15.7l2.09 15.73m20.24 6.93l-16.29-2.82m21.82-6.69l-1.34 6.64M30.79 12.1l5.95 10.22m-23.72-10.7l12.5-2.02m-13.15 4.64l4.35 3.08m10.56-5.2l-1.92 3.43m9.73 8.95l-6.54-1.67m5.07 13.33l-7.37-9.64"/></svg>
    <svg id="svg-icon-highrate-red-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#F00" d="M22 11h-1l-1-2h-6.25L16 12.5h-2L10.75 9H4c-.55 0-2-.45-2-1s1.5-2.5 3.5-2.5S7.67 6.5 9 7h12a1 1 0 0 1 1 1zM10.75 6.5L14 3h2l-2.25 3.5zM18 11V9.5h1.75L19 11zM3 19a1 1 0 0 1-1-1a1 1 0 0 1 1-1a4 4 0 0 1 4 4a1 1 0 0 1-1 1a1 1 0 0 1-1-1a2 2 0 0 0-2-2m8 2a1 1 0 0 1-1 1a1 1 0 0 1-1-1a6 6 0 0 0-6-6a1 1 0 0 1-1-1a1 1 0 0 1 1-1a8 8 0 0 1 8 8"/></svg>
    <svg  id="svg-icon-tracking-red-topbar" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 1024 1024"><path fill="#F00" d="m249.6 417.088l319.744 43.072l39.168 310.272L845.12 178.88zm-129.024 47.168a32 32 0 0 1-7.68-61.44l777.792-311.04a32 32 0 0 1 41.6 41.6l-310.336 775.68a32 32 0 0 1-61.44-7.808L512 516.992z"/></svg>
    
    <svg id="svg-icon-search" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" ><path fill="#0F0" d="M10 18a7.95 7.95 0 0 0 4.897-1.688l4.396 4.396l1.414-1.414l-4.396-4.396A7.95 7.95 0 0 0 18 10c0-4.411-3.589-8-8-8s-8 3.589-8 8s3.589 8 8 8m0-14c3.309 0 6 2.691 6 6s-2.691 6-6 6s-6-2.691-6-6s2.691-6 6-6"/></svg>
    <svg id="svg-icon-close" xmlns="http://www.w3.org/2000/svg" width="1.5em" height="1.5em" ><path fill="#F00" d="M2.93 17.07A10 10 0 1 1 17.07 2.93A10 10 0 0 1 2.93 17.07m1.41-1.41A8 8 0 1 0 15.66 4.34A8 8 0 0 0 4.34 15.66m9.9-8.49L11.41 10l2.83 2.83l-1.41 1.41L10 11.41l-2.83 2.83l-1.41-1.41L8.59 10L5.76 7.17l1.41-1.41L10 8.59l2.83-2.83z"/></svg>
    <svg id="svg-icon-copypaste" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><g fill="none" stroke="#0F0" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><rect width="8" height="4" x="8" y="2" rx="1" ry="1"/><path d="M8 4H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2M16 4h2a2 2 0 0 1 2 2v4m1 4H11"/><path d="m15 10l-4 4l4 4"/></g></svg>
    <svg xmlns="http://www.w3.org/2000/svg" width="1" height="1" viewBox="0 0 36 36"><path fill="#00247d" d="M0 9.059V13h5.628zM4.664 31H13v-5.837zM23 25.164V31h8.335zM0 23v3.941L5.63 23zM31.337 5H23v5.837zM36 26.942V23h-5.631zM36 13V9.059L30.371 13zM13 5H4.664L13 10.837z"/><path fill="#cf1b2b" d="m25.14 23l9.712 6.801a4 4 0 0 0 .99-1.749L28.627 23zM13 23h-2.141l-9.711 6.8c.521.53 1.189.909 1.938 1.085L13 23.943zm10-10h2.141l9.711-6.8a4 4 0 0 0-1.937-1.085L23 12.057zm-12.141 0L1.148 6.2a4 4 0 0 0-.991 1.749L7.372 13z"/><path fill="#eee" d="M36 21H21v10h2v-5.836L31.335 31H32a4 4 0 0 0 2.852-1.199L25.14 23h3.487l7.215 5.052c.093-.337.158-.686.158-1.052v-.058L30.369 23H36zM0 21v2h5.63L0 26.941V27c0 1.091.439 2.078 1.148 2.8l9.711-6.8H13v.943l-9.914 6.941c.294.07.598.116.914.116h.664L13 25.163V31h2V21zM36 9a3.98 3.98 0 0 0-1.148-2.8L25.141 13H23v-.943l9.915-6.942A4 4 0 0 0 32 5h-.663L23 10.837V5h-2v10h15v-2h-5.629L36 9.059zM13 5v5.837L4.664 5H4a4 4 0 0 0-2.852 1.2l9.711 6.8H7.372L.157 7.949A4 4 0 0 0 0 9v.059L5.628 13H0v2h15V5z"/><path fill="#cf1b2b" d="M21 15V5h-6v10H0v6h15v10h6V21h15v-6z"/></svg>    
    <svg id="svg-icon-distress2" xmlns="http://www.w3.org/2000/svg" width="2" height="2" viewBox="0 0 512 512"><path fill="#0F0" d="m68.79 19.5l57.51 69h23.4l-57.49-69zm185.31 0l59.4 178.3c5.5-2.1 11.2-4 17-5.7L273 19.5zm-92.2 83.7l-2.5 25.1l90.7 108.8c4.4-4.1 9-7.9 13.8-11.5zm-78.45 3.3l14.19 142h31.76l14.2-142zm302.05 96c-3.2 0-6.4.1-9.6.2L361 253.8l46.9-21.5l-3 43.1l40.5 12.4l-47.2 32.2l27 36.8l-51.8 11.6l8.3 53.6l-74.3-44.2l8.9-70.8l-28.4-44.7l58.9-55.7c-75.8 16.2-134 79.3-143.1 157.6l41.5-61.4l38.7 104.5l-29.9 12.5l80.4 40.5l-68.2 16.5l-52-26.6c5.7 15.2 13.4 29.4 22.7 42.3h150.2l78.5-65.2l-45.6-36l45.7-24.8l26.8 14.2V237c-30.1-21.7-67-34.5-107-34.5m-272 64c-12.8 0-23 10.2-23 23s10.2 23 23 23s23-10.2 23-23s-10.2-23-23-23m-94 11.1v18.7l60.11 16.2c-4.05-6-6.58-13-7.03-20.6zm268.4 7.3l4.2 42.1l-14.1 25.5l-15.3-51.2zM463.5 303l-15.4 43.4l-19.7-24.9zm-315.9 9.1c-4 6.1-9.7 11.1-16.3 14.3l57.9 15.6c1.4-5.9 2.9-11.7 4.7-17.4zm171.1 87.1l29.7 23.5l-18.3 25.4zm-131.4 20c-2.3.5-4.5 1-6.9 1.5c-69.9 15.5-126.2 28.2-160.9 35.9v18.5c32.9-7.4 91.7-20.5 164.8-36.8c2.3-.5 4.5-1 6.8-1.5c-1.5-5.8-2.8-11.7-3.8-17.6m175.3 9.4l42.9 15.9l-32.3 12.2z"/></svg>
    <svg id="svg-icon-distress" xmlns="http://www.w3.org/2000/svg" width="2" height="2" viewBox="0 0 24 24"><path fill="#F00" d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2m0 14H5.17L4 17.17V4h16zM11 5h2v6h-2zm0 8h2v2h-2z"/></svg>
    <svg id="svg-icon-wipe" xmlns="http://www.w3.org/2000/svg" width="2" height="2" viewBox="0 0 48 48"><g fill="none" stroke="#F00" stroke-linejoin="round" stroke-width="4"><path d="M9 10v34h30V10z"/><path stroke-linecap="round" d="M20 20v13m8-13v13M4 10h40"/><path d="m16 10l3.289-6h9.488L32 10z"/></g></svg>
    <svg id="svg-icon-poweroff" xmlns="http://www.w3.org/2000/svg" width="2" height="2" viewBox="0 0 24 24"><path fill="#FF0" d="m16.56 5.44l-1.45 1.45A5.97 5.97 0 0 1 18 12a6 6 0 0 1-6 6a6 6 0 0 1-6-6c0-2.17 1.16-4.06 2.88-5.12L7.44 5.44A7.96 7.96 0 0 0 4 12a8 8 0 0 0 8 8a8 8 0 0 0 8-8c0-2.72-1.36-5.12-3.44-6.56M13 3h-2v10h2"/></svg>

    <svg id="svg-icon-settings" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#00ff00" d="m9.25 22l-.4-3.2q-.325-.125-.612-.3t-.563-.375L4.7 19.375l-2.75-4.75l2.575-1.95Q4.5 12.5 4.5 12.338v-.675q0-.163.025-.338L1.95 9.375l2.75-4.75l2.975 1.25q.275-.2.575-.375t.6-.3l.4-3.2h5.5l.4 3.2q.325.125.613.3t.562.375l2.975-1.25l2.75 4.75l-2.575 1.95q.025.175.025.338v.674q0 .163-.05.338l2.575 1.95l-2.75 4.75l-2.95-1.25q-.275.2-.575.375t-.6.3l-.4 3.2zm2.8-6.5q1.45 0 2.475-1.025T15.55 12t-1.025-2.475T12.05 8.5q-1.475 0-2.488 1.025T8.55 12t1.013 2.475T12.05 15.5"/></svg>
    <svg id="svg-icon-timer" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 56 56"><path fill="#00FF00" d="M28 51.906c13.055 0 23.906-10.828 23.906-23.906c0-13.055-10.828-23.906-23.883-23.906c-1.242 0-1.851.75-1.851 1.968v9.094c0 1.008.68 1.828 1.71 1.828c1.032 0 1.735-.82 1.735-1.828V8.148C39.93 8.968 47.898 17.5 47.898 28A19.84 19.84 0 0 1 28 47.922c-11.063 0-19.945-8.86-19.922-19.922c.023-4.922 1.781-9.398 4.711-12.844c.726-.914.773-2.015 0-2.836c-.774-.843-2.086-.773-2.93.282C6.273 16.773 4.094 22.164 4.094 28c0 13.078 10.828 23.906 23.906 23.906m3.75-20.297c1.851-1.922 1.477-4.547-.75-6.093l-12.4-8.649c-1.171-.82-2.39.399-1.57 1.57l8.649 12.399c1.547 2.227 4.171 2.625 6.07.773"/></svg>
    <svg id="svg-icon-transmit-off" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#ff0000" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m10 14l2-2m2-2l7-7M10.718 6.713L21 3l-3.715 10.289m-1.063 2.941L14.5 21a.55.55 0 0 1-1 0L10 14l-7-3.5a.55.55 0 0 1 0-1l4.772-1.723M3 3l18 18"/></svg>
    <svg id="svg-icon-2-min" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#00ff00" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 8a4 4 0 1 1 8 0c0 1.098-.564 2.025-1.159 2.815L8 20h8"/></svg>
    <svg id="svg-icon-4-min" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#00ff00" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 20V5L7 16h10"/></svg>
    <svg id="svg-icon-10-min" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#00ff00" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 20V4L3 9m13 11a4 4 0 0 0 4-4V8a4 4 0 1 0-8 0v8a4 4 0 0 0 4 4"/></svg>
    <svg id="svg-icon-manual" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="none" stroke="#0096FF" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2 12h2m16 0h2M4 12a2 2 0 1 0 4 0a2 2 0 1 0-4 0m12 0a2 2 0 1 0 4 0a2 2 0 1 0-4 0m-8.5-1.5L15 5"/></svg>
    <svg id="svg-icon-random" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 512 512"><path fill="#FFA500" fill-rule="evenodd" d="M465.023 135.32L376.68 465.023L46.977 376.68L135.32 46.977zm-52.256 30.17L165.49 99.233L99.233 346.51l247.277 66.257zM317.08 316.538c17.07 4.574 27.201 22.121 22.627 39.192c-4.574 17.07-22.121 27.201-39.192 22.627c-17.07-4.574-27.201-22.12-22.627-39.192c4.574-17.07 22.12-27.201 39.192-22.627m-52.798-91.448c17.071 4.575 27.202 22.121 22.628 39.192s-22.121 27.202-39.192 22.628s-27.202-22.121-22.628-39.192s22.121-27.202 39.192-22.628m-52.797-91.447c17.07 4.574 27.201 22.12 22.627 39.192c-4.574 17.07-22.12 27.201-39.192 22.627c-17.07-4.574-27.201-22.12-22.627-39.192c4.574-17.07 22.121-27.201 39.192-22.627"/></svg>
    


<svg id="svg-icon-pin" class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="#00FF00" viewBox="0 0 24 24">
  <path fill-rule="evenodd" d="M5 9a7 7 0 1 1 8 6.93V21a1 1 0 1 1-2 0v-5.07A7.001 7.001 0 0 1 5 9Zm5.94-1.06A1.5 1.5 0 0 1 12 7.5a1 1 0 1 0 0-2A3.5 3.5 0 0 0 8.5 9a1 1 0 0 0 2 0c0-.398.158-.78.44-1.06Z" clip-rule="evenodd"/>
</svg>


    
    <svg id="svg-icon-toggle" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
	<path fill="#0F0" d="M7.5 2c-1.79 1.15-3 3.18-3 5.5s1.21 4.35 3.03 5.5C4.46 13 2 10.54 2 7.5A5.5 5.5 0 0 1 7.5 2m11.57 1.5l1.43 1.43L4.93 20.5L3.5 19.07zm-6.18 2.43L11.41 5L9.97 6l.42-1.7L9 3.24l1.75-.12l.58-1.65L12 3.1l1.73.03l-1.35 1.13zm-3.3 3.61l-1.16-.73l-1.12.78l.34-1.32l-1.09-.83l1.36-.09l.45-1.29l.51 1.27l1.36.03l-1.05.87zM19 13.5a5.5 5.5 0 0 1-5.5 5.5c-1.22 0-2.35-.4-3.26-1.07l7.69-7.69c.67.91 1.07 2.04 1.07 3.26m-4.4 6.58l2.77-1.15l-.24 3.35zm4.33-2.7l1.15-2.77l2.2 2.54zm1.15-4.96l-1.14-2.78l3.34.24zM9.63 18.93l2.77 1.15l-2.53 2.19z" />
    </svg>
    
</div>


</body>
</html>

