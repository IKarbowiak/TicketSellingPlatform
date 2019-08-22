$( document ).ready(function() {
    var timer2 = $('.timer').text();
    var interval = setInterval(timer_tick, 1000);

  function timer_tick(){
        var timer = timer2.split(':');

        var minutes = parseInt(timer[0], 10);
        var seconds = parseInt(timer[1], 10);
        --seconds;
        minutes = (seconds < 0) ? --minutes : minutes;
        if (minutes < 0) {
            clearInterval(interval);
            $('#res_canceled')[0].click();
        }
        seconds = (seconds < 0) ? 59 : seconds;
        seconds = (seconds < 10) ? '0' + seconds : seconds;
        $('.timer').html(minutes + ':' + seconds);
        timer2 = minutes + ':' + seconds;
        };
});
