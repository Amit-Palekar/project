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

app.get('/graph1', function (req, res) {
	var sent = false
	res.append('Access-Control-Allow-Origin', ['*']);
    res.append('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.append('Access-Control-Allow-Headers', 'Content-Type');
	const exec = require("child_process").execSync;
    
    var arr = JSON.parse(req.query.params);
    console.log(arr);
    var data = exec("python ../python/graph1.py"+ " " + arr.join(" "));
    console.log("Sample" + data.toString())
    res.send(data);
})

app.get('/graph3', function (req, res) {
	var sent = false
	res.append('Access-Control-Allow-Origin', ['*']);
    res.append('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.append('Access-Control-Allow-Headers', 'Content-Type');
	const exec = require("child_process").execSync;
    
    var arr = JSON.parse(req.query.params);
    console.log(arr);
    var data = exec("python3 ../python/graph3.py"+ " " + arr.join(" "));
    // console.log("Sample" + data.toString())
    res.send(data);
})

app.get('/graph4', function (req, res) {
	var sent = false
	res.append('Access-Control-Allow-Origin', ['*']);
    res.append('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.append('Access-Control-Allow-Headers', 'Content-Type');
	const exec = require("child_process").execSync;
    
    var arr = JSON.parse(req.query.params);
    console.log(arr);
    var data = exec("python3 ../python/graph4.py"+ " " + arr.join(" "));
    // console.log("Sample" + data.toString())
    res.send(data);
})

app.get('/graph5', function (req, res) {
	res.append('Access-Control-Allow-Origin', ['*']);
    res.append('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.append('Access-Control-Allow-Headers', 'Content-Type');
	const exec = require("child_process").execSync;
    
    var arr = JSON.parse(req.query.params);
    console.log(arr);
    var data = exec("python3 ../python/graph5.py"+ " " + arr.join(" "));
    // console.log("Sample" + data.toString())
    res.send(data);
})

app.get('/graph6', function (req, res) {
	res.append('Access-Control-Allow-Origin', ['*']);
    res.append('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE');
    res.append('Access-Control-Allow-Headers', 'Content-Type');
	const exec = require("child_process").execSync;
    
    var arr = JSON.parse(req.query.params);
    console.log(arr);
    var data = exec("python3 ../python/graph6.py"+ " " + arr.join(" "));
    // console.log("Sample" + data.toString())
    res.send(data);
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})