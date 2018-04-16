function run() {
  var username = $("#nme").val(); 
  console.log(username);     
  const spawn = require('child_process').spawn;
  const scriptExecution = spawn("python3", ["main.py"]);

  // Handle normal output
  scriptExecution.stdout.on('data', (data) => {
    console.log(String.fromCharCode.apply(null, data));
  });

  // Write data (remember to send only strings or numbers, otherwhise python wont understand)
  var data = JSON.stringify(username);
  scriptExecution.stdin.write(data);

  // End data write
  scriptExecution.stdin.end();

  //window.resizeTo(1000, 1000);
  $(".data").hide();
  $("#wait").show();
  setTimeout(makeAllCharts, 20000);
}

function back() {
  const spawn = require('child_process').spawn;
  const scriptExecution = spawn("python3", ["reset.py"]);

  // Handle normal output
  scriptExecution.stdout.on('data', (data) => {
    console.log(String.fromCharCode.apply(null, data));
  });

  window.resizeTo(579, 305);
  $(".data").show();
  $(".container-fluid").hide();
  $("#back").hide();
  $("#nme").val("");
  $(document.body).css("margin", "8% auto 0 auto")
  $("#celebTweet").html("CeleberTweet");
}

function makeAllCharts() {
  $("#wait").hide();
  $(".container-fluid").show();
  $("#back").show();
  $(document.body).css("margin", "1% auto 0 auto")

  $(document.html).scrollTop = $(document.html).scrollHeight;

  var username = $("#nme").val();

  $("#celebTweet").html("CeleberTweet (@"+username+")");

  var files = ["./nn_output", "./rocchio.out", "./char_output", "./word_output"]
  var names = ["Neural Network", "Rocchio", "Bigram (Character)", "Bigram (Word)"]

  for (var i = 0; i < 4; i++) {
    makeChart(files[i], i+1, names[i]);
  }
}