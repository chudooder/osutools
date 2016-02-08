var Scatterplot = function() {

    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 400 - margin.top - margin.bottom;

    // setup x 
    var xValue = function(d) { return d.difficultyrating;}, // data -> value
        xScale = d3.scale.linear().range([0, width]), // value -> display
        xMap = function(d) { return xScale(xValue(d));}, // data -> display
        xAxis = d3.svg.axis().scale(xScale).orient("bottom");

    // setup y
    var yValue = function(d) { return d.accuracy;}, // data -> value
        yScale = d3.scale.pow().exponent(3).range([height, 0]), // value -> display
        yMap = function(d) { return yScale(yValue(d));}, // data -> display
        yAxis = d3.svg.axis().scale(yScale).orient("left");

    // setup fill color
    var cValue = function(d) { return d.mode;},
        color = d3.scale.category10();

    // add the graph canvas to the body of the webpage
    var svg = d3.select(".scatterplot").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // add the tooltip area to the webpage
    var tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // load data
    d3.csv("data/scores_best.csv", function(error, data) {
        data.forEach(function(d) {
            d.difficultyrating = Math.min(+d.difficultyrating, 10);
            d.accuracy = 100 * +d.accuracy;
            d.timestamp = new Date(+d.timestamp);
        })

        // don't want dots overlapping axis, so add in buffer to data domain
        xScale.domain([d3.min(data, xValue), d3.max(data, xValue)]);
        yScale.domain([d3.min(data, yValue), d3.max(data, yValue)]);

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
            .text("Star Difficulty");

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
            .text("Accuracy");

        // draw dots
        svg.selectAll(".dot")
            .data(data)
        .enter().append("circle")
            .attr("class", "dot")
            .attr("r", 3.5)
            .attr("cx", xMap)
            .attr("cy", yMap)
            .style("fill", function(d) { return color(cValue(d));})
            .on("mouseover", function(d) {
                if(d3.select(this).attr("active") === "false") {
                    return;
                }
                tooltip.transition()
                    .duration(200)
                    .style("opacity", .9);
                tooltip.html(d.song_title+ " - " + d.version 
                    + "<br/> Acc: " + d.accuracy.toFixed(2)
                    + "<br/> Diff: " + d.difficultyrating.toFixed(2))
                    .style("left", (d3.event.pageX + 5) + "px")
                    .style("top", (d3.event.pageY - 28) + "px");
            })
            .on("mouseout", function(d) {
                tooltip.transition()
                    .duration(500)
                    .style("opacity", 0);
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
                var modes = ["osu!std", "Taiko", "CtB", "osu!mania"];
                return modes[d];
            });
    });

    var updateScores = function(mod_filter) {
        svg.selectAll(".dot")
            .attr("opacity", function(d) {
                for(mod in mod_filter) {
                    if(d[mod_filter[mod]] === "False") {
                        return 0.0;
                    }
                }
                return 1.0;
            });
    }

    // module stuff
    return {
        updateScores: updateScores
    };
}; 

