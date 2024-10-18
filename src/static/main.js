var oldDataTable = document.getElementById("dataTable")
var avgTimes = getAverageTimes()
var efficiencys = getEfficiency()
var partCounts = getPartCounts()

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
            newRow.insertCell(1).innerHTML = efficiencys[l].toFixed(2) + "%"
            newRow.insertCell(2).innerHTML = partCounts[l].toFixed(0)

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
                    newRow.insertCell(s+2).innerHTML = thisStationTime.toFixed(2)
                    if(s > maxS){
                        maxS = s
                    }
                } else {
                    newRow.insertCell(s+2).innerHTML = ''
              }
                
            }
            //write row to table here
        }
        
    }
    firstRow = dataTable.rows[0]
    for(let newS = 0; newS <= maxS+2; newS++){
        if(newS == 0){
            let newCell = firstRow.insertCell(0)
            newCell.innerHTML = "Line"
        }
        else{ if(newS == 1){
            let newCell = firstRow.insertCell(1)
            newCell.innerHTML = "Efficiency"
            }else if(newS == 2){
                let newCell = firstRow.insertCell(2)
                newCell.innerHTML = "Part Count"
            }else{
                let newCell = firstRow.insertCell(newS)
                newCell.innerHTML = "Station " + Number(newS-2).toString()
            }
        }
    }

    oldDataTable.parentNode.replaceChild(dataTable, oldDataTable)
    oldDataTable = dataTable
}

