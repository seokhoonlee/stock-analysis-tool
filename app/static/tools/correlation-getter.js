$(".search").on("click", function() {
  var stockCode1 = $("#stockCode1").val();
  var stockCode2 = $("#stockCode2").val();
  var startTime = $("#datetimepicker1").val();
  var endTime = $("#datetimepicker2").val();

  if (stockCode1 == "" || stockCode1 == "" || startTime == "" || endTime == "") {
    return;
  }

  var data = {stockCode1: stockCode1, stockCode2: stockCode2, startTime: startTime, endTime: endTime};

  $.ajax({
    type : "POST",
    url : "/correlation/query/" + stockCode1 + "/" + stockCode2 + "/" + startTime + "/" + endTime,
    data: JSON.stringify(data),
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
      clearLineGraph();
      drawLineGraph("open1", "Price (US$)");
      drawLineGraph("open2", "Price (US$)");
      drawLineGraph("correlation", "Ratio");
    }
  }); 

  console.log(data);
});

$(".clear").on("click", function() {
  $.ajax({
    type : "POST",
    url : "/correlation/clear",
    data: JSON.stringify(""),
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
      clearLineGraph();
    }
  }); 
});

$("#datetimepicker1").datetimepicker({
  format: 'YYYY-MM-DD',
  icons: {
    time: "fa fa-clock-o",
    date: "fa fa-calendar",
    up: "fa fa-arrow-up",
    down: "fa fa-arrow-down"
  }
});

$("#datetimepicker2").datetimepicker({
  format: 'YYYY-MM-DD',
  icons: {
    time: "fa fa-clock-o",
    date: "fa fa-calendar",
    up: "fa fa-arrow-up",
    down: "fa fa-arrow-down"
  },
  useCurrent: false
});

$("#datetimepicker1").on("click", function() {
  $("#datetimepicker1").data("DateTimePicker").show();
  $("#datetimepicker1").on("dp.change", function (e) {
    $('#datetimepicker2').data("DateTimePicker").minDate(e.date);
  });
});

$("#datetimepicker2").on("click", function() {
  $("#datetimepicker2").data("DateTimePicker").show();
  $("#datetimepicker2").on("dp.change", function (e) {
    $('#datetimepicker1').data("DateTimePicker").maxDate(e.date);
  });
});