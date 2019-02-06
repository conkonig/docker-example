<?php

$uri_parts = explode('?', $_SERVER['REQUEST_URI'], 2);
$currentURL = 'http://' . $_SERVER['HTTP_HOST'] . $uri_parts[0];
$pickupIndex = $_GET['pickup'];

$pickups = file_get_contents('http://api-service/pickup');
$obj = json_decode($pickups);
$pickups = $obj->pickups;

if($pickupIndex){
    $chosenOne = file_get_contents('http://api-service/pickup/'.$pickupIndex);
}

?>
<ul>
    <select name="pickup" onchange="document.location.href=this.options[this.selectedIndex].value;">
        <option value label="Get index from API">Get pickup line from API</option>
        <?php
            for ($i = 0; $i < sizeof($pickups); $i++) {
                echo "<option value='$currentURL?pickup=$i'>$i</option>";
            }
        ?>
    </select>
</ul>
<h1><?php echo $chosenOne ?></h1>