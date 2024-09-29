var oldDataTable = document.getElementById("dataTable")
var avgTimes = getAverageTimes()
var efficiencys = getEfficiency()

onPageLoad()
setInterval(onPageLoad, 1000);

function onPageLoad(){
    var dataTable = document.createElement('table');
    refreshRandomData()
    var partCounts = getPartCounts()
    maxS = 2;
    dataTable.insertRow(0)
    for(let l = 1;l <= 1000;l++){
        let thisLineEff = efficiencys[l]
        let thisLineTimes = avgTimes[l]
        if(thisLineEff != undefined){
            //create a new row in table
            newRow = dataTable.insertRow(dataTable.rows.length);
            newRow.insertCell(0).innerHTML = l
            newRow.insertCell(1).innerHTML = thisLineEff.toFixed(2)
            newRow.insertCell(2).innerHTML = partCounts[l]
            //loop through stations
            //populate row in this section
            for(let s = 1;s!=-1;s++){
                let thisStationTime = avgTimes[l][s]
                //this only works if stations are sequential without breaks
                if(thisStationTime == undefined){
                    break;
                }
                try{
                    newRow.insertCell(s+2).innerHTML = thisStationTime[0].toFixed(2)
                } catch(err){
                    newRow.cells[s+1].innerHTML = 0
                }
                if(s + 2 > maxS){
                    maxS = s + 2
                }
            }
            //write row to table here
        }
        
    }
    firstRow = dataTable.rows[0]
    for(let newS = 0; newS <= maxS; newS++){
        if(newS == 0){
            let newCell = firstRow.insertCell(0)
            newCell.innerHTML = "Line"
        } else if(newS == 1){
            let newCell = firstRow.insertCell(1)
            newCell.innerHTML = "Efficiency (%)"
        }else if(newS == 2){
            let newCell = firstRow.insertCell(2)
            newCell.innerHTML = "Part Count (#)"
        }else{
            let newCell = firstRow.insertCell(newS)
            newCell.innerHTML = "Station " + Number(newS-2).toString() + " (s)"
        }
    }

    oldDataTable.parentNode.replaceChild(dataTable, oldDataTable)
    oldDataTable = dataTable
}

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