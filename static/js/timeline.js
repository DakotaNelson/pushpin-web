var TIMELINE = {

  elementId: "#timeline",

  minTime: null,
  maxTime: null,
  numBins: 80,
  binSize: null,

  data: null, // note: this is always CLEANED data
  active: null, // array of strings describing the active data sources

  createTimeline: function(data) {
    if (TIMELINE.active == null) {
      // if the list of active sources hasn't been initialized, do so
      TIMELINE.active = d3.keys(data);
      TIMELINE.active.push('total');
    }

    var clean = TIMELINE.cleanData(data);
    TIMELINE.render(clean);
  },

  update: function() {
    TIMELINE.clear();
    TIMELINE.render(TIMELINE.data);
  },

  clear: function() {
    var container = document.getElementById(TIMELINE.elementId.substr(1));
    while(container.firstChild) {
      container.removeChild(container.firstChild);
    }
  },

  addActive: function(source) {
    if(TIMELINE.active.indexOf(source) == -1) {
      TIMELINE.active.push(source);
      TIMELINE.update();
    }
  },

  removeActive: function(source) {
    TIMELINE.active = TIMELINE.active.filter(function(elem) {
        if(elem === source){ return false; }
        else { return true; }
        });
    TIMELINE.update();
  },

  cleanData:function (timelineData) {

    //var active = d3.keys(timelineData);
    //TIMELINE.active = active;

    var dateFormat = d3.time.format("%%Y-%%m-%%d %%H:%%M:%%S");

    d3.entries(timelineData).forEach(function(entry) {
      timelineData[entry.key] = entry.value.map(function(time) { return dateFormat.parse(time); });
      // format all of the dates as date objects instead of strings and remove anything older than 5 years
    });

    d3.entries(timelineData).forEach(function(entry) {
      timelineData[entry.key] = entry.value.filter(function(time) { console.log(time); if(new Date().getFullYear() - time.getFullYear() < 5) { return true; } return false; });
      // filter out any pins older than 4ish years
    });

    var allData = d3.merge(d3.values(timelineData)); // all of the retrieved objects in one giant var

    //var weird = allData.filter(function(item) { if(item.getFullYear() < 1995) { return true; } return false; });
    //console.log(weird);

    TIMELINE.minTime = d3.min(allData).getTime();
    TIMELINE.maxTime = d3.max(allData).getTime();

    TIMELINE.binSize = (TIMELINE.maxTime - TIMELINE.minTime) / TIMELINE.numBins;

    // Initialize series structure.
    var series = {};
    TIMELINE.active.map(function(key) {
      series[key] = [];
    });

    // Set up empty bins.
    for(var i=0; i< TIMELINE.numBins+1; i++) {
      TIMELINE.active.map(function(key) {
        series[key].push({time:new Date(TIMELINE.minTime+(i*TIMELINE.binSize)), count:0});
      });
    }

    // Bin pins.
    d3.entries(timelineData).forEach(function(entry) {
      entry.value.map(function(pin) {
        var source = entry.key;
        var time = pin.getTime();
        var bindex = Math.floor((time-TIMELINE.minTime)/TIMELINE.binSize); // the index of the bin this pin goes in (for great win)

        if (0 <= bindex && bindex <= TIMELINE.numBins) {
          series['total'][bindex].count += 1;
          if (TIMELINE.active.indexOf(source) != -1) {
            series[source][bindex].count += 1;
          }
        }
      });
    });

    // Add empty first and last bins to each series -> line needs to start and end on x axis so fills work
    TIMELINE.active.map(function(key) {
      series[key] = [{time: new Date(TIMELINE.minTime-TIMELINE.binSize), count:0}].concat(series[key]); // empty first bin
      series[key].push({time:new Date(TIMELINE.minTime+((TIMELINE.numBins+1)*TIMELINE.binSize)), count:0}); // empty last bin
    });

    // Reformat for d3.
    // http://www.delimited.io/blog/2014/3/3/creating-multi-series-charts-in-d3-lines-bars-area-and-streamgraphs
    var res = [];
    for (key in series) {
      res.push({label:key, values:series[key]});
    }
    TIMELINE.data = res;
    return res;
  },


  render: function(timelineData) {

    // first: filter the data so we're only rendering the active set
    timelineData = timelineData.filter( function(item) {
      if(TIMELINE.active.indexOf(item.label) != -1) {
        return true;
      }
      return false;
    });

    // then find what we're putting this chart into, and get sizes
    var container = d3.select(TIMELINE.elementId);
    TIMELINE.width = container.node().offsetWidth;
    TIMELINE.height = container.node().offsetHeight;

    // add margins
    var margin = {"top":10, "right":30, "bottom":30, "left":60};
    var width = TIMELINE.width - margin.left - margin.right;
    var height = TIMELINE.height - margin.top - margin.bottom; // this handles margins for us

    var x = d3.time.scale()
                   .range([0, width])
                   .domain([TIMELINE.minTime - TIMELINE.binSize, TIMELINE.maxTime + TIMELINE.binSize]);

    var y = d3.scale.linear()
                    .domain([0, d3.max(timelineData[timelineData.length-1].values, function(d){ return d.count; })])
                    .range([height, 0]);

    var xAxis = d3.svg.axis()
                      .scale(x)
                      .orient("bottom")
                      .tickSize(-height)
                      .tickPadding(6);

    var yAxis = d3.svg.axis()
                      .scale(y)
                      .orient('left')
                      .ticks(3)
                      .tickSize(-width)
                      .tickFormat(d3.format("d"));

    var all_styles = {'flickr':{color: '#FF9900', width: '1px', fillOpacity: '0.2'},
                      'picasa':{ color: '#7E55FC', width: '1px', fillOpacity: '0.2'},
                      'shodan':{ color: '#FCF357', width: '1px', fillOpacity: '0.2'},
                      'twitter':{ color: '#5781FC', width: '1px', fillOpacity: '0.2'},
                      'youtube':{ color: '#FC6355', width: '1px', fillOpacity: '0.2'},
                      'total':{ color: 'Black', width: '1px', fillOpacity: '0.2'}};

    var active_styles = TIMELINE.active.map( function(item) { return all_styles[item];  } );

    var style = d3.scale.ordinal()
                        .range(active_styles)
                        .domain(TIMELINE.active);

    var svg = container.append("svg")
                       .attr("width", width+margin.left+margin.right)
                       .attr("height", height+margin.top+margin.bottom)
                     .append("g")
                       .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var line = d3.svg.line()
                     .x(function(d) { return x(d.time); })
                     .y(function(d) { return y(d.count); })
                     .interpolate("basis");

    var series = svg.selectAll(".series")
                      .data(timelineData)
                    .enter().append("g")
                      .attr("class","series");

    series.append("path")
          .attr("class","line")
          .attr("d", function(d) { return line(d.values); })
          .style("stroke", function (d) { return style(d.label).color; })
          .style('stroke-width', function (d) { return style(d.label).width; })
          .style('fill', function (d) { return style(d.label).color; })
          .style('fill-opacity', function (d) { return style(d.label).fillOpacity; });

    svg.append("g")
       .attr("class", "x axis")
       .attr("transform", "translate(0," + height + ")")
       .call(xAxis);

    svg.append("g")
       .attr("class", "y axis")
       .call(yAxis)
       .append("text")
       .attr("transform","rotate(-90)")
       .attr("y", -90)
       .attr("x", 0)
       .attr("dy", ".71em")
       .style("text-anchor","end")
       .text("Pins");

  },
};
