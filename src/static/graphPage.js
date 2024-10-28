var lineID = new URLSearchParams(window.location.search).get('line')


setupDemoData()
updateGraph()

function updateGraph(){
  var headerText = document.getElementById("TitleText")
  headerText.innerHTML = "Graph Page for line: " + lineID.toString()
}


function setupDemoData(){

  let realData = getAllStationsAvgOverTime(lineID, 554,3600*5,718188)

  let oneStation = realData[1]
  console.log(oneStation)
  timesForX = []
  avgTimeOnY = []

  for(let i = 0; i < oneStation.length; i++){
    //x and y array fill out here with oneStation[i][0] and [1]
    timesForX.push(oneStation[i][0])
    avgTimeOnY.push(oneStation[i][1])
  }

  // Define Data
  const data = [{
    x:timesForX,
    y:avgTimeOnY,
    mode:"scatter",
    line: {color: '#ffffff'}
  }];

  // Define Layout
  const layout = {
    xaxis: {title: "Time"},
    yaxis: {title: "Avg Time (s)"},  
    title: "Avg Cycle time over time",
    plot_bgcolor:"#333333",
    paper_bgcolor:"#333333",
    font: {
      family: 'sans-serif',
      size: 14,
      color: '#cccccc'
    }
  }

  // Display using Plotly
  Plotly.newPlot("myPlot", data, layout);
}
