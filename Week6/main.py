from fastapi import FastAPI, Path, Query, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates
import mysql.connector
from dotenv import load_dotenv
import os

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

# 載入 .env 變數
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = conn.cursor(dictionary=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_member_username(username):
    query = "SELECT * FROM member WHERE username = %s"
    cursor.execute(query, (username,))
    return cursor.fetchone()

def add_member_username(name, username, password):
    query = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, username, password))
    conn.commit()

def get_message_username_all():
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
    #檢查user id是否存在
    check_query = "SELECT id FROM member WHERE id = %s"
    cursor.execute(check_query, (member_id,))
    result = cursor.fetchone()

    if not result:
        #print("您非本站會員，無法新增")
        return False

    insert_query = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
    cursor.execute(insert_query, (member_id, content))
    conn.commit()
    return True


def delete_message_member_id(member_id, message_id):
    query = "SELECT member_id FROM message WHERE id = %s"
    cursor.execute(query, (message_id,))
    message = cursor.fetchone()

    #非本人操作
    if not message or message["member_id"] != member_id:
        #print("您非本站會員，無法刪除")
        return False

    query = "DELETE FROM message WHERE id = %s"
    cursor.execute(query, (message_id,))
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
    #帳號已被註冊
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

@app.get("/signin")
async def signin_redirect(request: Request):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)
    return RedirectResponse(url="/")

@app.post("/signin")
async def checkAccount(request: Request, account: str = Form(...), password: str = Form(...)):
    user = get_member_username(account)
    if not user:
        return RedirectResponse(url="/error?message=帳號或密碼錯誤", status_code=303)
    if password == user["password"]:
        request.session["signed_in"] = True
        request.session["member_id"] = user["id"]
        request.session["username"] = user["username"]
        return RedirectResponse(url="/member", status_code=303)

    return RedirectResponse(url="/error?message=帳號或密碼錯誤", status_code=303)

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if not request.session.get("signed_in"):
        return RedirectResponse(url="/")
    
    messages = get_message_username_all()
    username = request.session.get("username")
    member_id = request.session.get("member_id")

    return templates.TemplateResponse(
        "member.html",
        {
            "request": request,
            "messages": messages,
            "username": username,
            "member_id": member_id
        }
    )

@app.get("/signin")
async def signin_redirect(request: Request):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)
    return RedirectResponse(url="/")

@app.post("/createMessage")
async def createMessage(request: Request, content: str = Form(...)):
    if not request.session.get("signed_in"):
        return RedirectResponse(url="/")

    member_id = request.session.get("member_id")
    create_message_member_id(member_id, content)

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

@app.get("/deleteMessage")
async def signin_redirect(request: Request):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)
    return RedirectResponse(url="/")

@app.post("/deleteMessage")
async def deleteMessage(request: Request, message_id: int = Form(...)):
    if not request.session.get("signed_in"):
        return RedirectResponse(url="/")

    member_id = request.session.get("member_id")
    success = delete_message_member_id(member_id, message_id)
    if not success:
        return RedirectResponse(url="/error?message=非本人的留言無法刪除", status_code=303)

    return RedirectResponse(url="/member", status_code=303)

@app.get("/signout")
async def signout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")

@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str = "帳號、或密碼輸入錯誤"):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member", status_code=303)
    return templates.TemplateResponse("error.html", {"request": request, "message": message})

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return RedirectResponse(url="/")

#create_message_member_id(9999, 999)
#delete_message_member_id(9999, 999)
