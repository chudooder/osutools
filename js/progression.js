var ProgressionChart = function () {
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // setup x 
    var xValue = function(d) { return d.timestamp; }, // data -> value
        xScale = d3.time.scale().nice(d3.time.year).range([0, width]), // value -> display
        xMap = function(d) { return xScale(xValue(d));}, // data -> display
        xAxis = d3.svg.axis().scale(xScale).orient("bottom");

    // setup y
    var yValue = function(d) { return d.difficultyrating;}, // data -> value
        yScale = d3.scale.linear().range([height, 0]), // value -> display
        yMap = function(d) { return yScale(yValue(d));}, // data -> display
        yAxis = d3.svg.axis().scale(yScale).orient("left");

    // setup fill color
    var cValue = function(d) { return d.criteria; },
        color = d3.scale.category10();

    var line = d3.svg.line()
        .interpolate('step-after')
        .x(function(d) { return xScale(d.timestamp); })
        .y(function(d) { return yScale(d.difficultyrating); });

    var tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    var svg = d3.select(".progression").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.json("data/difficulty_progression.json", function(error, data) {
        var criteria = ['passed', 'A', 'S', 'SS']

        xScale.domain([d3.min(data.passed, xValue), d3.time.month.offset(d3.max(data.passed, xValue), 1)]);
        yScale.domain([0, d3.max(data.passed, yValue)]);

        // x-axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
        .append("text")
            .attr("class", "label")
            .attr("x", width)
            .attr("y", -6)
            .style("text-anchor", "end")
            .text("Date");

        // y-axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
        .append("text")
            .attr("class", "label")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Star Difficulty");

        criteria.forEach(function(crit) {
            data[crit].forEach(function(d) {
                d.timestamp = new Date(+d.timestamp);
                d.difficultyrating = +d.difficultyrating;
                d.criteria = crit;
            });

            svg.append("path")
                .datum(data[crit])
                .attr("class", "line")
                .attr("d", line)
                .style("stroke", function(d) { return color(cValue(d[0])); });

            svg.selectAll('.dot [crit]')
                .data(data[crit])
            .enter().append("circle")
                .attr("class", "dot")
                .attr("r", 5)
                .attr("cx", xMap)
                .attr("cy", yMap)
                .style("fill", function(d) { return color(cValue(d)); })
            .on("mouseover", function(d) {
                if(d3.select(this).attr("active") === "false") {
                    return;
                }
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);
                tooltip.html(d.song_title+ " - " + d.version 
                    + "<br/> Date: " + d.timestamp
                    + "<br/> Diff: " + d.difficultyrating.toFixed(2))
                    .style("left", (d3.event.pageX + 5) + "px")
                    .style("top", (d3.event.pageY - 28) + "px");
            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
            });

        });


        
        


        // draw legend
        var legend = svg.selectAll(".legend")
            .data(color.domain())
        .enter().append("g")
            .attr("class", "legend")
            .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

        // draw legend colored rectangles
        legend.append("rect")
            .attr("x", width - 18)
            .attr("width", 18)
            .attr("height", 18)
            .style("fill", color);

        // draw legend text
        legend.append("text")
            .attr("x", width - 24)
            .attr("y", 9)
            .attr("dy", ".35em")
            .style("text-anchor", "end")
            .text(function(d) {
                return d;
            });

    });

    return {};
};