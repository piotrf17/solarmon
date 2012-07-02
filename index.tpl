<html>
  <head>
    <title>Grondel SolarMon</title>
    <meta http-equiv="refresh" content="60">
    <script type='text/javascript' src='http://www.google.com/jsapi'></script>
    <script type='text/javascript'>
      google.load('visualization', '1', {'packages':['corechart','annotatedtimeline']});
      google.setOnLoadCallback(drawCharts);

      var last_hour_data = [
      ${LAST_HOUR}
      ];

      var last_day_data = [
      ${LAST_DAY}
      ];

      var last_week_data = [
      ${LAST_WEEK}
      ];

      function drawDefaultCharts(sensor_data, plots_tag) {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime', 'Time');
        data.addColumn('number', 'Solar Current');
        data.addColumn('number', 'Solar Voltage');
        data.addColumn('number', 'Battery Current');
        data.addColumn('number', 'Battery Voltage');
        data.addColumn('number', 'Temperature');
        data.addRows(sensor_data);

        var dataViewSolar = new google.visualization.DataView(data);
        dataViewSolar.setColumns([0, 2, 1]);
        var dataViewBattery = new google.visualization.DataView(data);
        dataViewBattery.setColumns([0, 4, 3]);
        var dataViewTemp = new google.visualization.DataView(data);
        dataViewTemp.setColumns([0, {calc: function(dataTable, rowNum) {return dataTable.getValue(rowNum, 5) * 1.8 + 32;},
                                  type: 'number', label: 'Monitor Board Temperature'}]);
        var dataViewEnergy = new google.visualization.DataView(data);
        dataViewEnergy.setColumns([0, 
          {calc: function(dataTable, rowNum) {return dataTable.getValue(rowNum, 1) * dataTable.getValue(rowNum, 2);},
           type: 'number', label: 'Solar Input Energy'},
          {calc: function(dataTable, rowNum) {return dataTable.getValue(rowNum, 3) * dataTable.getValue(rowNum, 4);},
           type: 'number', label: 'Battery Output Energy'}]);

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

        var chartSolar = new google.visualization.LineChart(document.getElementById('chart_solar_' + plots_tag));
        chartSolar.draw(dataViewSolar, options);

        var chartBattery = new google.visualization.LineChart(document.getElementById('chart_battery_' + plots_tag));
        chartBattery.draw(dataViewBattery, options);

        var chartTemp = new google.visualization.LineChart(document.getElementById('chart_temp_' + plots_tag));
        options.vAxes = [{logScale: false, format: '##.#\u00b0'}];
        chartTemp.draw(dataViewTemp, options); 

        var chartEnergy = new google.visualization.LineChart(document.getElementById('chart_energy_' + plots_tag));
        options.vAxes = [{logScale: false, format: '##.#W'}];
        options.series = {0: {targetAxisIndex: 0}, 1: {targetAxisIndex: 0}};
        chartEnergy.draw(dataViewEnergy, options);
      }

      function drawCharts() {
        drawDefaultCharts(last_hour_data, 'lasthour');
        drawDefaultCharts(last_day_data, 'lastday');
        drawDefaultCharts(last_week_data, 'lastweek');
      }
    </script>
  </head>

  <body>
    <div style="width:1622px">
      <h1>Grondel SolarMon</h1>
      <p>Last updated: ${UPDATE_TIME}</p>
      <h3>Last Hour</h3>
        <div id='chart_solar_lasthour' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_battery_lasthour' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_energy_lasthour' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_temp_lasthour' style='width: 400px; height: 300px; float: left;'></div>
      <h3>Last Day</h3>
        <div id='chart_solar_lastday' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_battery_lastday' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_energy_lastday' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_temp_lastday' style='width: 400px; height: 300px; float: left;'></div>
      <h3>Last Week</h3>
        <div id='chart_solar_lastweek' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_battery_lastweek' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_energy_lastweek' style='width: 400px; height: 300px; float: left;'></div>
        <div id='chart_temp_lastweek' style='width: 400px; height: 300px; float: left;'></div>
    </div>
  </body>
</html>
