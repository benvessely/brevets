<html>
    <head>
        <title>Brevet Control Times</title>
    </head>

    <body>
        
        <h1>Brevet Times</h1>
        
        <h3>All Brevet Times:</h3> 
        <ul> 
            <?php
            $json = file_get_contents('http://brevets-and-api:5000/listAll');
            // echo "DEBUG: $json"; //DB 
            $obj = json_decode($json);
            $times = $obj->times;
            $checkpoint = 1;
            foreach ($times as $control_time) {
                $open_time = $control_time->open;
                $close_time = $control_time->close;
                echo "<li>For checkpoint $checkpoint, Open: $open_time, Close: $close_time</li>";
                $checkpoint++; 
            }
            ?>
        </ul> 

        <h3>First k Open Times with k=2:</h3> 
        <ul> 
            <?php
            $json = file_get_contents('http://brevets-and-api:5000/listOpenOnly?top=2');
            // echo "DEBUG: $json"; //DB 
            $obj = json_decode($json);
            $times = $obj->times;
            $checkpoint = 1;
            foreach ($times as $control_time) {
                $open_time = $control_time->open;
                echo "<li>For checkpoint $checkpoint, Open: $open_time</li>";
                $checkpoint++; 
            }
            ?>
        </ul> 

        <h3>First k Close Times with k=2:</h3> 
        <ul> 
            <?php
            $json = file_get_contents('http://brevets-and-api:5000/listCloseOnly?top=2');
            // echo "DEBUG: $json"; //DB 
            $obj = json_decode($json);
            $times = $obj->times;
            $checkpoint = 1;
            foreach ($times as $control_time) {
                $close_time = $control_time->close;
                echo "<li>For checkpoint $checkpoint, Close: $close_time</li>";
                $checkpoint++; 
            }
            ?>
        </ul> 
        

        <h3>All Brevet Times in CSV format:</h3> 
        <ul> 
            <?php
            $csv = file_get_contents('http://brevets-and-api:5000/listAll/csv');
            // Check if $csv is empty (has length 5 in this case)
            if (strlen($csv) == 5) {
                echo ""; 
            } else {
                // echo "\$csv = $csv"; //DB 
                $split_csv = explode('\n', $csv);
                // print_r($split_csv); //DB
                $split_csv[0] = substr($split_csv[0], 1);
                $split_csv[1] = substr($split_csv[1], 0, -2);
                foreach ($split_csv as $element) {
                    echo "$element<br>"; 
                }
            }
            ?>
        </ul> 


        <h3>First k Open Times in CSV format with k=2:</h3> 
        <ul> 
            <?php
            $csv = file_get_contents('http://brevets-and-api:5000/listOpenOnly/csv?top=2');
            // $length = strlen($csv); //DB 
            // echo "DEBUG: strlen($csv) = $length <br>"; //DB 

            // Check if $csv is empty (has length 5 in this case)
            if (strlen($csv) == 5) {
                echo ""; 
            } else { 
                $split_csv = explode('\n', $csv);
                // print_r($split_csv); //DB
                $split_csv[0] = substr($split_csv[0], 1);
                $split_csv[1] = substr($split_csv[1], 0, -2);
                foreach ($split_csv as $element) {
                    echo "$element<br>"; 
                }
            }
            ?>
        </ul> 

        <h3>First k Close Times in CSV format with k=2:</h3> 
        <ul> 
            <?php
            $csv = file_get_contents('http://brevets-and-api:5000/listCloseOnly/csv?top=2');
            // echo "DEBUG: $csv<br>"; //DB 

            // Check if $csv is empty (has length 5 in this case)
            if (strlen($csv) == 5) {
                echo ""; 
            } else { 
                $split_csv = explode('\n', $csv);
                // print_r($split_csv); //DB
                $split_csv[0] = substr($split_csv[0], 1);
                $split_csv[1] = substr($split_csv[1], 0, -2);
                foreach ($split_csv as $element) {
                    echo "$element<br>"; 
                }
            }
            ?>
        </ul> 

    
    </body>
</html>