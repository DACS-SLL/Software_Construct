var express = require('express');
var app = express();
var fs = require("fs");
var bodyParser = require('body-parser');
var multer = require('multer');

app.use(express.static('public'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(multer({dest:'./tmp/'}).single('photo'));

if (!fs.existsSync('./uploads')) {
    fs.mkdirSync('./uploads');
}

app.post('/api/operations', (req, res) => {
    const { num1, num2 } = req.body;
    
    if (typeof num1 !== 'number' || typeof num2 !== 'number') {
        return res.status(400).json({ error: 'Both parameters must be numbers' });
    }

    if (num2 === 0) {
        return res.status(400).json({ error: 'Division by zero is not allowed' });
    }

    const result = {
        suma: num1 + num2,
        resta: num1 - num2,
        multiplicacion: num1 * num2,
        division: num1 / num2
    };

    res.json(result);
});

app.post('/api/register-user', (req, res) => {
    const { name, lastname, age, height, weight } = req.body;
    
    if (!name || !lastname || !age || !height || !weight) {
        return res.status(400).json({ result: false, msg: "ERROR: Missing required fields" });
    }

    const userData = `Nombre: ${name}\nApellido: ${lastname}\nEdad: ${age}\nAltura: ${height}\nPeso: ${weight}\n\n`;
    const filename = `user_${Date.now()}.txt`;

    fs.writeFile(`./uploads/${filename}`, userData, (err) => {
        if (err) {
            console.error(err);
            return res.json({ result: false, msg: "ERROR: Could not save file" });
        }
        res.json({ result: true, msg: "OK", filename: filename });
    });
});

app.post('/file_upload', function (req, res) {
    console.log(req.file);
    
    var file = __dirname + "/uploads/" + req.file.originalname;
    console.log(file);
    
    fs.readFile(req.file.path, function (err, data) {
        if (err) {
            console.log(err);
            return res.json({ error: err });
        }
        
        fs.writeFile(file, data, function (err) {
            let response;
            if (err) {
                console.log(err);
                response = { error: err };
            } else {
                response = {
                    message: 'File uploaded successfully',
                    filename: file
                };
            }
            res.json(response);
        });
    });
});

app.get('/index.html', function (req, res) {
    res.sendFile( __dirname + "/" + "index.html" );
})

var server = app.listen(8081, function () {
    var host = server.address().address;
    var port = server.address().port;
    
    console.log("Server listening at http://%s:%s", host, port);
});