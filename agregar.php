<?php

include("conex.php");
$sql = $conex->query("INSERT INTO `".$_GET['user']."` values(0, '".$_GET['Medicine']."', '".$_GET['Hour']."', '".$_GET['Minute']."', '".$_GET['DateStart']."', '".$_GET['DateFinish']."', '".$_GET['Quantity']."', '".$_GET['Box']."', '".$_GET['Ch']."')");

if($conex->connect_errno){
    die('Error al conectar');
}
else{
    echo($_GET['user']);

}
$conex->close();
?>