from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime
import uuid

app = FastAPI(title="SocialApp", version="1.0")

# ==================== التخزين ====================
users: Dict[str, dict] = {}
posts: List[dict] = []
groups: Dict[str, dict] = {}
stories: List[dict] = []
waiting_rooms: Dict[str, list] = {}
active_connections: Dict[str, List[WebSocket]] = {}

# ==================== النماذج ====================
class UserCreate(BaseModel):
    username: str
    password: str

class PostCreate(BaseModel):
    content: str
    author: str

class CommentCreate(BaseModel):
    content: str
    author: str

class GroupCreate(BaseModel):
    name: str
    creator: str

# ==================== 1. تسجيل الدخول ====================
@app.post("/register")
def register(user: UserCreate):
    if user.username in users:
        raise HTTPException(status_code=400, detail="اسم المستخدم موجود")
    users[user.username] = {
        "username": user.username,
        "password": user.password,
        "is_admin": False,
        "bio": "",
        "joined": datetime.now().isoformat()
    }
    return {"message": "تم التسجيل بنجاح", "username": user.username}

@app.post("/login")
def login(user: UserCreate):
    if user.username not in users or users[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="خطأ في اسم المستخدم أو كلمة المرور")
    return {
        "message": "تم تسجيل الدخول",
        "username": user.username,
        "is_admin": users[user.username]["is_admin"]
    }

@app.get("/profile/{username}")
def get_profile(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    user = users[username]
    return {
        "username": user["username"],
        "bio": user.get("bio", ""),
        "joined": user["joined"],
        "is_admin": user["is_admin"]
    }

# ==================== 2. المنشورات ====================
@app.post("/posts")
def create_post(post: PostCreate):
    if post.author not in users:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    new_post = {
        "id": str(uuid.uuid4()),
        "content": post.content,
        "author": post.author,
        "likes": 0,
        "comments": [],
        "created_at": datetime.now().isoformat()
    }
    posts.insert(0, new_post)  # الأحدث أولاً
    return new_post

@app.get("/posts")
def get_posts():
    return posts

@app.post("/posts/{post_id}/like")
def like_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            post["likes"] += 1
            return {"likes": post["likes"]}
    raise HTTPException(status_code=404, detail="المنشور غير موجود")

@app.post("/posts/{post_id}/comment")
def add_comment(post_id: str, comment: CommentCreate):
    for post in posts:
        if post["id"] == post_id:
            post["comments"].append({
                "author": comment.author,
                "content": comment.content,
                "created_at": datetime.now().isoformat()
            })
            return {"message": "تم إضافة التعليق", "comments_count": len(post["comments"])}
    raise HTTPException(status_code=404, detail="المنشور غير موجود")

# ==================== 3. المجموعات ====================
@app.post("/groups")
def create_group(group: GroupCreate):
    group_id = str(uuid.uuid4())
    groups[group_id] = {
        "id": group_id,
        "name": group.name,
        "creator": group.creator,
        "members": [group.creator],
        "created_at": datetime.now().isoformat()
    }
    return groups[group_id]

@app.get("/groups")
def get_groups():
    return list(groups.values())

@app.post("/groups/{group_id}/join")
def join_group(group_id: str, username: str):
    if group_id not in groups:
        raise HTTPException(status_code=404, detail="المجموعة غير موجودة")
    if username not in groups[group_id]["members"]:
        groups[group_id]["members"].append(username)
    return {"message": "تم الانضمام", "members": groups[group_id]["members"]}

# ==================== 4. القصص ====================
@app.post("/stories")
def create_story(content: str, author: str):
    story = {
        "id": str(uuid.uuid4()),
        "content": content,
        "author": author,
        "created_at": datetime.now().isoformat()
    }
    stories.append(story)
    return story

@app.get("/stories")
def get_stories():
    return stories

# ==================== 5. غرفة الانتظار ====================
@app.post("/waiting-room/{room_id}/join")
def join_waiting_room(room_id: str, username: str):
    if room_id not in waiting_rooms:
        waiting_rooms[room_id] = []
    if username not in waiting_rooms[room_id]:
        waiting_rooms[room_id].append(username)
    return {"waiting": waiting_rooms[room_id]}

@app.get("/waiting-room/{room_id}")
def get_waiting_room(room_id: str):
    return {"users": waiting_rooms.get(room_id, [])}

# ==================== 6. لوحة الآدمن ====================
@app.get("/admin/users")
def admin_get_users():
    return [{"username": u["username"], "is_admin": u["is_admin"]} for u in users.values()]

@app.delete("/admin/posts/{post_id}")
def admin_delete_post(post_id: str):
    global posts
    posts = [p for p in posts if p["id"] != post_id]
    return {"message": "تم حذف المنشور"}

# ==================== 7. الدردشة ====================
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for conn in active_connections[room_id]:
                await conn.send_text(data)
    except WebSocketDisconnect:
        active_connections[room_id].remove(websocket)

# ==================== الصفحة الرئيسية ====================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html dir="rtl">
        <head><title>SocialApp</title></head>
        <body style="font-family: Arial; text-align: center; margin-top: 80px;">
            <h1>مرحباً بك في المنصة</h1>
            <p>استخدم الرابط التالي لتجربة الـ API:</p>
            <a href="/docs" style="font-size: 20px;">/docs</a>
        </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "ok"}
      
