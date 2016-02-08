var ModSelect = function(scatter) {
    var scatterplot = scatter;
    var mods = ["no_mod", "double_time", "hidden", "hard_rock", "no_fail"];
    var mod_filter = [];

    var updateMods = function(button) {
        var d = d3.select(button);
        var mod = d.attr("mod");
        if(d.node().checked) {
            mod_filter.push(mod);
        } else {
            var index = mod_filter.indexOf(mod);
            if(index != -1) {
                mod_filter.splice(index, 1);
            } else {
                console.log("PANIC! Mod is not in current mods");
            }
        }
        scatterplot.updateScores(mod_filter);
    }

    d3.select("#mod_select").selectAll("input")
        .data(mods)
        .enter()
        .append('label')
        .text(function(d) {
            // capitalize and remove underscore
            var spl = d.split("_");
            var str = []
            for(i=0; i<spl.length; i++) {
                str.push(spl[i].charAt(0).toUpperCase() + spl[i].slice(1));
            }
            return str.join(" ");
        })
    .append("input")
        .attr("class", "mod_button")
        .attr("mod", function(d) { return d; })
        .attr("type", "checkbox")
        .on("change", function() {
            updateMods(this);
        });

    return {
        updateMods: updateMods
    };
}