// ลิ้ง location
let ln =document.getElementById("location_name");
var location_name = sessionStorage.getItem("location_name");
ln.innerText = location_name;


window.onload = function(){
    var pass = null
    var not_pass = null
    var in_avg = 0
    var out_avg = 0
    var time_range = 
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart1);
    fetch("https://exceed15.cpsk-club.xyz", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      })
      .then((data) => data.json())
      .then((datas) => {
        datas.forEach((each) => {
            in_avg = each.in_avg
            out_avg = each.out_avg
            time_range = each.time_range
            // call bar graph function
        });
    });
    function drawChart1() {

    var data1 = google.visualization.arrayToDataTable([
    ['Numbers', 'Category', { role: 'style' }],
    ['A', in_avg, '#5382bc'],
    ['B', out_avg, '#5382bc'],
    ['C', time_range, '#5382bc']
    ]);

    var options1 = {
    legend: { position: 'bottom', textStyle: {fontSize: 16}, },
    backgroundColor: "#faf3e3",
    title: 'Bar Chart',
    fontSize: 30,
    fontFamily: "Nanum Gothic Coding",
    colors: ['#5382bc']
    };

    var chart1 = new google.visualization.BarChart(document.getElementById("abc"))

    chart1.draw(data1, options1);
    }
    
    google.charts.load('visualization', '1', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart2);
    fetch("http://158.108.182.17:2255/get_temp_A", {
        method: "GET",
        headers: { "Content-Type": "application/json" },
      })
      .then((response) => response.json())
      .then((data) => {
            pass = data.pass
            not_pass = data.not_pass
            // call pie chart function
      });

    function drawChart2() {

    var data2 = google.visualization.arrayToDataTable([
    ['Category', 'Percentage'],
    ['PASS', pass],
    ['NOT PASS', not_pass]
    ]);

    var options2 = {
    // pieSliceBorderColor: '#000',
    legend: { position: 'bottom', textStyle: {fontSize: 25}, },
    backgroundColor: "#e9d5ae",
    title: 'Percentage',
    fontSize: 30,
    fontName: 'Nanum Gothic Coding',
    slices: [{color: '#4dd77f',offset:0},{color: '#f62f2f',offset:0.1}]
    };

    var chart2 = new google.visualization.PieChart(document.getElementById('piechart'));

    chart2.draw(data2, options2);
    }
}