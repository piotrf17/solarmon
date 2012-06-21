<html>
  <head>
    <title>Grondel SolarMon</title>
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
        data.addRows([
        ${LAST_MINUTE}
        ]);

        var dataViewSolar = new google.visualization.DataView(data);
        dataViewSolar.setColumns([0, 1, 2]);
        var dataViewBattery = new google.visualization.DataView(data);
        dataViewBattery.setColumns([0, 3, 4]);

        var options = {
          displayAnnotations: true,
          vAxis: {0: {logScale: false, title: 'Current [A]'},
                  1: {logScale: false, title: 'Voltage [V]'}},
          series: {
            0: {targetAxisIndex: 0},
            1: {targetAxisIndex: 1}},
        }


        var chartSolar = new google.visualization.LineChart(document.getElementById('chart_lastminute_solar'));
        chartSolar.draw(dataViewSolar, options);

        var chartBattery = new google.visualization.LineChart(document.getElementById('chart_lastminute_battery'));
        chartBattery.draw(dataViewBattery, options);
      }

      function drawLastHourCharts() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime', 'Time');
        data.addColumn('number', 'Solar Current');
        data.addColumn('number', 'Solar Voltage');
        data.addColumn('number', 'Battery Current');
        data.addColumn('number', 'Battery Voltage');
        data.addRows([
        ${LAST_HOUR}
        ]);

        var dataViewSolar = new google.visualization.DataView(data);
        dataViewSolar.setColumns([0, 1, 2]);
        var dataViewBattery = new google.visualization.DataView(data);
        dataViewBattery.setColumns([0, 3, 4]);

        var options = {
          displayAnnotations: true,
          vAxis: {0: {logScale: false, title: 'Current [A]'},
                  1: {logScale: false, title: 'Voltage [V]'}},
          series: {
            0: {targetAxisIndex: 0},
            1: {targetAxisIndex: 1}},
        }


        var chartSolar = new google.visualization.LineChart(document.getElementById('chart_lasthour_solar'));
        chartSolar.draw(dataViewSolar, options);

        var chartBattery = new google.visualization.LineChart(document.getElementById('chart_lasthour_battery'));
        chartBattery.draw(dataViewBattery, options);
      }

      function drawLastDayCharts() {
        var data = new google.visualization.DataTable();
        data.addColumn('datetime', 'Time');
        data.addColumn('number', 'Solar Current');
        data.addColumn('number', 'Solar Voltage');
        data.addColumn('number', 'Battery Current');
        data.addColumn('number', 'Battery Voltage');
        data.addRows([
        ${LAST_DAY}
        ]);

        var dataViewSolar = new google.visualization.DataView(data);
        dataViewSolar.setColumns([0, 1, 2]);
        var dataViewBattery = new google.visualization.DataView(data);
        dataViewBattery.setColumns([0, 3, 4]);

        var options = {
          displayAnnotations: true,
          vAxis: {0: {logScale: false, title: 'Current [A]'},
                  1: {logScale: false, title: 'Voltage [V]'}},
          series: {
            0: {targetAxisIndex: 0},
            1: {targetAxisIndex: 1}},
        }


        var chartSolar = new google.visualization.LineChart(document.getElementById('chart_lastday_solar'));
        chartSolar.draw(dataViewSolar, options);

        var chartBattery = new google.visualization.LineChart(document.getElementById('chart_lastday_battery'));
        chartBattery.draw(dataViewBattery, options);
      }

      function drawCharts() {
        drawLastMinuteCharts();
        drawLastHourCharts();
        drawLastDayCharts();
      }
    </script>
  </head>

  <body>
    <div style="width:1222px">
      <h1>Grondel SolarMon</h1>
      <p>Last updated: ${UPDATE_TIME}</p>
      <h3>Last Minute</h3>
        <div id='chart_lastminute_solar' style='width: 600px; height: 400px; float: left;'></div>
        <div id='chart_lastminute_battery' style='width: 600px; height: 400px; float: left;'></div>
      <h3>Last Hour</h3>
        <div id='chart_lasthour_solar' style='width: 600px; height: 400px; float: left;'></div>
        <div id='chart_lasthour_battery' style='width: 600px; height: 400px; float: left;'></div>
      <h3>Last Day</h3>
        <div id='chart_lastday_solar' style='width: 600px; height: 400px; float: left;'></div>
        <div id='chart_lastday_battery' style='width: 600px; height: 400px; float: left;'></div>
    </div>
  </body>
</html>
