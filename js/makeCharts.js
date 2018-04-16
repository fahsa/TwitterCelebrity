function makeChart(file, num, name) {
  const colors = []
  colors.push('rgba(255, 99, 132, 1)')
  colors.push('rgba(54, 162, 235, 1)')
  colors.push('rgba(255, 206, 86, 1)')

  var fs = require("fs");
  var results = fs.readFileSync(file, "utf-8");
  results = results.split("\n")

  var labels = [results[0], results[2], results[4]]

  var datasets = [{
    label: "Probability",
    backgroundColor: colors,
    data: [results[1], results[3], results[5]]
  }]

  console.log(labels)
  console.log(datasets)

  var chart = new Chart($('.chart'+num), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      scales: {
        yAxes: [{
          ticks: {
            beginAtZero: true
          }
        }]
      },
      maintainAspectRatio: false,
      title: {
        display: true,
        text: 'Top 3 Celebrities - '+name,
        fontColor: 'rgb(0, 0, 0)',
        fontSize: 16
      },
      legend: {
        display: false,
        labels: {
          fontColor: 'rgb(0, 0, 0)',
          fontSize: 12
        }
      }
    }
  })
}