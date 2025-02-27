from fastapi import FastAPI, Path, Query, Form, Request, Body
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates
import mysql.connector
from dotenv import load_dotenv
import os

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_member_username(username):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = "SELECT * FROM member WHERE username = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone()

def add_member_username(name, username, password):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (name, username, password))
            conn.commit()

def update_member_username(name, username):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = "UPDATE member SET name = %s WHERE username = %s;"
            cursor.execute(query, (name, username))
            conn.commit()


def get_message_username_all():
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = """
            SELECT message.id, member.name AS sender_name, message.member_id,
                   message.content, message.like_count, message.time
            FROM message
            INNER JOIN member ON message.member_id = member.id
            ORDER BY message.time DESC;
            """
            cursor.execute(query)
            return cursor.fetchall()

def create_message_member_id(member_id, content):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            # 檢查 user id 是否存在
            cursor.execute("SELECT id FROM member WHERE id = %s", (member_id,))
            if not cursor.fetchone():
                return False

            cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (member_id, content))
            conn.commit()
            return True

def delete_message_member_id(member_id, message_id):
    with mysql.connector.connect(**DB_CONFIG) as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT member_id FROM message WHERE id = %s", (message_id,))
            message = cursor.fetchone()

            if not message or message["member_id"] != member_id:
                return False

            cursor.execute("DELETE FROM message WHERE id = %s", (message_id,))
            conn.commit()
            return True

@app.get("/")
async def home(request: Request):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signup")
async def signup_redirect(request: Request):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)
    return RedirectResponse(url="/")

@app.post("/signup")
async def addAccount(request: Request, name: str = Form(...), account: str = Form(...), password: str = Form(...)):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)

    user = get_member_username(account)
    if user:
        return RedirectResponse(url="/error?message=帳號已經被註冊", status_code=303)
    
    add_member_username(name, account, password)
    return HTMLResponse(
        """
        <script>
            alert("註冊成功！");
            setTimeout(function() {
                window.location.href = "/";
            }, 500);
        </script>
        """,
        status_code=200
    )

@app.post("/signin")
async def checkAccount(request: Request, account: str = Form(...), password: str = Form(...)):
    user = get_member_username(account)
    if not user or password != user["password"]:
        return RedirectResponse(url="/error?message=帳號或密碼錯誤", status_code=303)

    request.session["signed_in"] = True
    request.session["member_id"] = user["id"]
    request.session["username"] = user["username"]
    return RedirectResponse(url="/member", status_code=303)

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if not request.session.get("signed_in"):
        return RedirectResponse(url="/")

    messages = get_message_username_all()
    return templates.TemplateResponse(
        "member.html",
        {
            "request": request,
            "messages": messages,
            "username": request.session.get("username"),
            "member_id": request.session.get("member_id")
        }
    )


@app.get("/api/member")
async def get_member(request: Request, username: str = Query(None)):
    if not request.session.get("signed_in"):
        return JSONResponse(content={"data": None}, status_code=200)

    if not username:
        return JSONResponse(content={"data": None}, status_code=200)

    user = get_member_username(username)
    if user:
        return JSONResponse(content={"data": {
            "id": user["id"],
            "name": user["name"],
            "username": user["username"]
        }}, status_code=200)

    return JSONResponse(content={"data": None}, status_code=200)

@app.patch("/api/member")
async def update_member(request: Request, data: dict = Body(...)):
    if not request.session.get("signed_in"):
        return JSONResponse(content={"ok": False}, status_code=401)

    name = data.get("name")
    if not name:
        return JSONResponse(content={"ok": False}, status_code=400)

    username = request.session.get("username")
    update_member_username(name, username)

    return JSONResponse(content={"name": name, "ok": True}, status_code=200)


@app.post("/createMessage")
async def createMessage(request: Request, content: str = Form(...)):
    if not request.session.get("signed_in"):
        return RedirectResponse(url="/")

    member_id = request.session.get("member_id")
    if not create_message_member_id(member_id, content):
        return RedirectResponse(url="/error?message=無法發送留言", status_code=303)

    return HTMLResponse(
        """
        <script>
            alert("新增留言成功！");
            setTimeout(function() {
                window.location.href = "/member";
            }, 500);
        </script>
        """,
        status_code=200
    )

@app.post("/deleteMessage")
async def deleteMessage(request: Request, message_id: int = Form(...)):
    if not request.session.get("signed_in"):
        return RedirectResponse(url="/")

    member_id = request.session.get("member_id")
    if not delete_message_member_id(member_id, message_id):
        return RedirectResponse(url="/error?message=非本人的留言無法刪除", status_code=303)

    return RedirectResponse(url="/member", status_code=303)

@app.get("/signout")
async def signout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")

@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str = "帳號或密碼輸入錯誤"):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return RedirectResponse(url="/")


#create_message_member_id(9999, 999)
#delete_message_member_id(9999, 999)
