
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
  /* 
  console.log(`distance.val() = ${distance.val()}, \
      begin_date.val() = ${begin_date.val()}, \ 
      begin_time.val() = ${begin_time.val()}`); //DB 
  */ 
  $.getJSON(TIME_CALC_URL, { km: km_val , brevet_dist: distance.val() , 
       begin_date: begin_date.val(), begin_time: begin_time.val() }, 
     // response handler
     function(data) {
       var times = data.result;
       console.log("Got a response: " +  JSON.stringify(times));
       console.log("Response.open = " + times.open);
       // console.log(`moment.utc(times.open) = ${moment(times.open)}`);
       console.log(`Type of Response.open is ${typeof times.open}`);
       // If we had valid control distance and thus server returned isoformat string
       // We check times.open since also checking times.close is redundant here
       if (typeof times.open === 'string') {  
         open_time_field.val( moment.utc(times.open).format("ddd M/D H:mm"));
         close_time_field.val( moment.utc(times.close).format("ddd M/D H:mm"));
       } 
       // If we returned an error list containing boolean and error message
       else { 
         var notes = control.find(".notes");
         console.log(`Setting notes.val equal to ${times.open[1]}`);
         notes.text(times.open[1]);
       } 
     } // end of handler function
);// End of getJSON
  }
  
$(document).ready(function(){
 // Do the following when the page is finished loading

    $('input[name="miles"]').change(
       function() {
           var miles = parseFloat($(this).val());
           var km = (1.609344 * miles).toFixed(1) ;
           console.log("Converted " + miles + " miles to " + km + " kilometers");
           var control_entry = $(this).parents(".control")
           var target = control_entry.find("input[name='km']");
           target.val( km );
           // Then calculate times for this entry
           calc_times(control_entry);
        });

    $('input[name="km"]').change(
       function() {
           var km = parseFloat($(this).val());
           var miles = (0.621371 * km).toFixed(1) ;
           console.log("Converted " + km + " km to " + miles + " miles");
           var control_entry = $(this).parents(".control")
           var target = control_entry.find("input[name='miles']");
           target.val( miles );
           // Then calculate times for this entry
           calc_times(control_entry);
        });

   });   // end of what we do on document ready


window.addEventListener('DOMContentLoaded', (event) => {
    // Get all input elements inside the table
    var inputs = document.querySelectorAll('.control_time_table input');
    for(var i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();  // Prevent form submission
                var index = Array.prototype.indexOf.call(inputs, e.target);
                // Check if index not in last row 
                if (index < inputs.length - 5) {        
                    // Focus the input element directly below, or 5 right in the array
                    inputs[index + 5].focus(); 
                } else { // If in last row, return key just moves focus one to right
                    $("#submit").focus(); 
                }
            }
        });
    }
});





