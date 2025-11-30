const express = require('express');
const fetch = require('node-fetch');
const path = require('path');
const app = express();
const WebSocket = require("ws");

app.use((req, res, next) => {
    console.log(`API CALLED: ${req.method} ${req.url} ${res.statusCode}`);
    next();
});

// Serve static files from Frontend folder
app.use(express.static(path.join(__dirname, "../Frontend")));

// JSON parser
app.use(express.json());

// Serve index.html at root
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, "../Frontend/index.html"));
});

// POST endpoint
app.post('/api/reservation', (req, res) => {
    console.log("received json file", req.body);
    res.status(200).json({ status: "ok" });
});




// WebSocket server
const wss = new WebSocket.Server({ port: 3031 });
wss.on('connection', ws => {
    console.log('Client connected');
    ws.send("Welcome Python client!");
    ws.on('message', message => {
        console.log('Received:', message.toString());
        ws.send(`Server echo: ${message}`);
    });

    ws.on('close', () => console.log('Client disconnected'));
});

// HTTP listener
app.listen(3001, 'localhost', () => {
    console.log('Server běží na http://localhost:3001');
});
