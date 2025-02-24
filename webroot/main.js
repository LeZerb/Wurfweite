var counter = 0;

function cycle() {
    var httpRequest = new XMLHttpRequest();
    httpRequest.open("GET", "http://" + location.hostname + ":55556", false); // false for synchronous request
    httpRequest.send();
    var result = JSON.parse(httpRequest.responseText);
    console.log(result)

    if (result.hasOwnProperty("NEXTATHLETE") || result.hasOwnProperty("MEASURED")) {
        var athlete;

        if (result.hasOwnProperty("NEXTATHLETE")) {
            athlete = result.NEXTATHLETE[0];
            document.getElementById("Distance").innerHTML = "-";
        }
        else {
            athlete = result.MEASURED[0];
            document.getElementById("Distance").innerHTML = athlete.DISTANCE;
        }

        document.getElementById("Athlete").innerHTML = athlete.NAME + ", " + athlete.VNAME;
        document.getElementById("Background").innerHTML = athlete.CLUB;
        document.getElementById("Attempt").innerHTML = athlete.ATTEMPT;
        document.getElementById("Rank").innerHTML = athlete.RANK;
    }
}

function init() {
    setInterval(cycle, 1000);
}
