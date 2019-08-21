function changeclass(element) {
    var chosen_seats = $("#chosen_seats").val();
    var tickets_amount = parseInt($("#tickets_counter").val());
    var seat = $(element).val();
    var new_chosen_seats_value = "";

    if (jQuery(element).hasClass('chosen')) {
        $(element).removeClass('chosen');
        console.log("remove");
        if (chosen_seats.includes(seat)){
            new_chosen_seats_value  = chosen_seats.replace(seat, '').replace(/,\s*$/, "");;
        }
        tickets_amount --;
    }
    else {
        $(element).addClass('chosen');
        console.log(chosen_seats);
        new_chosen_seats_value = chosen_seats.trim().length == 0 ? seat : (chosen_seats + ', ' + seat);

        tickets_amount ++;
    }
    $("#tickets_counter").val(tickets_amount);
    $("#chosen_seats").val(new_chosen_seats_value);
}

$(document).ready(function() {

});

