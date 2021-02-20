

let form = document.getElementById("location_input");            // from = id(location_input)

form.addEventListener("submit",(event)=>{              // กด submit ทำ event
    event.preventDefault();
    let sel = document.getElementById("BUTTON_LOCATION");       // สิ่งที่อยู่ใน select ของ BUTTON LOCATION
    let loc = sel.options[sel.selectedIndex].text;                       // ระบุ select
    // sel = select , loc = location

    if(loc==="LOCATION A") {
        var location_name = "A";
        sessionStorage.setItem("location_name", location_name);
        location.href = "../TODAY/today.html";
    }
    else if(loc==="LOCATION B") {
        var location_name = "B";
        sessionStorage.setItem("location_name", location_name);
        location.href = "../TODAY/today.html";
    }
});

function makeNewNode(text) {
    newNode = document.createElement("p");
    newNode.innerText = text;
    return newNode;
  }

// ดึง real-time data
test_bar = document.getElementById("test-bar")
setInterval (() => {
    fetch("http://158.108.182.17:2255/get_dens_A")
        .then((response) => response.json())
        .then((data) => {
        //     datas.forEach(data => {
                people = data.people
                hr = data.hour
                min = data.minute
                dens = data.density
                // getBarData()
                // test_bar.appendChild(makeNewNode(dens))
            })
        .catch((error) => console.log("error", error));
},5000);

// ดึงข้อมูลของ bar graph
function getBarData()
{
    fetch("http://158.108.182.17:2255/get_time_A_yesterday")
      .then((response) => response.json())
      .then((data) => {
          for (var i = 10; i <= 21; i++) {
            in_yes = data[i].in
            out_yes = data[i].out
            // time_range = each.time_range
            // call bar graph function
          }
        });
}

// ดึง ข้อมูลของ piechart
function getPieData()
{
    fetch("http://158.108.182.17:2255/get_temp_A")
      .then((response) => response.json())
      .then((data) => {
            pass = data.pass_yesterday
            not_pass = data.not_pass_yesterday
            // call pie chart function
      });
}

// function getLineData()
// {
//     fetch("https://exceed15.cpsk-club.xyz", {
//         method: "GET",
//         headers: { "Content-Type": "application/json" },
//       })
//       .then((data) => data.json())
//       .then((datas) => {
//         datas.forEach((each) => {
//             amount = each.people
//             real_time = each.real_time
//         });
//     })
// }

// function getStatus()
// {
//     fetch("https://exceed15.cpsk-club.xyz", {
//         method: "GET",
//         headers: { "Content-Type": "application/json" },
//       })
//       .then((data) => data.json())
//       .then((datas) => {
//         datas.forEach((each) => {
//             amount = each.pass
//             real_time = each.not_pass
//         });
//     })
// }

// function getDensity()
// {
//     fetch("https://exceed15.cpsk-club.xyz", {
//         method: "GET",
//         headers: { "Content-Type": "application/json" },
//       })
//       .then((data) => data.json())
//       .then((datas) => {
//         datas.forEach((each) => {
//             amount = each.pass
//             real_time = each.not_pass
//         });
//     })
// }