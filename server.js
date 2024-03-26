const express = require("express")
const path = require("path")
const cors = require("cors")
const bodyParser = require("body-parser")

const app = express();
app.use(bodyParser.json())
app.use(cors())
const port = 3001;

const frontendpath = path.join(__dirname, '../enigmafrontend/app/page.jsx')

const data = [
    {
        data1: "this is data 1",
        data2: "this is data 2",
    },{
        data1: "this is data 1",
        data2: "this is data 2",
    },{
        data1: "this is data 1",
        data2: "this is data 2",
    },{
        data1: "this is data 1",
        data2: "this is data 2",
    }
] 

app.get("/api/data", (req,res)=>{
    res.send(data) 
})

app.post("/api/getdata", (req, res)=>{

    let recievedData = req.body;

    console.log(recievedData);

    res.status(200).json({message: "status 200 aaya hai"})

    res.send("okay data has been recieved on the server")
})

app.get("/", (req,res)=>{
    res.send("this server is working") 
})

app.listen(port, ()=>{
    console.log("server is runnning at port: " +  `${port}`)
})