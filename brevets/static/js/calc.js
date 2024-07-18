
var TIME_CALC_URL = SCRIPT_ROOT + "/_calc_times";

// Pass calctimes a <td> element containing the data for a control.
// It extracts the distance and calls the server to get times to
// fill in open and close times in a human-readable format.
// (If we want to also keep the ISO-formatted times, we'll need to
// stash them in hidden fields.) 
function calc_times(control) {
    console.log(`At start of calc_times()`);
    var km_val = control.find("input[name='km']").val();
    var open_time_field = control.find("input[name='open']");
    var close_time_field = control.find("input[name='close']");
    // Accessing distance, start date, and start time so we can send to server
    var distance = $("#brevet_dist_km");
    var begin_date = $("#begin_date");
    var begin_time = $("#begin_time");

    // console.log(`distance.val() = ${distance.val()}, \
    //     begin_date.val() = ${begin_date.val()}, \ 
    //     begin_time.val() = ${begin_time.val()}`); //DB 
    $.getJSON(TIME_CALC_URL, {
        km: km_val, brevet_dist: distance.val(),
        begin_date: begin_date.val(), begin_time: begin_time.val()
        },
        // response handler
        function (data) {
            var times = data.result;
            console.log("Got a response: " + JSON.stringify(times));
            console.log("Response.open = " + times.open);
            // console.log(`moment.utc(times.open) = ${moment(times.open)}`);
            // console.log(`Type of Response.open is ${typeof times.open}`);
            // If we had valid control distance and thus server returned isoformat string,
            // we check times.open since also checking times.close is redundant here
            if (typeof times.open === 'string') {
                open_time_field.val(moment.utc(times.open).format("ddd M/D H:mm"));
                close_time_field.val(moment.utc(times.close).format("ddd M/D H:mm"));
            }
            // Else if we returned an error list containing boolean and error message
            else {
                var notes = control.find(".notes");
                console.log(`Setting notes.val equal to ${times.open[1]}`);
                notes.text(times.open[1]);
            }
        }
    );
}

$(document).ready(function () {
    
    $('input[name="km"]').change(
        function (event) {
            var control_entry = $(this).parents(".control")

            var notes = control_entry.find("td.notes");
            // Erase any previous error message in Notes column 
            notes.html("&nbsp;");

            var km = parseFloat($(this).val());
            var miles = (0.621371 * km).toFixed(1);
            console.log("Converted " + km + " km to " + miles + " miles");
            var target = control_entry.find("input[name='miles']");
            target.val(miles);

            calc_times(control_entry);
        }
    );

    $('input[name="miles"]').change(
        function (event) {
            var control_entry = $(this).parents(".control")

            var notes = control_entry.find("td.notes");
            // Erase any previous error message in Notes column 
            notes.html("&nbsp;");

            var miles = parseFloat($(this).val());
            var km = (1.609344 * miles).toFixed(1);
            console.log("Converted " + miles + " miles to " + km + " kilometers");
            var target = control_entry.find("input[name='km']");
            target.val(km);

            calc_times(control_entry)
        }
    );


    // Below makes return key behave well when dealing with our html elements

    var start_options = document.querySelectorAll('.startOptions');
    var table_inputs = document.querySelectorAll('.control_time_table input');

    for (var i = 0; i < start_options.length; i++) {
        start_options[i].addEventListener('keydown', function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                var index = Array.prototype.indexOf.call(start_options, e.target);
                // For first two startOption elements, return key just moves to next one
                if (index < start_options.length - 1) {
                    start_options[index + 1].focus();
                }
                // For final startOption element (time), return moves into table
                else if (index === start_options.length - 1) {
                    table_inputs[0].focus();
                }
            }
        });
    }

    for (var i = 0; i < table_inputs.length; i++) {
        table_inputs[i].addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();  // Prevent form submission
                var index = Array.prototype.indexOf.call(table_inputs, e.target);
                // Check if index not in last row 
                if (index < table_inputs.length - 5) {
                    // Focus the input element directly below, or 5 right in the array
                    table_inputs[index + 5].focus();
                } else { 
                    // If in last row, return key focuses the submit button
                    $("#submit").focus();
                }
            }
        });
    }


    // Delay submission on press of submit button so that form AJAX fills out
    document.getElementById('submitInput').addEventListener('click',
        function (event) {
            event.preventDefault();
            console.log(`Delaying mainForm submission`); //DB
            setTimeout(function () {
                // Check that all "notes" elements are empty, i.e. no errors
                var allEmpty = 
                Array.from(document.querySelectorAll('td[name="notes"]')).every(function(td) {
                    return td.textContent.trim() === '';
                });
                if(allEmpty) {
                    console.log(`Notes all empty; submitting form`);
                    document.getElementById('errorArea').innerHTML = "";
                    document.getElementById('mainForm').submit();
                } else {
                    console.log(`At least one note is non-empty; form not submitted`); 
                    document.getElementById('errorArea').innerHTML = 
                        "Submit unsuccessful: there is at least one error in the table.";
                }
            }, 250);
        }
    );

    

});