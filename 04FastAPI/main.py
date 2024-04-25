from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="APP_AUTHORIZED", max_age= 3600)

app.mount("/static", StaticFiles(directory="static"), name= 'static')

templates = Jinja2Templates(directory= 'templates')


@app.get("/", response_class= HTMLResponse)
async def read_item(request: Request):
  if len(request.session.keys()) == 0:
    request.session.update({"SIGNED-IN": False})
  return templates.TemplateResponse(
    request = request, name = 'login.html'
  )
# Declare a Request parameter in the path operation that will return a template.
# Use the templates you created to render and return a TemplateResponse, pass the name of the template, the request object, and a "context" dictionary with key-value pairs to be used inside of the Jinja2 template.
# By declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.


@app.post("/signin/", response_class=HTMLResponse)
async def login(request: Request, account: str= Form(None), pwd: str= Form(None)):
  if account is None or pwd is None or account.strip() == "" or pwd.strip() == "":
    response = RedirectResponse(url="/error/?message=請輸入帳號與密碼", status_code=302)
    return response
  elif account != "test" and pwd != "test":
    response = RedirectResponse(url="/error/?message=帳號或密碼輸入錯誤", status_code=302)
    return response
  elif account == "test" and pwd == "test":
    # Upon successful login, set a flag in the session to indicate SIGNED-IN
    request.session.update({"SIGNED-IN": True})
    response = RedirectResponse(url="/member/", status_code=302) #302 is necessary for redirecting
    return response


@app.get("/error/", response_class=HTMLResponse)
async def error(request: Request, message: str):
  return templates.TemplateResponse(
    request= request,
    name = 'invalid.html',
    context = {"message": message}
  )


@app.get("/member/", response_class=HTMLResponse)
async def success(request: Request):
  if not request.session["SIGNED-IN"] == True:
    response = RedirectResponse(url= "/", status_code= 302)
    return response
  else:
    return templates.TemplateResponse(
    request= request,
    name='member.html',
  )

@app.get("/signout/", response_class=HTMLResponse)
async def logout(request: Request):
  request.session.update({"SIGNED-IN": False})
  response = RedirectResponse(url="/", status_code=302)
  return response

@app.get("/square/{square}", response_class=HTMLResponse)
async def squareCal(square: int, request: Request):
  square_result = square*square
  return templates.TemplateResponse(
    request= request,
    name= 'square.html',
    context={"square_result": square_result}
  )