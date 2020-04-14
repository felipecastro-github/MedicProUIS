<!--
Script to read data fron MySQL database
Author:Felipe Castro
Company:UIS
Signature:Diseño con microprosesadores y microcontroladores
Project:Dispensador de medicamentos
-->
<html>
    <head>
        <title>LeerBase</title>
    </head>
    <body>
        <?php
        $info = $_GET['info'];
        $User=$_GET['User'];
        $ob = new mysqli('localhost','id13011033_medicpro','medicprouis','id13011033_medicpro');
        if($ob->connect_errno){
            echo('Error al conectar');
        }else{
            $timezone = new DateTimeZone("America/Bogota"); 
            $dateNow = new DateTime("now", $timezone);
            $dateNow=$dateNow->format('Y-m-d H:i');
            $dateNow = date_create($dateNow);
            $va=[];
            $Data=$ob->query("SELECT * FROM `US_".$User."`");
            while ($imp=mysqli_fetch_array($Data,MYSQLI_NUM)){
            if($imp[8]){
                $dateStart = date_create(''.$imp[4].' '.$imp[2].':'.$imp[3].'');
                $dateFinish = date_create(''.$imp[5].' '.$imp[2].':'.$imp[3].'');
                $intervalStart = date_diff($dateNow,$dateStart);
                $intervalFinish = date_diff($dateNow,$dateFinish);
                $diffDaysFinish = (float)$intervalFinish->format('%R%a');
                $diffHoursFinish= (float)$intervalFinish->format('%R%H');
                $diffDaysStart = (float)$intervalStart->format('%R%a');
                $diffHoursStart= (float)$intervalStart->format('%R%H');
                if($diffDaysFinish<=0&$diffHoursFinish<=-2){
                    $ob->query("UPDATE `US_".$User."` SET `Ch` = '0' WHERE `US_".$User."`.`Id` = ".$imp[0]."");
                }
                if($diffDaysStart<=0&$diffHoursStart<=5){
                    array_push($va,''.$imp[0].','.$imp[1].','.$imp[2].','.$imp[3].','.$imp[6].','.$imp[7].','.$imp[8].'');
                }
            }
            }
            $toSend=implode('\r',$va);
            if($info==$toSend){
                echo '~+noData~+';
            }else{
                echo '~+'.$toSend.'~+';
            }
        }
        ?>
    </body>
</html>