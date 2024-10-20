var lineID = new URLSearchParams(window.location.search).get('line')


setupDemoData()
updateGraph()

function updateGraph(){
  var headerText = document.getElementById("TitleText")
  headerText.innerHTML = "Graph Page for line: " + lineID.toString()
}


function setupDemoData(){

  let realData = getAllStationsAvgOverTime(lineID, 60,3600,3600)

  let oneStation = realData[1]
  console.log(oneStation)

  for(let i = 0; i < oneStation.length; i++){
    //x and y array fill out here with oneStation[i][0] and [1]
  }
  const xArray = [50,60,70,80,90,100,110,120,130,140,150];
  const yArray = [7,8,8,9,9,9,10,11,14,14,15];

  // Define Data
  const data = [{
    x:xArray,
    y:yArray,
    mode:"markers"
  }];

  // Define Layout
  const layout = {
    xaxis: {range: [40, 160], title: "Square Meters"},
    yaxis: {range: [5, 16], title: "Price in Millions"},  
    title: "House Prices vs. Size"
  };

  // Display using Plotly
  Plotly.newPlot("myPlot", data, layout);
}
