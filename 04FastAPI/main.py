from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name= 'static')

templates = Jinja2Templates(directory= 'templates')

@app.get("/", response_class= HTMLResponse)
async def read_item(request: Request):
  return templates.TemplateResponse(
    request = request, name = 'login.html'
  )
# Declare a Request parameter in the path operation that will return a template.
# Use the templates you created to render and return a TemplateResponse, pass the name of the template, the request object, and a "context" dictionary with key-value pairs to be used inside of the Jinja2 template.
# By declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.

@app.post("/signin/")
async def login(account: str= Form(None), pwd: str= Form(None)):
  if account is None or pwd is None or account.strip() == "" or pwd.strip() == "":
    response = RedirectResponse(url="/error/?message=請輸入帳號與密碼", status_code=302)
    return response
  elif account != "test" and pwd != "test":
    response = RedirectResponse(url="/error/?message=帳號或密碼輸入錯誤", status_code=302)
    return response
  elif account == "test" and pwd == "test":
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
  return templates.TemplateResponse(
    request= request,
    name='member.html',
  )
