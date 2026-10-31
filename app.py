from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List
import json

app = FastAPI(title="SocialApp", description="دردشة + مكالمات فيديو (نسخة أولية)")

# مدير الاتصالات
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# صفحة الدردشة
html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>دردشة فورية</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; background: #f0f2f5; }
        #messages { list-style: none; padding: 10px; height: 400px; overflow-y: auto; background: white; border-radius: 10px; }
        #messages li { padding: 8px; margin: 5px 0; background: #e4e6eb; border-radius: 8px; }
        form { margin-top: 15px; display: flex; gap: 10px; }
        input { flex: 1; padding: 10px; border-radius: 20px; border: 1px solid #ccc; }
        button { padding: 10px 20px; border-radius: 20px; background: #1877f2; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h2>دردشة فورية</h2>
    <ul id="messages"></ul>
    <form onsubmit="sendMessage(event)">
        <input type="text" id="messageText" placeholder="اكتب رسالة..." autocomplete="off" required>
        <button type="submit">إرسال</button>
    </form>

    <script>
        const ws = new WebSocket(`ws://${location.host}/ws`);
        const messages = document.getElementById("messages");

        ws.onmessage = (event) => {
            const li = document.createElement("li");
            li.textContent = event.data;
            messages.appendChild(li);
            messages.scrollTop = messages.scrollHeight;
        };

        function sendMessage(event) {
            event.preventDefault();
            const input = document.getElementById("messageText");
            if (input.value.trim()) {
                ws.send(input.value);
                input.value = "";
            }
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
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("شخص غادر الدردشة")

@app.get("/health")
def health():
    return {"status": "ok"}
