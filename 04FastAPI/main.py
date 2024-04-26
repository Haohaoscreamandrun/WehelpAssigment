from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

app.add_middleware(SessionMiddleware,
                   secret_key="APP_AUTHORIZED", max_age=3600)  # 10 mins valid

app.mount("/static", StaticFiles(directory="static"), name='static')

templates = Jinja2Templates(directory='templates')


# By declaring response_class=HTMLResponse the docs UI will be able to know that the response will be HTML.
@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    if len(request.session.keys()) == 0:  # switch the flag to False if there's no flag
        request.session.update({"SIGNED-IN": False})
    return templates.TemplateResponse(
        # Declare a Request parameter in the path operation that will return a template.
        request=request,
        name='login.html',
        status_code=200
    )
# Use the templates you created to render and return a TemplateResponse, pass the name of the template, the request object, and a "context" dictionary with key-value pairs to be used inside of the Jinja2 template.

key = ("test", "test")  # modify the username and password here


@app.post("/signin/", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(None), password: str = Form(None)):
    # Remove leading and trailing whitespace from input(None type don't have .strip())
    username = username.strip() if username is not None else None
    password = password.strip() if password is not None else None
    # Situation 1. User does not type anything or only input whitespace
    if not all((username, password)):
        return RedirectResponse(url="/error/?message=請輸入帳號與密碼", status_code=302)
    # Situation 2. User provide a wrong username or password
    elif (username, password) != key:
        return RedirectResponse(url="/error/?message=帳號或密碼輸入錯誤", status_code=302)
    # Situation 3. User provide the correct key
    else:
        # Upon successful login, set a flag in the session to indicate SIGNED-IN
        request.session.update({"SIGNED-IN": True})
        # 302 is necessary for redirecting
        return RedirectResponse(url="/member/", status_code=302)


@app.get("/error/", response_class=HTMLResponse)
async def error(request: Request, message: str):  # message for query parameter
    return templates.TemplateResponse(
        request=request,
        name='invalid.html',
        # show different message in different situation
        context={"message": message},
        status_code=200
    )


@app.get("/member/", response_class=HTMLResponse)
async def success(request: Request):
    # block any access without green flag
    if not request.session["SIGNED-IN"] == True:
        return RedirectResponse(url="/", status_code=302)
    else:
        return templates.TemplateResponse(
            request=request,
            name='member.html',
            status_code=200
        )


@app.get("/signout/", response_class=HTMLResponse)
async def logout(request: Request):
    # switch the flag back to red
    request.session.update({"SIGNED-IN": False})
    return RedirectResponse(url="/", status_code=302)


# include the positive integer into path parameter
@app.get("/square/{square}", response_class=HTMLResponse)
async def squareCal(square: int, request: Request):
    square_result = square*square
    return templates.TemplateResponse(
        request=request,
        name='square.html',
        context={"square_result": square_result},
        status_code=200
    )
