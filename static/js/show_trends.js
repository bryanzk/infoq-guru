function waitForMsg(){
        /* This requests the url "msgsrv.php"
        When it complete (or errors)*/
        $.ajax({
            type: "GET",
            url: "notifyget",
            async: true, /* If set to non-async, browser shows page as "Loading.."*/
            cache: false,
            timeout:50000, /* Timeout in ms */
            success: function(data){ /* called when request to barge.php completes */
              if(data!=''){
                humane.log(data);
              }
                setTimeout(
                    'waitForMsg()', /* Request next message */
                    5000 /* ..after 1 seconds */
                );
            },
            error: function(XMLHttpRequest, textStatus, errorThrown){

              humane.clickToClose = true // default: false
                humane.log('error');
                setTimeout(
                    'waitForMsg()', /* Try again after.. */
                    "15000"); /* milliseconds (15seconds) */
            }
        });
    };



function show_trends(width,height,url,select){   
    var m = [30, 30, 30, 30],
    w = width - m[1] - m[3],
    h = height- m[0] - m[2],
    parse = d3.time.format("%Y %m %d").parse;

// Scales and axes. Note the inverted domain for the y-scale: bigger is up!
var x = d3.time.scale().range([0, w]),
    y = d3.scale.linear().range([h, 0]),
    xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true),
    yAxis = d3.svg.axis().scale(y).ticks(4).orient("right");

// An area generator, for the light fill.
var area = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return x(d.date); })
    .y0(h)
    .y1(function(d) { return y(d.price); });

// A line generator, for the dark stroke.
var line = d3.svg.line()
    .interpolate("monotone")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.price); });

d3.json(url, function(data) {

  
  var values=data;

  // Parse dates and numbers. We assume values are sorted by date.
  values.forEach(function(d) {
    d.date = parse(d.date);
    d.price = +d.price;
  });

  // Compute the minimum and maximum date, and the maximum price.
  x.domain([values[0].date, values[values.length - 1].date]);
  y.domain([0, d3.max(values, function(d) { return d.price; })]).nice();

  // Add an SVG element with the desired dimensions and margin.
  var svg = d3.select(select).append("svg:svg")
      .attr("width", w + m[1] + m[3])
      .attr("height", h + m[0] + m[2])
    .append("svg:g")
      .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

  // Add the clip path.
  svg.append("svg:clipPath")
      .attr("id", "clip")
    .append("svg:rect")
      .attr("width", w)
      .attr("height", h);

  // Add the area path.
  svg.append("svg:path")
      .attr("class", "area")
      .attr("clip-path", "url(#clip)")
      .attr("d", area(values));

  // Add the x-axis.
  svg.append("svg:g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + h + ")")
      .call(xAxis);

  // Add the y-axis.
  svg.append("svg:g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + w + ",0)")
      .call(yAxis);

  // Add the line path.
  svg.append("svg:path")
      .attr("class", "line")
      .attr("clip-path", "url(#clip)")
      .attr("d", line(values));

  // Add a small label for the symbol name.
  svg.append("svg:text")
      .attr("x", w - 6)
      .attr("y", h - 6)
      .attr("text-anchor", "end")
      .text(values[0].symbol);

  svg.on("click", function() {
    var n = values.length - 1,
        i = Math.floor(Math.random() * n / 2),
        j = i + Math.floor(Math.random() * n / 2) + 1;
    x.domain([values[i].date, values[j].date]);
    var t = svg.transition().duration(750);
    t.select(".x.axis").call(xAxis);
    t.select(".area").attr("d", area(values));
    t.select(".line").attr("d", line(values));
  });
  
  
});
}






function show_trends2(width,height,url,select){   
    var m = [30, 30, 30, 30],
    w = width - m[1] - m[3],
    h = height- m[0] - m[2],
    parse = d3.time.format("%Y %m %d").parse;

// Scales and axes. Note the inverted domain for the y-scale: bigger is up!
var x = d3.time.scale().range([0, w]),
    y = d3.scale.linear().range([h, 0]),
    xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true),
    yAxis = d3.svg.axis().scale(y).ticks(4).orient("right");

// An area generator, for the light fill.
var area = d3.svg.area()
    .interpolate("monotone")
    .x(function(d) { return x(d.date); })
    .y0(h)
    .y1(function(d) { return y(d.price); });

// A line generator, for the dark stroke.
var line = d3.svg.line()
    .interpolate("monotone")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.price); });

d3.json(url, function(data) {

  // Filter to one symbol; the S&P 500.
  //var values = data.filter(function(d) {
  // return d.symbol == "S&P 500";
  //});
  var values=data;

  // Parse dates and numbers. We assume values are sorted by date.
  values.forEach(function(d) {
    d.date = parse(d.date);
    d.price = +d.price;
  });

  // Compute the minimum and maximum date, and the maximum price.
  x.domain([values[0].date, values[values.length - 1].date]);
  y.domain([0, d3.max(values, function(d) { return d.price; })]).nice();

  // Add an SVG element with the desired dimensions and margin.
  var svg = d3.select(select).append("svg:svg")
      .attr("width", w + m[1] + m[3])
      .attr("height", h + m[0] + m[2])
    .append("svg:g")
      .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

  // Add the clip path.
  svg.append("svg:clipPath")
      .attr("id", "clip")
    .append("svg:rect")
      .attr("width", w)
      .attr("height", h);

  // Add the area path.
  svg.append("svg:path")
      .attr("class", "area")
      .attr("clip-path", "url(#clip)")
      .attr("d", area(values));



  // Add the y-axis.
  svg.append("svg:g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + w + ",0)")
      .call(yAxis);

  // Add the line path.
  svg.append("svg:path")
      .attr("class", "line")
      .attr("clip-path", "url(#clip)")
      .attr("d", line(values));

svg.on("click", function() {
    var n = values.length - 1,
        i = Math.floor(Math.random() * n / 2),
        j = i + Math.floor(Math.random() * n / 2) + 1;
    x.domain([values[i].date, values[j].date]);
    var t = svg.transition().duration(750);
    t.select(".x.axis").call(xAxis);
    t.select(".area").attr("d", area(values));
    t.select(".line").attr("d", line(values));
  });

  
});
}