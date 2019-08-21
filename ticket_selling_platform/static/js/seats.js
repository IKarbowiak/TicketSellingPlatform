function changeclass(element) {
    if (jQuery(element).hasClass('chosen')) {
        $(element).removeClass('chosen');
        console.log("remove");
    }
    else {
        $(element).addClass('chosen');
        console.log("add");
    }
}

$(document).ready(function() {

});

