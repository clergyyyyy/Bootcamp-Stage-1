from fastapi import FastAPI, Path, Query, Form, Request
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from starlette.templating import Jinja2Templates
app=FastAPI()

# GPT建議 允許 CORS，確保前端可以發送請求
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

#非靜態檔案處理
#一個case寫一個路由x
@app.get("/")
async def home(request: Request):
    if request.session.get("signed_in"):
        return RedirectResponse(url="/member")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/signin")
async def checkAccount(request: Request, account: str = Form(...), password: str = Form(...)):
    if account == "test" and password == "test":
        request.session["signed_in"] = True #SIGNED-IN state to TRUE 
        return RedirectResponse(url="/member", status_code=303)
    return RedirectResponse(url="/error?message=帳號、或密碼錯誤", status_code=303)

@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    if not request.session.get("signed_in"):
        return RedirectResponse(url="/") #SIGNED-IN not true redirect 
    return templates.TemplateResponse("member.html", {"request": request})

@app.get("/signout")
async def signout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")

@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message:str = "帳號、或密碼輸入錯誤"):
    return templates.TemplateResponse(
        "error.html", {"request": request, "message": message}
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return RedirectResponse(url="/")