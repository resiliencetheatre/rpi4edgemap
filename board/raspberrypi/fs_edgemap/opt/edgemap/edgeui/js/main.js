'use strict';

/* Add if needed:
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
                id   : 'about',
                title: 'About',
                icon: '#svg-icon-about'
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
                 changeLanguage('zh');
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
	const radialContextMenu = new RadialMenu(// 2nd RadialMenu with different {menuItems}
		menuItems,
		200,
		{
			multiInnerRadius: 0.2,
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
			}
	});
	document.addEventListener('contextmenu', function(event)
	{ // right-mouse(as context-menu) opened at position[x,y] of mouse-click
		event.preventDefault();
		if (radialContextMenu.isOpen())
		{
			return;
		}
		radialContextMenu.open(event.x, event.y);
	});
};
