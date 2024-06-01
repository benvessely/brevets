<html>
    <head>
        <title>Brevet Control Times</title>
    </head>

    <body>
        
        <h1>List All</h1>
        <ul> 
            <?php
            $curl_handle=curl_init();
            curl_setopt($curl_handle, CURLOPT_URL, 'http://brevets-and-api:5000/listAll/');
            curl_setopt($curl_handle, CURLOPT_CONNECTTIMEOUT, 2);
            curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, 1);
            curl_setopt($curl_handle, CURLOPT_USERAGENT, 'Your application name');
            $json = curl_exec($curl_handle);
            if ($json === false) {
                echo 'cURL error: ' . curl_error($curl_handle);
            } else {
                // echo $json;
                $obj = json_decode($json);
                // rest of your code
                curl_close($curl_handle);
              g  print_r($obj);
                //     $times = $obj->times;
                // foreach ($times as $control_time) {
                //     echo "<li>$control_time</li>";
                // }
            }
            ?>
        </ul> 
    
    </body>
</html>