$( document ).ready(function() {
    var chosen_seats = $("#id_chosen_seats").val();
    if (chosen_seats !== undefined && chosen_seats !== "") {
        chosen_seats = chosen_seats .split(', ');
        $("#id_chosen_seats").val("");
        $("#tickets_counter").val(0);
        for (var i = 0; i < chosen_seats.length; i++) {
            changeclass($(`#${chosen_seats[i]}`));
        }
    }
});

function changeclass(element) {
    var chosen_seats = $("#id_chosen_seats").val();
    var tickets_amount = parseInt($("#tickets_counter").val());
    var seat = $(element).val();
    var new_chosen_seats_value = "";
    var element_type = seat.charAt(0);
    var type_counter = parseInt($(`#${element_type}`).text());

    if (jQuery(element).hasClass('booked')){
        $("#warning").val("Some seats have already been taken. Please choose another one.");
    }
    else if (jQuery(element).hasClass('chosen')) {
        $(element).removeClass('chosen');
        if (chosen_seats.includes(seat)){
            new_chosen_seats_value  = chosen_seats.replace(seat, '').replace(/,\s*$|^,/, "").replace(/,\s,\s*/, ", ");;
        }
        tickets_amount --;
        type_counter ++;
    }
    else {
        $(element).addClass('chosen');
        new_chosen_seats_value = chosen_seats.trim().length == 0 ? seat : (chosen_seats + ', ' + seat);

        tickets_amount ++;
        type_counter --;
    }
    $("#tickets_counter").val(tickets_amount);
    $("#id_chosen_seats").val(new_chosen_seats_value);
    $(`#${element_type}`).text(type_counter);
}

