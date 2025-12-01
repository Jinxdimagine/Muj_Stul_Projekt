const express = require('express');
const path = require('path');
const app = express();
const WebSocket = require("ws");
const fs = require("fs");
const http = require('http');
const dsPath = path.join(__dirname, 'ds_server.json');
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });
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
    const reservations=send_saved_reservations()
    // Poslat uvítací zprávu
    ws.send(JSON.stringify({ message: "Welcome Python client!" }));
    reservations.forEach(res => ws.send(JSON.stringify(res)));
    clear();
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
    console.log(wss.clients.size)
    if (wss.clients.size !== 0) {
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
    }else{
        const newReservation = req.body;
        save_reservation(newReservation)
    }
});

function send_saved_reservations(){
    let data = [];
    try {
        const jsonString = fs.readFileSync(dsPath, "utf8");
        if (jsonString) {
            data = JSON.parse(jsonString);
        }
    } catch (err) {
        console.error("Error reading file:", err);
    }
    return data
}
function save_reservation(newReservation){
    let data = [];
    try {
        const jsonString = fs.readFileSync(dsPath, "utf8");
        if (jsonString) {
            data = JSON.parse(jsonString);
        }
    } catch (err) {
        console.error("Error reading file:", err);
    }
    data.push(newReservation)
    fs.writeFileSync(dsPath, JSON.stringify(data, null, 4));
}
function clear(){
    fs.writeFileSync(dsPath, JSON.stringify([], null, 4));

}

// HTTP listener
const PORT = process.env.PORT || 3001;
server.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});