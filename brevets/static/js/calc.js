/* global $, moment */
;
const TIME_CALC_URL = SCRIPT_ROOT + "/_calc_times";

const convertKmToMiles = (km) => (0.621371 * parseFloat(km)).toFixed(1);
const convertMilesToKm = (miles) => (1.609344 * parseFloat(miles)).toFixed(1);

const selectors = {
    getBrevetDist: () => $("#brevet_dist_km"),
    getBeginDate: () => $("#begin_date"),
    getBeginTime: () => $("#begin_time"),
    getErrorArea: () => document.getElementById('errorArea'),
    getAllNotes: () => document.querySelectorAll('td[name="notes"]'),
    getTableInputs: () => document.querySelectorAll('.control_time_table input')
};

// Time calculation functions
const calculateTimes = (control) => {
    const kmVal = control.find("input[name='km']").val();
    const openTimeField = control.find("input[name='open']");
    const closeTimeField = control.find("input[name='close']");
    
    const kmValFloat = parseFloat(kmVal);
    
    // When the empty string is converted using parseFloat, it shows up as NaN
    if (isNaN(kmValFloat)) {
        openTimeField.val("");
        closeTimeField.val("");
        return;
    }

    const requestData = {
        km: kmVal,
        brevet_dist: selectors.getBrevetDist().val(),
        begin_date: selectors.getBeginDate().val(),
        begin_time: selectors.getBeginTime().val()
    };

    $.getJSON(TIME_CALC_URL, requestData, (data) => {
        const times = data.result;
        
        // If we had valid control distance and thus server returned isoformat string,
        // we check times.open since also checking times.close is redundant here
        if (typeof times.open === 'string') {
            openTimeField.val(moment.utc(times.open).format("ddd M/D H:mm"));
            closeTimeField.val(moment.utc(times.close).format("ddd M/D H:mm"));
        } 
        // Else if we returned an error list containing boolean and error message
        else { 
            const notes = control.find(".notes");
            notes.text(times.open[1]);
        }
    });
};

const handleDistanceChange = (event, unit) => {
    const control = $(event.target).parents(".control");
    const notes = control.find("td.notes");
    // Erase any previous error message in Notes column 
    notes.html("&nbsp;");

    const value = parseFloat($(event.target).val());
    const targetField = control.find(`input[name='${unit === 'km' ? 'miles' : 'km'}']`);
    
    if (unit === 'km') {
        targetField.val(convertKmToMiles(value));
    } else {
        targetField.val(convertMilesToKm(value));
    }

    calculateTimes(control);
};

const isTableEmpty = () => {
    const inputs = document.querySelectorAll('.control_time_table input');
        
    for (const input of inputs) {
        if (input.type === 'number') {
            if (input.value !== '') {
                return false;
            }
        }
        else if (input.type === 'datetime') {
            if (input.value !== '') {
                return false;
            }
        }
        else if (input.type === 'text') {
            if (input.value.trim() !== '') {
                return false;
            }
        }
    }
    
    return true;
  
};

const areNotesEmpty = () => {
    return Array.from(selectors.getAllNotes())
        .every(td => td.textContent.trim() === '');
};

const setupDistanceConverters = () => {
    $('input[name="km"]').change(e => handleDistanceChange(e, 'km'));
    $('input[name="miles"]').change(e => handleDistanceChange(e, 'miles'));
};

const setupKeyboardNavigation = () => {
    const startOptions = document.querySelectorAll('.startOptions');
    const tableInputs = selectors.getTableInputs();

    startOptions.forEach((option, index) => {
        option.addEventListener('keydown', (e) => {
            if (e.key === "Enter") {
                e.preventDefault();
                // For first two startOption elements, return key just moves to next one
                if (index < startOptions.length - 1) {
                    startOptions[index + 1].focus();
                } 
                // For final startOption element (time), return moves into table
                else {
                    tableInputs[0].focus();
                }
            }
        });
    });

    tableInputs.forEach((input, index) => {
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                // Check if index not in last row 
                if (index < tableInputs.length - 5) {
                    // Focus the input element directly below, i.e. 5 right in the array
                    tableInputs[index + 5].focus();
                } else {
                    // If in last row, return key focuses the submit button
                    $("#submit").focus();
                }
            }
        });
    });  
       
};

const setupFormButtons = () => {
    document.getElementById('submitInput').addEventListener('click', (event) => {
        event.preventDefault();
        const errorArea = selectors.getErrorArea();
        
        new Promise(function(resolve) {
            if ($.active === 0) {
                resolve(); 
            } else { 
                $(document).one('ajaxStop', resolve);    
            }
        })
        .then(() => {
            if (areNotesEmpty()) {
                errorArea.innerHTML = "";
                document.getElementById('mainForm').submit();
            } else {
                errorArea.innerHTML = "Submit unsuccessful: there is at least one error in the table.";
            }
        })
        .catch(error => {
            errorArea.innerHTML = "An error occurred while submitting the form.";
            console.error('Form submission error:', error);
        });
    });

    document.getElementById('clearInput').addEventListener('click', () => {
        document.getElementById('brevet_dist_km').selectedIndex = 0;
        document.getElementById('begin_date').value = '2017-01-01';
        document.getElementById('begin_time').value = '00:00';
        
        document.querySelectorAll('.control input[type="number"], .control input[type="text"], .datetime-input')
            .forEach(input => input.value = '');
        
        selectors.getErrorArea().textContent = '';
        document.querySelectorAll('.notes').forEach(note => note.innerHTML = '');
    });

    document.getElementById('displayInput').addEventListener('click', function(event) {
        event.preventDefault();
        const errorArea = selectors.getErrorArea();
        
        if (isTableEmpty()) {
            const form = this.closest('form'); 
            form.action = '/display';
            form.method = 'GET';
            // console.log(`Submitting form with action ${form.action} and method ${form.method}`); 
            form.submit(); 
            form.action = '/submit';
            form.method = 'POST'; 
        } else {
            errorArea.textContent = 'Display failed: table is not empty, please submit or clear';
        }
    });
};

const setupResponsiveContainer = () => {
    const checkWidth = () => {
        const div = document.getElementById('container-div');
        div.className = window.innerWidth < 1000 ? "container-fluid" : "container";
    };

    checkWidth();
    window.addEventListener('resize', checkWidth);
};


$(document).ready(() => {
    setupDistanceConverters();
    setupKeyboardNavigation();
    setupFormButtons();
    setupResponsiveContainer();
});
