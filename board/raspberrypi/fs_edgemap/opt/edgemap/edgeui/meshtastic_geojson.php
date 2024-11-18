<?php
/*
 * Sample geojson fetch from sqlite db
 * 
 * 
 * 
 */

// TODO: More sanity check of invalid or empty data !
$db_file="/tmp/radio.db";
// Check if sqlite3 DB is available
if ( file_exists($db_file) && is_readable($db_file) ) {
} else {
    exit;
}

$db = new SQLite3($db_file);
// linkline between nodes (0/1)
$LINK_LINE = $_GET['linkline'];
$MY_CALLSIGN = $_GET['myCallSign'];

// Color code
function getSignalColor($dBm) {
    // Define thresholds and colors
    // $thresholds = [-100, -70, -50, -30];
    $thresholds = [-100, -50, -30, -20];
    $colors = [
        ['r' => 255, 'g' => 0, 'b' => 0],    // Red (poor signal)
        ['r' => 255, 'g' => 255, 'b' => 0],  // Yellow (medium signal)
        ['r' => 0, 'g' => 255, 'b' => 0],    // Green (good signal)
    ];

    // Clamp dBm to be within the thresholds
    if ($dBm <= $thresholds[0]) {
        return sprintf("rgb(%d, %d, %d)", $colors[0]['r'], $colors[0]['g'], $colors[0]['b']);
    }
    if ($dBm >= $thresholds[3]) {
        return sprintf("rgb(%d, %d, %d)", $colors[2]['r'], $colors[2]['g'], $colors[2]['b']);
    }

    // Find which threshold range the dBm value falls into
    for ($i = 0; $i < count($thresholds) - 1; $i++) {
        if ($dBm >= $thresholds[$i] && $dBm < $thresholds[$i + 1]) {
            $ratio = ($dBm - $thresholds[$i]) / ($thresholds[$i + 1] - $thresholds[$i]);
            $r = round($colors[$i]['r'] + $ratio * ($colors[$i + 1]['r'] - $colors[$i]['r']));
            $g = round($colors[$i]['g'] + $ratio * ($colors[$i + 1]['g'] - $colors[$i]['g']));
            $b = round($colors[$i]['b'] + $ratio * ($colors[$i + 1]['b'] - $colors[$i]['b']));
            return sprintf("rgb(%d, %d, %d)", $r, $g, $b);
        }
    }

    // Fallback color (should never reach here)
    return "rgb(0, 0, 0)";
}

//
// Query NAME's first
//
$res = $db->query('SELECT DISTINCT callsign FROM meshradio order by ID DESC');
$x=1;
while ($row = $res->fetchArray()) {
	// echo "{$row['id']} {$row['callsign']} {$row['time']} {$row['lat']} {$row['lon']} \n";
	if ( $row['callsign'] != "" ) {
            $NAME[$x] = "{$row['callsign']}";
            $x++;
	}
}  

//
// Count of items in DB
//
$ITEM_COUNT = $x-1;

// 
// Query each target: name, time, lat and lon (latest position)
// 
for ($loop = 1; $loop < $x; $loop++)  {
	$db = new SQLite3($db_file);
	$res = $db->query('SELECT * FROM meshradio WHERE callsign like "'.$NAME[$loop].'" order by ID DESC LIMIT 1 ');
	while ($row = $res->fetchArray()) {
		if ( $row['callsign'] != "" && $row['lat'] != "" && $row['lon'] != "" && strcmp( $MY_CALLSIGN , $ITEM_NAME[$display_loop] ) != -1 ) {
			$ITEM_NAME[$loop] = "{$row['callsign']}";
			$ITEM_TIME[$loop] = "{$row['time']}";
			$ITEM_LAT[$loop] = "{$row['lat']}";
			$ITEM_LON[$loop] = "{$row['lon']}";
            $ITEM_SNR[$loop] = "{$row['snr']}";
            $ITEM_RSSI[$loop] = "{$row['rssi']}";
		}
	} 
}

// 
// Query my location
// 
$db = new SQLite3($db_file);
$res = $db->query('SELECT * FROM meshradio WHERE callsign like "'.$MY_CALLSIGN.'%" order by ID DESC LIMIT 1 ');
while ($row = $res->fetchArray()) {
    if ( $row['callsign'] != "" && $row['lat'] != "" && $row['lon'] != "" ) {
        $MY_CALLSIGN_LAT = "{$row['lat']}";
        $MY_CALLSIGN_LON = "{$row['lon']}";
    }
} 

// Output feature collection
echo '
{ "type": "FeatureCollection", 
  "features": [';
  
  
for ($loop = 1; $loop <= $ITEM_COUNT; $loop++)
{
    $LON = $ITEM_LON[$loop];
    $LAT = $ITEM_LAT[$loop];
    $LON_2 = $MY_CALLSIGN_LON;
    $LAT_2 = $MY_CALLSIGN_LAT;
    
    // $LINE_TEXT = $ITEM_NAME[$from] ."->".$ITEM_NAME[$to].": ".$ITEM_SNR[$to] ." (". $ITEM_RSSI[$to].")";
    // $LINE_TEXT = $ITEM_NAME[$from] ." (".$ITEM_RSSI[$from]." dBm)" ." to ".$ITEM_NAME[$to]." (".$ITEM_RSSI[$to]." dBm)";
    // $LINE_TEXT = "".$ITEM_RSSI[$to]." dBm";
                        
    $LINE_COLOR = "#6F6";
    $LINE_WIDTH = 16;
    $LINE_TEXT = $ITEM_RSSI[$loop]." dBm";
    $LINE_COLOR = getSignalColor($ITEM_RSSI[$loop]); // "#6F6";
    
    echo '{ "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": [ ['.$LON .','.$LAT.'],['.$LON_2 .','.$LAT_2.'] ]},
        "properties": { "color": "'.$LINE_COLOR.'", "width": '.$LINE_WIDTH.', "opacity": 0.8, "title": "'.$LINE_TEXT.'", "text-color": "#000","text-size": 16,"text-halo-color": "#fff","text-halo-width": 3,"text-halo-blur": 2 }
        }';
        
    if ( $loop < $ITEM_COUNT ) {
        echo ",";
    }
}
echo "]
	  }";
 
      
?>
