// ลิ้ง location
let ln =document.getElementById("location_name");
var location_name = sessionStorage.getItem("location_name");
ln.innerText = location_name;


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

test_d = document.getElementById("test")

function block_col(url)
{
    fetch(url)
    .then((response) => response.json())
    .then((data) => {
            people = data.people
            dens = data.density
            test_d.appendChild(makeNewNode(dens))
            test(block1,people,1);
            test(block2,people,2);
        })
    .catch((error) => console.log("error", error)); 
}

// เปลี่ยนสี blocks
function test(block,checkQuantity,checkBlock){
    if ( (checkQuantity<=10 && checkBlock===1 ) || (checkQuantity<=49 && checkBlock===2) ) {
        block.style.backgroundColor = "#4dd77f";
    }
    else if ((checkQuantity<=36 && checkBlock===1 ) || (checkQuantity<=100 && checkBlock===2)) {
        block.style.backgroundColor = "#f68b39";
    }
    else {
        block.style.backgroundColor = "#f62f2f";
    }
}

test(block1,0,1);
test(block2,0,2);