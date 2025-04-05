'use strict';
/* 
 * radialmenus - note that edgemap_ng.js needs to be loaded first
 * 
 * Add if needed:
 * 
    {
        id   : 'distress',
        title: 'Distress',
        icon: '#svg-icon-distress'
    },
  
*/
var menuItems = [
    {
        id   : 'setlocation',
        title: 'Set location',
        icon: '#svg-icon-my-location'
    },
    {
        id   : 'terrain',
        title: 'Terrain',
        icon: '#svg-icon-terrain'
    },
    {
        id   : 'sendimage',
        title: 'Image',
        icon: '#svg-icon-camera'
    },
    {
        id   : 'meshtasticnodes',
        title: 'Meshtastic',
        icon: '#svg-icon-meshtastic'
    },
    {
        id   : 'symbols',
        title: 'Show',
        icon: '#svg-icon-pin'
    },
    {
        id   : 'more',
        title: 'More...',
        icon: '#svg-icon-more',
        items: [
            {
                id   : 'language',
                title: 'Language',
                icon: '#svg-icon-language',
                    items: [
                    {
                        id   : 'language-en',
                        title: 'English',
                        icon: '#svg-icon-language-en'
                    },
                    {
                        id   : 'language-zh',
                        title: 'Chinese',
                        icon: '#svg-icon-language-zh'
                    },
                    {
                        id   : 'language-ukr',
                        title: 'Ukrainian',
                        icon: '#svg-icon-language-ukr'
                    },
                    {
                        id   : 'language-ar',
                        title: 'Arabic',
                        icon: '#svg-icon-language-ar'
                    },
                    {
                        id   : 'language-de',
                        title: 'German',
                        icon: '#svg-icon-language-de'
                    },
                    {
                        id   : 'language-es',
                        title: 'Spanish',
                        icon: '#svg-icon-language-es'
                    },
                    {
                        id   : 'language-fr',
                        title: 'French',
                        icon: '#svg-icon-language-fr'
                    },
                    {
                        id   : 'language-ru',
                        title: 'Russian',
                        icon: '#svg-icon-language-ru'
                    },
                    {
                        id   : 'language-he',
                        title: 'Hebrew',
                        icon: '#svg-icon-language-he'
                    }
                    
                ]
            },
            {
                id   : 'timer',
                title: 'Pos report',
                icon: '#svg-icon-timer',
                
                items: [
                    {
                        id   : 'pos_off',
                        title: 'Reports Off',
                        icon: '#svg-icon-transmit-off',
                    },
                    {
                        id   : 'pos_2',
                        title: 'minutes',
                        icon: '#svg-icon-2-min',
                    },
                    {
                        id   : 'pos_4',
                        title: 'minutes',
                        icon: '#svg-icon-4-min',
                    },
                    {
                        id   : 'pos_10',
                        title: 'minutes',
                        icon: '#svg-icon-10-min',
                    },
                    {
                        id   : 'pos_manual',
                        title: 'Manual',
                        icon: '#svg-icon-manual',
                    },
                    {
                        id   : 'pos_random',
                        title: 'Random',
                        icon: '#svg-icon-random',
                    }
                ]
            },
            {
                id   : 'coordinate',
                title: 'Coordinates',
                icon: '#svg-icon-coordinate-search'
            },
            {
                id   : 'measure',
                title: 'Distance',
                icon: '#svg-icon-measure'
            },
            {
                id   : 'style',
                title: 'Style',
                icon: '#svg-icon-toggle'
            },
            {
                id   : 'editsymbols',
                title: 'Edit symbols',
                icon: '#svg-icon-pin'
            },
            {
                id   : 'poweroff',
                title: 'Power off',
                icon: '#svg-icon-poweroff'
            },      
        ]
    },
    {
        id: 'message',
        title: 'Message',
        icon: '#svg-icon-message',
        
    }
];

//
// Right click menu
//
// Call generateRightMenuSymbols(); so that SVG's are available
// 
var rightClickmenuItems = [
    {
        id   : 'setlocation',
        title: 'Set location',
        icon: '#svg-icon-my-location'
    },
    {
        id   : 'sendimage',
        title: 'Send image',
        icon: '#svg-icon-camera'
    },
    {
        id: 'symbol0',
        title: menuSymbolText[0],
        icon: '#milSymbol_0'
    },
    {
        id: 'symbol1',
        title: menuSymbolText[1],
        icon: '#milSymbol_1'
    },
    {
        id: 'symbol2',
        title: menuSymbolText[2],
        icon: '#milSymbol_2'
    },
    {
        id: 'symbol3',
        title: menuSymbolText[3],
        icon: '#milSymbol_3'
    }
];

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
window.onload = function ()
{
	const radialMenu = new RadialMenu(menuItems, 250, {
        ui: {
				classes: {
					menuOpen: "open",
					menuClose: "close"
				}
        },
		parent: document.body,
		closeOnClick: true,
		closeOnClickOutside: true,
		onClick: function(item)
		{
			// console.log('You have clicked:', item.id, item.title);
			// console.log(item);
            
            if ( item.id == "setlocation" ) {
                 setManualLocationNotifyMessage();
            }
            if ( item.id == "terrain" ) {
                 toggleHillShadow();
            }
            if ( item.id == "language" ) {
                 openLanguageSelectBox();
            }
            if ( item.id == "coordinate" ) {
                 openCoordinateSearchEntryBox();
            }
            if ( item.id == "symbols" ) {
                 loadLocalSymbols();
            }
            if ( item.id == "message" ) {
                 openMessageEntryBox();
            }
            if ( item.id == "meshtasticnodes" ) {
                 toggleRadioList();
            }
            if ( item.id == "sendimage" ) {
                 clickSendImageForm();
            }
            
            if ( item.id == "language-en" ) {
                 changeLanguage('en');
            }
            if ( item.id == "language-zh" ) {
                 changeLanguage('zh-Hans');
            }
            if ( item.id == "language-ukr" ) {
                 changeLanguage('uk');
            }
            if ( item.id == "language-ar" ) {
                 changeLanguage('ar');
            }
            if ( item.id == "language-de" ) {
                 changeLanguage('de');
            }
            if ( item.id == "language-es" ) {
                 changeLanguage('es');
            }
            if ( item.id == "language-fr" ) {
                 changeLanguage('fr');
            }
            if ( item.id == "language-ru" ) {
                 changeLanguage('ru');
            }
            if ( item.id == "language-he" ) {
                 changeLanguage('he');
            } 
            
            if ( item.id == "wipe" ) {
                engine("wipe");
            }
            if ( item.id == "distress" ) {
                engine("distress");
            }
            if ( item.id == "poweroff" ) {
                engine("poweroff"); // nextgen
            }
            if ( item.id == "pos_off" ) {
                engine("pos_off");
            }
            if ( item.id == "pos_2" ) {
                engine("pos_2");
            }
            if ( item.id == "pos_4" ) {
                engine("pos_4");
            }
            if ( item.id == "pos_10" ) {
                engine("pos_10");
            }
            if ( item.id == "pos_manual" ) {
                engine("pos_manual");
            }
            if ( item.id == "pos_random" ) {
                engine("pos_random");
            }
            if ( item.id == "style" ) {
                toggleStyle();
            }
            if ( item.id == "editsymbols" ) {
                const relativePath = "symbolseditor/"; 
                window.location.href = relativePath;
            }
            if ( item.id == "measure" ) {
                distanceControlOpenButton();
            }
		}
	});
    
	document.getElementById('topRightMenuButton').addEventListener('click', function(event)
	{
		radialMenu.open();
	});
    
	/*document.getElementById('closeMenu').addEventListener('click', function(event)
	{
		radialMenu.close();
	});*/
    
    //
    // Right click menu functions
    // 
	const rightClickMenu = new RadialMenu(
		rightClickmenuItems,
        250,
		{
			ui: {
				classes: {
					menuContainer: "menuHolder2",
					menuCreate: "menu2",
					menuCreateParent: "inner2",
					menuCreateNested: "outer2",
					menuOpen: "open2",
					menuClose: "close2"
				},
				nested: {
					title: false
				}
			},
            closeOnClick: true,
            closeOnClickOutside: true,
            onClick: function(item)
            {
                if ( item.id == "setlocation" ) {
                     lat = document.getElementById('rightMenuLat').innerHTML;
                     lon = document.getElementById('rightMenuLon').innerHTML;
                     manualLocationSetFromRightMenu(lat,lon);
                     document.getElementById('rightMenuLat').innerHTML = "";
                     document.getElementById('rightMenuLon').innerHTML = "";
                }
                if ( item.id == "sendimage" ) {
                    // Take location clicked 
                    lat = document.getElementById('rightMenuLat').innerHTML;
                    lon = document.getElementById('rightMenuLon').innerHTML;
                    // Populate upload form with latitude, longitude
                    const formInfo = document.forms['uploadform'];
                    formInfo.lat.value = lat;
                    formInfo.lon.value = lon;
                    // Upload image
                    clickSendImageForm();
                    // Clear used location
                    document.getElementById('rightMenuLat').innerHTML = "";
                    document.getElementById('rightMenuLon').innerHTML = "";
                }
                if ( item.id == "symbol0" ) {
                    lat = document.getElementById('rightMenuLat').innerHTML;
                    lon = document.getElementById('rightMenuLon').innerHTML;
                    addRightClickSymbol(lat,lon,0);
                }
                if ( item.id == "symbol1" ) {
                    lat = document.getElementById('rightMenuLat').innerHTML;
                    lon = document.getElementById('rightMenuLon').innerHTML;
                    addRightClickSymbol(lat,lon,1);
                }
                if ( item.id == "symbol2" ) {
                    lat = document.getElementById('rightMenuLat').innerHTML;
                    lon = document.getElementById('rightMenuLon').innerHTML;
                    addRightClickSymbol(lat,lon,2);
                }
                if ( item.id == "symbol3" ) {
                    lat = document.getElementById('rightMenuLat').innerHTML;
                    lon = document.getElementById('rightMenuLon').innerHTML;
                    addRightClickSymbol(lat,lon,3);
                }
            }
	});
    
    /*
     * "The contextmenu event fires when the user attempts to open a context menu. 
     * This event is typically triggered by clicking the right mouse button, 
     * or by pressing the context menu key."
     */
    
    //
    // Right click event on desktop browsers
    //
	document.addEventListener('contextmenu', function(event)
	{ 
        // Get the map container
        const mapContainer = document.getElementById('map');
        if (!mapContainer) {
            console.error("Map container not found");
            return;
        }
        // Get the bounding rect of the map container
        const rect = mapContainer.getBoundingClientRect();
        // Convert screen coordinates to map-relative coordinates
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        // Convert to latitude and longitude
        const lngLat = map.unproject([x, y]);
        document.getElementById('rightMenuLat').innerHTML = lngLat.lat;
        document.getElementById('rightMenuLon').innerHTML = lngLat.lng;
        // event.preventDefault();
		if (rightClickMenu.isOpen())
		{
			return;
		}
		rightClickMenu.open(event.x, event.y);
	});
    
    //
    // Long touch as right click on mobile browsers
    //
    // We have timerArray because desktop firefox intializes multiple
    // timers on touchstart event. So what ever we start, we clear
    // all of them with clearTimer().
    //
    let timer;
    let timerArray = [];
    function clearTimer() {
        timerArray.forEach(clearTimerEntry);
    }
    function clearTimerEntry(timerToClear) {
        clearTimeout(timerToClear);
    }
    
    const targetElement = document.getElementById("map");
    
    targetElement.addEventListener("touchstart", function (event) {
        timer = setTimeout(() => {
            // console.log("rightClickMenu.open() ", timer );
            rightClickMenu.open(event.touches[0].clientX, event.touches[0].clientY);
            // Get the map container
            const mapContainer = document.getElementById('map');
            if (!mapContainer) {
                console.error("Map container not found");
                return;
            }
            // Get the bounding rect of the map container
            const rect = mapContainer.getBoundingClientRect();
            // Convert screen coordinates to map-relative coordinates
            const x = event.touches[0].clientX - rect.left;
            const y = event.touches[0].clientY - rect.top;
            // Convert to latitude and longitude
            const lngLat = map.unproject([x, y]);
            // Equip html elements
            document.getElementById('rightMenuLat').innerHTML = lngLat.lat;
            document.getElementById('rightMenuLon').innerHTML = lngLat.lng;
        }, 800); 
        // console.log(" timer = setTimeout(()) ", timer);
        timerArray.push(timer);
    });
    
    // Clear timer events
    targetElement.addEventListener("touchend", clearTimer );
    targetElement.addEventListener("touchmove", clearTimer, { passive: false });
    targetElement.addEventListener("gesturestart", clearTimer);
    targetElement.addEventListener("gesturechange", clearTimer);
    targetElement.addEventListener("gestureend", clearTimer);
    targetElement.addEventListener("touchstart", function (event) {
        if (event.touches.length > 1) {
            clearTimer();
        }
    });
    targetElement.addEventListener("touchmove", function (event) {
        if (event.touches.length > 1) {
            clearTimer();
        }
    });
    targetElement.addEventListener("pointercancel", clearTimer);
    
    
    
};
