function getStockPrice(stockName, dateFrom, dateTo) {
	console.log(stockName);
	console.log(dateFrom);
	console.log(dateTo);

	var BASE_URL = 'https://query.yahooapis.com/v1/public/yql?q=';
	var YQL_QUERY = 'select * from yahoo.finance.historicaldata where symbol in ("' + stockName + '") and startDate = "' + dateFrom + '" and endDate = "' + dateTo + '"';
	var YQL_QUERY_STR = encodeURI(BASE_URL + YQL_QUERY);
	var QUERY_STR = YQL_QUERY_STR + '&format=json&diagnostics=true&env=store://datatables.org/alltableswithkeys'

	$.getJSON(QUERY_STR, function(data) {
		console.log(data);
	});
}

$(".search").on("click", function() {
	getStockPrice($("#stockcode").val(), $("#datetimepicker1").val(), $("#datetimepicker2").val());
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