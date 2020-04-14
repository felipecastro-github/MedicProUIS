<?php

include("conex.php");

$sql = $conex->query("SELECT * FROM `users` WHERE `Email` =".$_GET['Email']." AND `Password` =".$_GET['Password']."");

if($conex->connect_errno){
    die('Error al conectar');
}
else{
    echo "login,";
    $fila = mysqli_fetch_array($sql);
    echo($fila['Id']);
    echo ",";
    echo($fila['Name']);
    echo ",";
    echo($fila['Last Name']);
}


$sql->free();
$conex->close();
?>