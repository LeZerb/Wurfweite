var counter = 0;

function cycle() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.open("GET", "http://" + location.hostname + ":55556", false); // false for synchronous request
    httpRequest.send();
    var result = JSON.parse(httpRequest.responseText);
    console.log(result)

    if (result.JIDS.includes("WMTNX")) {
        document.getElementById("Athlete").innerHTML = result.NEXTATHLETE[0].NAME + ", " + result.NEXTATHLETE[0].VNAME;
        document.getElementById("Background").innerHTML = result.NEXTATHLETE[0].CLUB;
        document.getElementById("Attempt").innerHTML = result.NEXTATHLETE[0].ATTEMPT;
        document.getElementById("Rank").innerHTML = result.NEXTATHLETE[0].RANK;
        document.getElementById("Distance").innerHTML = "-";
    }
    else if (result.JIDS.includes("WMTMS")) {
        document.getElementById("Athlete").innerHTML = result.MEASURED[0].NAME + ", " + result.MEASURED[0].VNAME;
        document.getElementById("Background").innerHTML = result.MEASURED[0].CLUB;
        document.getElementById("Attempt").innerHTML = result.MEASURED[0].ATTEMPT;
        document.getElementById("Rank").innerHTML = result.MEASURED[0].RANK;
        document.getElementById("Distance").innerHTML = result.MEASURED[0].DISTANCE;
    }
}

function init() {
    setInterval(cycle, 1000);
}
