// ลิ้ง location
let ln =document.getElementById("location_name");
var location_name = sessionStorage.getItem("location_name");
ln.innerText = location_name;
let M2 =document.getElementById("peopleM2");
let MIN =document.getElementById("peopleMIN");


let block1 = document.getElementById("BLOCKS_DENSITY_M2");
let block2 = document.getElementById("BLOCKS_DENSITY_MIN");

setInterval (() => {
    if (location_name==="A"){
        url = "http://158.108.182.17:2255/get_dens_A"
        block_col(url)
    }
    else{
        url = "http://158.108.182.17:2255/get_dens_B"
        block_col(url)
    }
    
},1000);

function makeNewNode(text) {
    newNode = document.createElement("p");
    newNode.innerText = text;
    return newNode;
  }

// test_d = document.getElementById("test")

function block_col(url)
{
    fetch(url)
    .then((response) => response.json())
    .then((data) => {
            people = data.people
            dens = data.density
            test(block1,dens,1);
            // test_d.appendChild(makeNewNode(dens))
            test(block1,dens,1);
            test(block2,people,2);
            M2.innerText = dens;
            MIN.innerText = people;
        })
    .catch((error) => console.log("error", error)); 
}

// เปลี่ยนสี blocks
function test(block,checkQuantity,checkBlock){
    if ( (checkQuantity<=1 && checkBlock===1 ) || (checkQuantity<=49 && checkBlock===2) ) {
        block.style.backgroundColor = "#4dd77f";
    }
    else if ((checkQuantity<=3.6 && checkBlock===1 ) || (checkQuantity<=100 && checkBlock===2)) {
        block.style.backgroundColor = "#f68b39";
    }
    else {
        block.style.backgroundColor = "#f62f2f";
    }
}
test(block1,0,1);
test(block2,0,2);

// load current chart package
google.charts.load("current", {
    packages: ["corechart", "line"]
});
// set callback function when api loaded
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
    // create data object with default value
    let data = google.visualization.arrayToDataTable([
        ["Time", "People"],
        [0, 0]
    ]);
    // create options object with titles, colors, etc.
    let options = {
        title: "Population / Time",
        hAxis: {
            title: "Time"
        },
        vAxis: {
            title: "Number of People"
        }
    };
    // draw chart on load
    let chart = new google.visualization.LineChart(
        document.getElementById("chart_div")
    );
    chart.draw(data, options);
    // interval for adding new data every 250ms
    let index = 0;
    setInterval(function() {
        // instead of this random, you can make an ajax call for the current cpu usage or what ever data you want to display
        // let random = Math.random() * 30 + 20;
        fetch("http://158.108.182.17:2255/get_temp_A", {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        })
            .then((response) => response.json())
            .then((data) => {
            ppp = data.people
            hhh = data.hour
            mmm = data.minute
            });
        data.addRow([index, people]); // Right now cannot display x-axis as current time in string.
        chart.draw(data, options);
        index++;
    }, 5000);
}