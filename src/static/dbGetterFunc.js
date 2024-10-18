function getAverageTimes(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url_g + "/api/getAverageTimes", false);
    xhr.send();
    const data = xhr.response;
    //console.log(data);
    ret = JSON.parse(data);
    return ret
}

function getEfficiency(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url_g + "/api/getEfficiency", false);
    xhr.send();
    const data = xhr.response;
    //console.log(data);
    ret = JSON.parse(data);
    return ret
}

function getPartCounts(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url_g + "/api/getPartCounts", false);
    xhr.send();
    const data = xhr.response;
    //console.log(data);
    ret = JSON.parse(data);
    return ret
}

function refreshDBData(){
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url_g + "/api/regenData", false);
    xhr.send();
    return ret
}

function refreshRandomData(){
    refreshDBData()
    avgTimes = getAverageTimes()
    efficiencys = getEfficiency()

}