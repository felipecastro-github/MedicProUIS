<?php

include("conex.php");

$sql =$conex->query("CREATE TABLE `".$_GET['Table']."`(
    Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Medicine VARCHAR(60) NOT NULL,
    Hour INT(10) NOT NULL,
    Minute INT(10) NOT NULL,
    DateStart DATE NOT NULL,
    DateFinish DATE NOT NULL,
    Quantity INT(10) NOT NULL,
    Box INT(10) NOT NULL,
    Ch TINYINT(1) NOT NULL
    )");
?>