<?php

include("conex.php");
$user = $_GET['user'];
$sql = $conex->query("DELETE FROM `".$user."` WHERE `".$user."`.`Medicine` = ".$_GET['Medicine']."");

if($conex->connect_errno){
    die('Error al conectar');
}
else{
    echo "Delete ok";
}

$conex->close();
?>