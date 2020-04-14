<?php

include("conex.php");

$sql = $conex->query("INSERT INTO `users` values(0, '".$_GET['Name']."', '".$_GET['Last']."', '".$_GET['Email']."', '".$_GET['Password']."')");

if($conex->connect_errno){
    die('Error al conectar');
}
else{

}
$conex->close();
?>