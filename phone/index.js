const express = require('express');
const { exec } = require('child_process');
const fs = require('fs')
const app = express();

app.get('/index.jpg', (req, res) => {
    console.log("Incoming connection")
    var ts = +new Date();
    exec("termux-camera-photo ./data/" + ts + ".jpg", (error, stdout, stderr) => {
        var readStream = fs.createReadStream('./data/' + ts + ".jpg");
        data = [];
        readStream.on('data', (chunk) => {
            data.push(chunk);
        });
        readStream.on('end', () => {
            res.set('Content-Type', 'image/jpg');
            res.send(Buffer.concat(data));
            console.log("Image sent")
            // end : I am transferring in bytes by bytes called chunk
        });
    });
});

app.listen(3000, () => console.log('Phone server up and running on port 3000'));