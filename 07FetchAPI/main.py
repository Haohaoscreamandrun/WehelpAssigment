import mysql.connector
from dotenv import load_dotenv
import os
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from pydantic import BaseModel

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
    elif request.session["SIGNED-IN"] == True:
        return RedirectResponse("/member", status_code=303)
    else:
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
    sql = 'SELECT username FROM member WHERE username = %s'
    val = (username,)
    print(sql)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchone()
    # condition 1: username exist
    if myresult is not None:
        return RedirectResponse(url="/error/?message=Repeated Username", status_code=303)
    # condition 2: new username, insert into
    else:
        sql = "INSERT INTO member (username, account, password) VALUES (%s, %s ,%s)"
        query = (username, account, password)
        mycursor.execute(sql, query)
        mydb.commit()
        #redirect to homepage with query message
        return RedirectResponse(url="/?message=註冊成功，請由下方登入", status_code=303)
        

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
    sql ='SELECT id, username\
        FROM member WHERE account = %s AND password = %s'
    query = (account, password,)
    mycursor.execute(sql,query)
    myresult = mycursor.fetchall()
    if not myresult:
        return RedirectResponse(url="/error/?message=Username or password is not correct", status_code=303)
    else:
        for row in myresult:
            member_id, member_username = row
            # Store sign-in status and credentials into sessionmiddleware
            request.session.update({
                "SIGNED-IN": True,
                "MEMBER_ID": member_id,
                "MEMBER_USERNAME": member_username,
            })
        return RedirectResponse(url="/member", status_code=303)
    
    

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
        return RedirectResponse(url="/?message=請重新登入", status_code=303)
    else:
        #access database and message table
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DBpassword,
            database="website"
        )
        mycursor = mydb.cursor()
        # select all message
        sql = "SELECT \
            message.id AS message,\
            member.username AS member, \
            message.context AS message \
            FROM member \
            INNER JOIN message ON member.id = message.member_id"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        # create structure of template literate
        message = ""
        for m in myresult:
            message += f'<form id="delete-form-{m[0]}" style="display: inline" onsubmit="deleteMessage(event)"> \
                <b>{m[1]}</b> : {m[2]} \
                <input type="hidden" name="message_id" value="{m[0]}">'
            if m[1] == request.session["MEMBER_USERNAME"]:
                message += '<input type="submit" value="x">\
                </form>'
            else:
                message += '</form>'
        # return response
        return templates.TemplateResponse(
            request=request,
            name='member.html',
            context={
                "username": request.session["MEMBER_USERNAME"],
                "message":message},
            status_code=200
        )


@app.get("/signout", response_class=HTMLResponse)
async def logout(request: Request):
    # switch the flag back to red
    request.session.update({"SIGNED-IN": False})
    return RedirectResponse(url="/?message=已成功登出", status_code=302)


@app.post("/createMessage", response_class=HTMLResponse)
async def createMessage(request: Request, message: str = Form(None)):
    message = message.strip()
    if not request.session["SIGNED-IN"] == True:
        return RedirectResponse(url="/?message=登入已過時，請重新登入再嘗試", status_code=303)
    else:
        # connect to MySQL 'website' database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DBpassword,
            database="website"
        )
        mycursor = mydb.cursor()
        # INSERT INTO
        sql = 'INSERT INTO message (member_id, context) VALUES (%s, %s)'
        query = (request.session["MEMBER_ID"], message)
        mycursor.execute(sql, query)
        mydb.commit()
        # redirect to member page
        return RedirectResponse(url="/member", status_code=303)

@app.post("/deleteMessage", response_class=HTMLResponse)
async def deleteMessage(request: Request, message_id: str = Form(None)):
    if not request.session["SIGNED-IN"] == True:
        return RedirectResponse(url="/?message=登入已過時，請重新登入再嘗試", status_code=303)
    else:
        # connect to MySQL 'website' database
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=DBpassword,
            database="website"
        )
        mycursor = mydb.cursor()
        # Delete message by ID
        sql = 'DELETE FROM message WHERE id = %s'
        query = (message_id,)
        mycursor.execute(sql, query)
        mydb.commit()
        return RedirectResponse(url="/member", status_code=303)

# Create nested baseModel for response 
class Member(BaseModel):
    id: int
    username: str
    account: str

class memberItem(BaseModel):
    data: Member | None = None # should be able to respond null

@app.get("/api/member", response_model=memberItem)
def findMember(request: Request, account: str):
    # connect to MySQL 'website' database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DBpassword,
        database="website"
    )
    mycursor = mydb.cursor()
    # Select id, username and account
    sql = "SELECT id, username, account FROM member\
            WHERE account = %s"
    val = (account,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    # create vessel of response
    item = {}
    # Cond1: not logged in
    if len(request.session.keys()) == 0 or request.session["SIGNED-IN"] == False:
        item["data"] = None
    # Cond2: no user data is fetched
    elif not myresult:
        item["data"] = None
    # Cond3: user data found
    else:
        for row in myresult:
            member_id, member_username, member_account = row
            data = {
                "id": member_id,
                "username": member_username,
                "account": member_account
                }
            item["data"] = data
    return item



if __name__ == "__main__":
   uvicorn.run("main:app",host = "127.0.0.1", port= 8000, log_level="info")

# load in environment variables in .env
load_dotenv()
DBpassword = os.getenv('password')

# "CREATE TABLE member (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), account VARCHAR(255), password VARCHAR(255))"

