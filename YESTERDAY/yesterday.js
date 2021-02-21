// ลิ้ง location
let ln = document.getElementById("location_name");
var location_name = sessionStorage.getItem("location_name");
ln.innerText = location_name;

window.onload = function () {
  google.charts.load('current', { 'packages': ['corechart'] });

// ---------------------------------- Bar Chart.

  var box1 = new Array();
  var box2 = new Array();
  var check = 0
  function makeNewNode(text) {
    newNode = document.createElement("p");
    newNode.innerText = text;
    return newNode;
  }
  test_bar = document.getElementById("test-bar")
  fetch("http://158.108.182.17:2255/get_time_A_yesterday", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  })
    .then((response) => response.json())
    .then((data) => {//*********************** cannot read data ************************* */
        in_1 = data[10].in + data[11].in + data[12].in + data[13].in //จำนวนคนเข้า
        out_1 = data[10].out + data[11].out + data[12].out + data[13].out   // จำนวนคนออก
        in_2 = data[13].in + data[14].in + data[15].in + data[16].in //จำนวนคนเข้า
        out_2 = data[13].out + data[14].out + data[15].out + data[16].out   
        in_3 = data[16].in + data[17].in + data[18].in + data[19].in //จำนวนคนเข้า
        out_3 = data[16].out + data[17].out + data[18].out + data[19].out   
        in_4 = data[19].in + data[20].in + data[21].in
        out_4 = data[19].out + data[20].out + data[21].out
        barchart(in_1, in_2, in_3, in_4, out_1, out_2, out_3, out_4)
        check = in_yes
    });
function barchart(in_1, in_2, in_3, in_4, out_1, out_2, out_3, out_4)
{
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
          { label: "10:00-13:00", y: in_1 },//********************* Enter number of entering people *************************** */
          { label: "13:00-16:00", y: in_2 },
          { label: "16:00-19:00", y: in_3 },
          { label: "19:00-21:00", y: in_4 }
        ]
      },
      {
        type: "column",	
        name: "Exit",
        legendText: "Exit",
        axisYType: "secondary",
        showInLegend: true,
        dataPoints:[
          { label: "10:00-13:00", y: out_1 },//********************* enter number of exiting people *************************** */
          { label: "13:00-16:00", y: out_2 },
          { label: "16:00-19:00", y: out_3 },
          { label: "19:00-21:00", y: out_4 }
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
  }
// ---------------------------------- Pie Chart.

  google.charts.setOnLoadCallback(drawChart2);
  fetch("http://158.108.182.17:2255/get_temp_A")
    .then((response) => response.json())
    .then((data) => {
      pass = data.pass_yesterday
      not_pass = data.not_pass_yesterday
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