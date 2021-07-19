<?php
function wind_cardinals($degrees) {
  $directions = array('N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N');
  return $directions[round($degrees / 22.5)];
}





?>
