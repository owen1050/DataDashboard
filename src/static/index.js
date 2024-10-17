var oldDataTable = document.getElementById("dataTable")
var avgTimes = getAverageTimes()
var efficiencys = getEfficiency()

onPageLoad()
//setInterval(onPageLoad, 1000);

function onPageLoad(){
    var dataTable = document.createElement('table');
    maxS = 2;
    dataTable.insertRow(0)

    for(let l = 1;l <= 100;l++){
        let thisLineTimes = avgTimes[l]
        console.log(thisLineTimes)
        if(thisLineTimes != undefined){
            //create a new row in table
            newRow = dataTable.insertRow(dataTable.rows.length);
            newRow.insertCell(0).innerHTML = l

            numStation =  Object.keys(avgTimes[l]).length
            console.log(numStation)
            //loop through stations
            //populate row in this section
            goodCount = 0
            for(let s = 1;s<50 && goodCount<numStation;s++){
                let thisStationTime = avgTimes[l][s]
                //console.log(l, s, thisStationTime  )
                //this only works if stations are sequential without breaks
                if(thisStationTime != undefined){
                    goodCount = goodCount + 1
                    newRow.insertCell(s).innerHTML = thisStationTime.toFixed(2)
                    if(s > maxS){
                        maxS = s
                    }
                } else {
                    newRow.insertCell(s).innerHTML = ''
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
        }else{
            let newCell = firstRow.insertCell(newS)
            newCell.innerHTML = "Station " + Number(newS).toString()
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