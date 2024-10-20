var lineID = new URLSearchParams(window.location.search).get('line')


setupDemoData()
updateGraph()

function updateGraph(){
  var headerText = document.getElementById("TitleText")
  headerText.innerHTML = "Graph Page for line: " + lineID.toString()
}


function setupDemoData(){

  let realData = getAllStationsAvgOverTime(lineID, 600,3600,3600*4)

  let oneStation = realData[1]
  console.log(oneStation)
  timesForX = []
  avgTimeOnY = []

  for(let i = 0; i < oneStation.length; i++){
    //x and y array fill out here with oneStation[i][0] and [1]
    timesForX.push(oneStation[i][0])
    avgTimeOnY.push(oneStation[i][1])
  }
  const xArray = [50,60,70,80,90,100,110,120,130,140,150];
  const yArray = [7,8,8,9,9,9,10,11,14,14,15];

  // Define Data
  const data = [{
    x:timesForX,
    y:avgTimeOnY,
    mode:"scatter"
  }];

  // Define Layout
  const layout = {
    xaxis: {title: "Time"},
    yaxis: {title: "Avg Time (s)"},  
    title: "Avg Cycle time over time"
  };

  // Display using Plotly
  Plotly.newPlot("myPlot", data, layout);
}
