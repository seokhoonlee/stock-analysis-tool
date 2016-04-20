clearData()
drawGraph("openclose", "Price (US$)");
drawGraph("highlow", "Price (US$)");
drawGraph("volume", "Volume (x1000)");

function drawGraph(fileName, unit) {
  var margin = {top: 50, right: 50, bottom: 50, left: 50},
              width = 550 - margin.left - margin.right,
              height = 400 - margin.top - margin.bottom;

  var parseDate = d3.time.format("%Y%m%d").parse;

  var x = d3.time.scale()
      .range([0, width]);

  var y = d3.scale.linear()
      .range([height, 0]);

  var color = d3.scale.category10();

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");

  var line = d3.svg.line()
      .x(function(d) { return x(d.date); })
      .y(function(d) { return y(d.price); });

  var svg = d3.select("#svg-graph-technical").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.tsv("technical/data/" + fileName, function(error, data) {
    if (error) throw error;

    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

    data.forEach(function(d) {
      d.date = parseDate(d.date);
    });

    if (data.length == 0) {
      return;
    }

    var stocks = color.domain().map(function(name) {
      return {
        name: name,
        values: data.map(function(d) {
          return {date: d.date, price: +d[name]};
        })
      };
    });

    x.domain(d3.extent(data, function(d) { return d.date; }));

    y.domain([
      d3.min(stocks, function(c) { return d3.min(c.values, function(v) { return v.price; }); }),
      d3.max(stocks, function(c) { return d3.max(c.values, function(v) { return v.price; }); })
    ]);

    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text(unit);

    var stock = svg.selectAll(".stock")
        .data(stocks)
      .enter().append("g")
        .attr("class", "stock");

    stock.append("path")
        .attr("class", "line")
        .attr("d", function(d) { return line(d.values); })
        .style("stroke", function(d) { 
          if (d.name == 'Open') {
            return "#1f77b4";
          } else if (d.name == 'Close') {
            return "#ff7f0e";
          } else if (d.name == 'High') {
            return "#2ca02c";
          } else if (d.name == 'Low') {
            return "#d62728";
          } else if (d.name == 'Volume') {
            return "#9467bd";
          }

          return "#000000";
        });

    stock.append("text")
        .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
        .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.price) + ")"; })
        .attr("x", 3)
        .attr("dy", ".35em")
        .text(function(d) { return d.name; });
  });
}

function updateData() {
  clearData()
  drawGraph("openclose");
  drawGraph("highlow");
  drawGraph("volume");
}

function clearData() {
  d3.selectAll("svg > *").remove();
  d3.selectAll("svg").remove();
}