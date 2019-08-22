//function makeTimer() {
//		var endTime = new Date("15:00");
//			endTime = (Date.parse(endTime) / 1000);
//
//			var now = new Date();
//			now = (Date.parse(now) / 1000);
//
//			var timeLeft = endTime - now;
//
//			var days = Math.floor(timeLeft / 86400);
//			var hours = Math.floor((timeLeft - (days * 86400)) / 3600);
//			var minutes = Math.floor((timeLeft - (days * 86400) - (hours * 3600 )) / 60);
//			var seconds = Math.floor((timeLeft - (days * 86400) - (hours * 3600) - (minutes * 60)));
//
//			if (hours < "10") { hours = "0" + hours; }
//			if (minutes < "10") { minutes = "0" + minutes; }
//			if (seconds < "10") { seconds = "0" + seconds; }
//
//			$("#days").html(days + "<span>Days</span>");
//			$("#hours").html(hours + "<span>Hours</span>");
//			$("#minutes").html(minutes + "<span>Minutes</span>");
//			$("#seconds").html(seconds + "<span>Seconds</span>");
//
//	}
//
//	setInterval(function() { makeTimer(); }, 1000);
//

//var timer2 = "";
//while (timer2 === ""){
//    timer2 = $('.timer').text();
//};
//var interval = setInterval(function() {
//
//var timer = timer2.split(':');
//console.log(timer);
//var minutes = parseInt(timer[0], 10);
//var seconds = parseInt(timer[1], 10);
//--seconds;
//minutes = (seconds < 0) ? --minutes : minutes;
//if (minutes < 0) clearInterval(interval);
//seconds = (seconds < 0) ? 59 : seconds;
//seconds = (seconds < 10) ? '0' + seconds : seconds;
//$('.timer').html(minutes + ':' + seconds);
//timer2 = minutes + ':' + seconds;
//}, 1000);

$( document ).ready(function() {
    var timer2 = $('.timer').text();
    setInterval(timer_tick, 1000);

  function timer_tick(){
        var timer = timer2.split(':');

        var minutes = parseInt(timer[0], 10);
        var seconds = parseInt(timer[1], 10);
        --seconds;
        minutes = (seconds < 0) ? --minutes : minutes;
        if (minutes < 0) clearInterval(interval);
        seconds = (seconds < 0) ? 59 : seconds;
        seconds = (seconds < 10) ? '0' + seconds : seconds;
        $('.timer').html(minutes + ':' + seconds);
        timer2 = minutes + ':' + seconds;
        };
});

//var timer2 = "15:00";
//var interval = setInterval(function() {
//
//  var timer = timer2.split(':');
//
//  var minutes = parseInt(timer[0], 10);
//  var seconds = parseInt(timer[1], 10);
//  --seconds;
//  minutes = (seconds < 0) ? --minutes : minutes;
//  if (minutes < 0) clearInterval(interval);
//  seconds = (seconds < 0) ? 59 : seconds;
//  seconds = (seconds < 10) ? '0' + seconds : seconds;
//  $('.timer').html(minutes + ':' + seconds);
//  timer2 = minutes + ':' + seconds;
//}, 1000);

//function timerStart() {
//    var timer2 = "15:00";
//    var interval = setInterval(function() {
//
//      var timer = timer2.split(':');
//
//      var minutes = parseInt(timer[0], 10);
//      var seconds = parseInt(timer[1], 10);
//      --seconds;
//      minutes = (seconds < 0) ? --minutes : minutes;
//      if (minutes < 0) clearInterval(interval);
//      seconds = (seconds < 0) ? 59 : seconds;
//      seconds = (seconds < 10) ? '0' + seconds : seconds;
//      $('.countdown').html(minutes + ':' + seconds);
//      timer2 = minutes + ':' + seconds;
//    }, 1000);
//}