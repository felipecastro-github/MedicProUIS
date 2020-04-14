<?php

include("conex.php");
$user = $_GET['user'];
$sql = $conex->query("SELECT * FROM `".$user."`");
$rows = $sql->num_rows;

    
if($conex->connect_errno){
    die('Error al conectar');
}
else{
    while($fila = mysqli_fetch_array($sql)){
    echo($fila['Quantity']);
    echo ",";
    echo($fila['Medicine']);
    echo ",";
    echo($fila['Hour']);
    echo ",";
    echo($fila['Minute']);
    echo ",";
    }
    
    
}
$sql->free();
$conex->close();
?>