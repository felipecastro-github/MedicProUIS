<?php
//codigo para conectarse a la base de datos.
// se crea la variable conex
$conex= new mysqli('localhost','id13011033_medicpro','medicprouis','id13011033_medicpro');
if($conex){
//echo "Conexion correcta";    
}else{
echo "error en la conexión";
}
?>