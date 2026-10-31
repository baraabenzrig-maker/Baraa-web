from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

# مدير الاتصالات (مهم للدردشة الجماعية)
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# صفحة HTML بسيطة للدردشة
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>دردشة فورية</title>
        <style>
            body { font-family: Arial; max-width: 600px; margin: 50px auto; }
            #messages { list-style: none; padding: 0; height: 300px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; }
            input { width: 70%; padding: 8px; }
            button { padding: 8px 15px; }
        </style>
    </head>
    <body>
        <h1>دردشة فورية (مثل واتساب)</h1>
        <ul id="messages"></ul>
        <form onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off" placeholder="اكتب رسالة..."/>
            <button>إرسال</button>
        </form>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                message.textContent = event.data
                messages.appendChild(message)
            };
            function sendMessage(event) {
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

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"شخص قال: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("شخص غادر الدردشة")
