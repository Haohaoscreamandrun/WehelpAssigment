import mysql.connector
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(SessionMiddleware,
                   secret_key="APP_AUTHORIZED", max_age=3600)  # 10 mins valid

app.mount("/static", StaticFiles(directory="static"), name='static')
# In FastAPI, the app.mount() function is typically used to mount an ASGI application on a specific path within another ASGI application. However, it seems like you're trying to mount a directory containing static files rather than an ASGI application.


templates = Jinja2Templates(directory='templates')

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request, message: str = None):
    if len(request.session.keys()) == 0:  # switch the flag to False if there's no flag
        request.session.update({"SIGNED-IN": False})

    return templates.TemplateResponse(
        # Declare a Request parameter in the path operation that will return a template.
        request=request,
        name='home.html',
        context={'message': message},
        status_code=200
    )

@app.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(None), account: str = Form(None), password: str = Form(None)):
    username, account, password = (s.strip() for s in (username, account, password))
    print("Form input:",username, account, password)
    # connect to MySQL 'website' database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DBpassword,
        database="website"
    )
    # select the username column and compare to input 
    mycursor = mydb.cursor()
    sql = f'SELECT username FROM member WHERE username = "{username}"'
    print(sql)
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    # condition 1: username exist
    if myresult is not None:
        return RedirectResponse(url="/error/?message=Repeated Username", status_code=303)
    # condition 2: new username, insert into
    else:
        sql = "INSERT INTO member (username, account, password) VALUES (%s, %s ,%s)"
        val = (username, account, password)
        mycursor.execute(sql, val)
        mydb.commit()
        #redirect to homepage with query message
        return RedirectResponse(url="/?message=註冊成功", status_code=303)
        

@app.post("/signin", response_class=HTMLResponse)
async def login(request: Request, account: str = Form(None), password: str = Form(None)):
    account, password = (s.strip() for s in (account, password))
    # connect to MySQL 'website' database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DBpassword,
        database="website"
    )
    mycursor = mydb.cursor()
    # select all account and password
    sql ='SELECT account, password FROM member WHERE account = %s AND password = %s'
    query = (f'{account}', f'{password}',)
    mycursor.execute(sql,query)
    myresult = mycursor.fetchall()
    if not myresult:
        return RedirectResponse(url="/error/?message=Username or password is not correct", status_code=303)
    else:
        for row in myresult:
            member_id, member_username, member_account, member_password = row
    
    

@app.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str):  # message for query parameter
    return templates.TemplateResponse(
        request=request,
        name='error.html',
        # show different message in different situation
        context={"message": message},
        status_code=200
    )


@app.get("/member", response_class=HTMLResponse)
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


@app.get("/signout", response_class=HTMLResponse)
async def logout(request: Request):
    # switch the flag back to red
    request.session.update({"SIGNED-IN": False})
    return RedirectResponse(url="/", status_code=302)

if __name__ == "__main__":
   uvicorn.run("main:app",host = "127.0.0.1", port= 8000, log_level="info")

# load in environment variables in .env
load_dotenv()
DBpassword = os.getenv('password')

# "CREATE TABLE member (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), account VARCHAR(255), password VARCHAR(255))"

