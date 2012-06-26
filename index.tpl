<html>
  <head>
    <title>Grondel SolarMon</title>
    <meta http-equiv="refresh" content="60">
    <script type='text/javascript' src='http://www.google.com/jsapi'></script>
    <script type='text/javascript'>
      google.load('visualization', '1', {'packages':['corechart','annotatedtimeline']});
      google.setOnLoadCallback(drawCharts);

      function drawLastMinuteCharts() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime', 'Time');
        data.addColumn('number', 'Solar Current');
        data.addColumn('number', 'Solar Voltage');
        data.addColumn('number', 'Battery Current');
        data.addColumn('number', 'Battery Voltage');
        data.addColumn('number', 'Temperature');
        data.addRows([
        ${LAST_MINUTE}
        ]);

        var dataViewSolar = new google.visualization.DataView(data);
        dataViewSolar.setColumns([0, 2, 1]);
        var dataViewBattery = new google.visualization.DataView(data);
        dataViewBattery.setColumns([0, 4, 3]);
        var dataViewTemp = new google.visualization.DataView(data);
        dataViewTemp.setColumns([0, {calc: function(dataTable, rowNum) {return dataTable.getValue(rowNum, 5) * 1.8 + 32;},
                                  type: 'number', label: 'Temperature'}]);

        var options = {
          displayAnnotations: true,
          vAxes: [{logScale: false, format: '##.##V'},
                  {logScale: false, format: '#.##A'}],
          series: {
            0: {targetAxisIndex: 0},
            1: {targetAxisIndex: 1}},
          chartArea: {left: "10%", top: "8%", width: "80%", height: "80%"},
          legend: {position: "top"},
        }


        var chartSolar = new google.visualization.LineChart(document.getElementById('chart_lastminute_solar'));
        chartSolar.draw(dataViewSolar, options);

        var chartBattery = new google.visualization.LineChart(document.getElementById('chart_lastminute_battery'));
        chartBattery.draw(dataViewBattery, options);

        var chartTemp = new google.visualization.LineChart(document.getElementById('chart_lastminute_temp'));
        options.vAxes = [{logScale: false, format: '##.#\u00b0'}];
        chartTemp.draw(dataViewTemp, options);
      }

      function drawLastHourCharts() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime', 'Time');
        data.addColumn('number', 'Solar Current');
        data.addColumn('number', 'Solar Voltage');
        data.addColumn('number', 'Battery Current');
        data.addColumn('number', 'Battery Voltage');
        data.addColumn('number', 'Temperature');
        data.addRows([
        ${LAST_HOUR}
        ]);

        var dataViewSolar = new google.visualization.DataView(data);
        dataViewSolar.setColumns([0, 2, 1]);
        var dataViewBattery = new google.visualization.DataView(data);
        dataViewBattery.setColumns([0, 4, 3]);
        var dataViewTemp = new google.visualization.DataView(data);
        dataViewTemp.setColumns([0, {calc: function(dataTable, rowNum) {return dataTable.getValue(rowNum, 5) * 1.8 + 32;},
                                  type: 'number', label: 'Temperature'}]);

        var options = {
          displayAnnotations: true,
          vAxes: [{logScale: false, format: '##.##V'},
                  {logScale: false, format: '#.##A'}],
          series: {
            0: {targetAxisIndex: 0},
            1: {targetAxisIndex: 1}},
          chartArea: {left: "10%", top: "8%", width: "80%", height: "80%"},
          legend: {position: "top"},
        }

        var chartSolar = new google.visualization.LineChart(document.getElementById('chart_lasthour_solar'));
        chartSolar.draw(dataViewSolar, options);

        var chartBattery = new google.visualization.LineChart(document.getElementById('chart_lasthour_battery'));
        chartBattery.draw(dataViewBattery, options);

        var chartTemp = new google.visualization.LineChart(document.getElementById('chart_lasthour_temp'));
        options.vAxes = [{logScale: false, format: '##.#\u00b0'}];
        chartTemp.draw(dataViewTemp, options); 
      }

      function drawLastDayCharts() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime', 'Time');
        data.addColumn('number', 'Solar Current');
        data.addColumn('number', 'Solar Voltage');
        data.addColumn('number', 'Battery Current');
        data.addColumn('number', 'Battery Voltage');
        data.addColumn('number', 'Temperature');
        data.addRows([
        ${LAST_DAY}
        ]);

        var dataViewSolar = new google.visualization.DataView(data);
        dataViewSolar.setColumns([0, 2, 1]);
        var dataViewBattery = new google.visualization.DataView(data);
        dataViewBattery.setColumns([0, 4, 3]);
        var dataViewTemp = new google.visualization.DataView(data);
        dataViewTemp.setColumns([0, {calc: function(dataTable, rowNum) {return dataTable.getValue(rowNum, 5) * 1.8 + 32;},
                                  type: 'number', label: 'Temperature'}]);

        var options = {
          displayAnnotations: true,
          vAxes: [{logScale: false, format: '##.##V'},
                  {logScale: false, format: '#.##A'}],
          series: {
            0: {targetAxisIndex: 0},
            1: {targetAxisIndex: 1}},
          chartArea: {left: "10%", top: "8%", width: "80%", height: "80%"},
          legend: {position: "top"},
        }

        var chartSolar = new google.visualization.LineChart(document.getElementById('chart_lastday_solar'));
        chartSolar.draw(dataViewSolar, options);

        var chartBattery = new google.visualization.LineChart(document.getElementById('chart_lastday_battery'));
        chartBattery.draw(dataViewBattery, options);

        var chartTemp = new google.visualization.LineChart(document.getElementById('chart_lastday_temp'));
        options.vAxes = [{logScale: false, format: '##.#\u00b0'}];
        chartTemp.draw(dataViewTemp, options); 
      }

      function drawLastWeekCharts() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime', 'Time');
        data.addColumn('number', 'Solar Current');
        data.addColumn('number', 'Solar Voltage');
        data.addColumn('number', 'Battery Current');
        data.addColumn('number', 'Battery Voltage');
        data.addColumn('number', 'Temperature');
        data.addRows([
        ${LAST_WEEK}
        ]);

        var dataViewSolar = new google.visualization.DataView(data);
        dataViewSolar.setColumns([0, 2, 1]);
        var dataViewBattery = new google.visualization.DataView(data);
        dataViewBattery.setColumns([0, 4, 3]);
        var dataViewTemp = new google.visualization.DataView(data);
        dataViewTemp.setColumns([0, {calc: function(dataTable, rowNum) {return dataTable.getValue(rowNum, 5) * 1.8 + 32;},
                                  type: 'number', label: 'Temperature'}]);

        var options = {
          displayAnnotations: true,
          vAxes: [{logScale: false, format: '##.##V'},
                  {logScale: false, format: '#.##A'}],
          series: {
            0: {targetAxisIndex: 0},
            1: {targetAxisIndex: 1}},
          chartArea: {left: "10%", top: "8%", width: "80%", height: "80%"},
          legend: {position: "top"},
        }

        var chartSolar = new google.visualization.LineChart(document.getElementById('chart_lastweek_solar'));
        chartSolar.draw(dataViewSolar, options);

        var chartBattery = new google.visualization.LineChart(document.getElementById('chart_lastweek_battery'));
        chartBattery.draw(dataViewBattery, options);

        var chartTemp = new google.visualization.LineChart(document.getElementById('chart_lastweek_temp'));
        options.vAxes = [{logScale: false, format: '##.#\u00b0'}];
        chartTemp.draw(dataViewTemp, options); 
      }


      function drawCharts() {
        drawLastMinuteCharts();
        drawLastHourCharts();
        drawLastDayCharts();
        drawLastWeekCharts();
      }
    </script>
  </head>

  <body>
    <div style="width:1222px">
      <h1>Grondel SolarMon</h1>
      <p>Last updated: ${UPDATE_TIME}</p>
      <h3>Last Minute</h3>
        <div id='chart_lastminute_solar' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_lastminute_battery' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_lastminute_temp' style='width: 400px; height: 300px; float: left;'></div>
      <h3>Last Hour</h3>
        <div id='chart_lasthour_solar' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_lasthour_battery' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_lasthour_temp' style='width: 400px; height: 300px; float: left;'></div>
      <h3>Last Day</h3>
        <div id='chart_lastday_solar' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_lastday_battery' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_lastday_temp' style='width: 400px; height: 300px; float: left;'></div>
      <h3>Last Week</h3>
        <div id='chart_lastweek_solar' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_lastweek_battery' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_lastweek_temp' style='width: 400px; height: 300px; float: left;'></div>
    </div>
  </body>
</html>
