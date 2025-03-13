from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="setUser(event)">
            <input type="text" id="usernameText" placeholder="Enter username" autocomplete="off"/>
            <button>Set</button>
        </form>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" placeholder="Enter message" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            let ws;
            function setUser(event) {
                let input = document.getElementById("usernameText")
                ws = new WebSocket(`ws://localhost:8000/ws/${input.value}`);
                ws.onmessage = function(event) {
                    let messages = document.getElementById('messages')
                    let message = document.createElement('li')
                    let content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                console.log(ws)
                if (typeof ws === "undefined") {
                    alert("Username is hot set!!!");
                    return;
                }
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
        self.usernames: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.usernames[websocket] = username

    def disconnect(self, websocket: WebSocket):
        # Remove the WebSocket and its username
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            username = self.usernames.pop(websocket)
            return username

    async def broadcast(self, message: str):
        # Send the message to all active connections
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            # Wait to receive a message from the client
            data = await websocket.receive_text()
            # Prepend the username to the message
            message = f"{username}: {data}"
            # Broadcast the message to all connected clients
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
