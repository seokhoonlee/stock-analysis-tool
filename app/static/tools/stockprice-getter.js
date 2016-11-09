// function getStockPrice(stockName, dateFrom, dateTo) {
// 	console.log(stockName);
// 	console.log(dateFrom);
// 	console.log(dateTo);

// 	var BASE_URL = 'https://query.yahooapis.com/v1/public/yql?q=';
// 	var YQL_QUERY = 'select * from yahoo.finance.historicaldata where symbol in ("' + stockName + '") and startDate = "' + dateFrom + '" and endDate = "' + dateTo + '"';
// 	var YQL_QUERY_STR = encodeURI(BASE_URL + YQL_QUERY);
// 	var QUERY_STR = YQL_QUERY_STR + '&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys'

// 	$.getJSON(QUERY_STR, function(data) {
// 		var TSV_STRING = 'data\t' + stockName + '\n';	

// 		for (var i = 0; i < data.query.count; i++) {
// 			TSV_STRING += data.query.results.quote[i].Date + '\t' + data.query.results.quote[i].Close + '\n';
// 		}

// 		console.log(TSV_STRING);
// 	});
// }

$(".search").on("click", function() {
	// getStockPrice($("#stockcode").val(), $("#datetimepicker1").val(), $("#datetimepicker2").val());

	var stockCode = $("#stockCode").val();
	var startTime = $("#datetimepicker1").val();
	var endTime = $("#datetimepicker2").val();

	if (stockCode == "" || startTime == "" || endTime == "") {
		return;
	}

	var data = {stockCode: stockCode, startTime: startTime, endTime: endTime};

	$.ajax({
    type : "POST",
    url : "/technical/query/" + stockCode + "/" + startTime + "/" + endTime,
    data: JSON.stringify(data),
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
      // updateTable();
      clearLineGraph();
      drawLineGraph("openclose", "Price (US$)");
      drawLineGraph("highlow", "Price (US$)");
      drawLineGraph("volume", "Volume (x1000)");
      drawBarGraph("ratio");
    }
  });	

	console.log(data);
});

$(".clear").on("click", function() {
	$.ajax({
    type : "POST",
    url : "/technical/clear",
    data: JSON.stringify(""),
    contentType: 'application/json;charset=UTF-8',
    success: function(result) {
    	clearLineGraph();
    	clearBarGraph();
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