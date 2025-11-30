const express = require('express');
const fetch = require('node-fetch');
const path = require('path');
const app = express();
const WebSocket = require("ws");
const wss = new WebSocket.Server({ port: 3031 });
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

wss.on('connection', ws => {
    console.log('Client connected');

    // Poslat uvítací zprávu
    ws.send(JSON.stringify({ message: "Welcome Python client!" }));

    // Zachytávání zpráv od klienta
    ws.on('message', message => {
        let data;
        try {
            // Pokud posíláš JSON, parse
            data = JSON.parse(message);
        } catch (err) {
            console.warn("Non-JSON message received:", message);
            data = { raw: message.toString() };
        }

        console.log("Received from client:", data);

        // Echo zpět klientovi
        ws.send(JSON.stringify({ echo: data }));
    });

    ws.on('close', () => console.log('Client disconnected'));
});

app.post('/api/reservation', (req, res) => {
    console.log("received json file", req.body);
    res.status(200).json({ status: "ok" });

    // Odeslání každému připojenému klientovi
    wss.clients.forEach(client => {
        if (client.readyState === WebSocket.OPEN) {
            try {
                client.send(JSON.stringify(req.body));
            } catch (err) {
                console.error("Failed to send to client:", err);
            }
        }
    });
});


// HTTP listener
app.listen(3001, 'localhost', () => {
    console.log('Server běží na http://localhost:3001');
});
