// ลิ้ง location
let ln = document.getElementById("location_name");
var location_name = sessionStorage.getItem("location_name");
ln.innerText = location_name;

function getBarData() {
  fetch("http://158.108.182.17:2255/get_time_A_yesterday")
    .then((response) => response.json())
    .then((data) => {
      for (var i = 10; i <= 21; i++) {
        in_yes = data[i].in  //จำนวนคนเข้า
        out_yes = data[i].out  // จำนวนคนออก
      }
    });
}

window.onload = function () {
  google.charts.load('current', { 'packages': ['corechart'] });

// ---------------------------------- Bar Chart.

  var box1 = new Array();
  var box2 = new Array();
  var check = 0
  fetch("http://158.108.182.17:2255/get_time_A_yesterday", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      for (var i = 10; i <= 21; i++) { //*********************** cannot read data ************************* */
        in_yes = data[i].in  //จำนวนคนเข้า
        out_yes = data[i].out  // จำนวนคนออก
        // box1.push(in_yes)
        // box2.push(out_yes)
        check = in_yes
      }
    });

    var chart = new CanvasJS.Chart("chartContainer", {
      animationEnabled: true,
      title:{
        text: "Yesterday"
      },	
      axisY: {
        title: "Number of people",
        titleFontColor: "#000",
        lineColor: "#000",
        labelFontColor: "#000",
        tickColor: "#000"
      },
      toolTip: {
        shared: true
      },
      legend: {
        cursor:"pointer",
        itemclick: toggleDataSeries
      },
      data: [{
        type: "column",
        name: "Entry",
        legendText: "Entry",
        showInLegend: true, 
        dataPoints:[
          { label: "10:00-13:00", y: 50 },//********************* Enter number of entering people *************************** */
          { label: "13:00-16:00", y: check },
          { label: "16:00-19:00", y: 25 },
          { label: "19:00-22:00", y: 20 }
        ]
      },
      {
        type: "column",	
        name: "Exit",
        legendText: "Exit",
        axisYType: "secondary",
        showInLegend: true,
        dataPoints:[
          { label: "10:00-13:00", y: 10 },//********************* enter number of exiting people *************************** */
          { label: "13:00-16:00", y: 12 },
          { label: "16:00-19:00", y: 31 },
          { label: "19:00-22:00", y: 40 }
        ]
      }]
    });
    chart.render();
    function toggleDataSeries(e) {
      if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
        e.dataSeries.visible = false;
      }
      else {
        e.dataSeries.visible = true;
      }
      chart.render();
    }
// ---------------------------------- Pie Chart.

  google.charts.setOnLoadCallback(drawChart2);
  fetch("http://158.108.182.17:2255/get_temp_A", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {
      pass = data.pass
      not_pass = data.not_pass
    });

  function drawChart2() {
    var data2 = google.visualization.arrayToDataTable([
      ['Category', 'Percentage'],
      ['PASS', pass],
      ['NOT PASS', not_pass]
    ]);
    var options2 = {
      // pieSliceBorderColor: '#fff',
      legend: { position: 'bottom', textStyle: { fontSize: 25 }, },
      backgroundColor: "#e9d5ae",
      title: 'Percentage',
      fontSize: 30,
      fontName: 'Nanum Gothic Coding',
      slices: [{ color: '#4dd77f', offset: 0 }, { color: '#f62f2f', offset: 0.1 }]
    };
    var chart2 = new google.visualization.PieChart(document.getElementById('piechart'));
    chart2.draw(data2, options2);
  }
}