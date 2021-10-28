var express = require('express')
var app = express()
const port = 3000

// respond with "hello world" when a GET request is made to the homepage
app.get('/line', function (req, res) {
	var sent = false
	res.append('Access-Control-Allow-Origin', ['*']);
    res.append('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.append('Access-Control-Allow-Headers', 'Content-Type');
	const exec = require("child_process").execSync;
    
    var data = exec("python ../python/line.py" + " " + req.query.vx + " " + req.query.vy);
    console.log("Line" + data.toString())
    res.send(data);
})

app.get('/sample', function (req, res) {
	var sent = false
	res.append('Access-Control-Allow-Origin', ['*']);
    res.append('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.append('Access-Control-Allow-Headers', 'Content-Type');
	const exec = require("child_process").execSync;
    
    var data = exec("python ../python/sample_and_hold.py");
    console.log("Sample" + data.toString())
    res.send(data);
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})