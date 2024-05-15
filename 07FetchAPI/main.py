import mysql.connector
from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Request, Form, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from pydantic import BaseModel
from typing import Annotated, Optional

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
async def signup(request: Request, name: str = Form(None), username: str = Form(None), password: str = Form(None)):
    name, username, password = (s.strip() for s in (name, username, password))
    # connect to MySQL 'website' database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DBpassword,
        database="website"
    )
    # select the name column and compare to input 
    mycursor = mydb.cursor()
    sql = 'SELECT username FROM member WHERE username = %s'
    val = (username,)
    mycursor.execute(sql,val)
    myresult = mycursor.fetchone()
    # condition 1: name exist
    if myresult is not None:
        return RedirectResponse(url="/error/?message=Repeated Username", status_code=303)
    # condition 2: new name, insert into
    else:
        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s ,%s)"
        query = (name, username, password)
        mycursor.execute(sql, query)
        mydb.commit()
        #redirect to homepage with query message
        return RedirectResponse(url="/?message=註冊成功，請由下方登入", status_code=303)
        

@app.post("/signin", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(None), password: str = Form(None)):
    username, password = (s.strip() for s in (username, password))
    # connect to MySQL 'website' database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DBpassword,
        database="website"
    )
    mycursor = mydb.cursor()
    # select all username and password
    sql ='SELECT id, name\
        FROM member WHERE username = %s AND password = %s'
    query = (username, password,)
    mycursor.execute(sql,query)
    myresult = mycursor.fetchall()
    if not myresult:
        return RedirectResponse(url="/error/?message=Username or password is not correct", status_code=303)
    else:
        for row in myresult:
            member_id, member_name = row
            # Store sign-in status and credentials into sessionmiddleware
            request.session.update({
                "SIGNED-IN": True,
                "MEMBER_ID": member_id,
                "MEMBER_NAME": member_name,
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
    if len(request.session.keys()) == 0 or not request.session["SIGNED-IN"] == True:
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
            message.id AS message_id,\
            member.id AS member_id,\
            member.name AS name, \
            message.context AS message \
            FROM member \
            INNER JOIN message ON member.id = message.member_id\
            ORDER BY message_id"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        # create structure of template literate
        message = ""
        for m in myresult:
            message_id, member_id, member_name, message_context = m
            message += f'<form id="delete-form-{message_id}" style="display: inline" onsubmit="deleteMessage(event)"> \
                <b>{member_name}</b> : {message_context} \
                <input type="hidden" name="message_id" value="{message_id}">'
            if member_id == request.session["MEMBER_ID"]:
                message += '<input type="submit" value="x">\
                </form>'
            else:
                message += '</form>'
        # return response
        return templates.TemplateResponse(
            request=request,
            name='member.html',
            context={
                "name": request.session["MEMBER_NAME"],
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
    if len(request.session.keys()) == 0 or not request.session["SIGNED-IN"] == True:
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
    if len(request.session.keys()) == 0 or not request.session["SIGNED-IN"] == True:
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
        sql = 'DELETE FROM message \
            WHERE id = %s AND member_id = %s'
        query = (message_id, request.session["MEMBER_ID"],)
        mycursor.execute(sql, query)
        mydb.commit()
        return RedirectResponse(url="/member", status_code=303)

# Create nested baseModel for response 
class Member(BaseModel):
    id: int
    name: str
    username: str

class memberItem(BaseModel):
    data: Member | None = None # should be able to respond null

@app.get("/api/member", response_model=memberItem)
def findMember(request: Request, username: str):
    # connect to MySQL 'website' database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DBpassword,
        database="website"
    )
    mycursor = mydb.cursor()
    # Select id, name and username
    sql = "SELECT id, name, username FROM member\
            WHERE username = %s"
    val = (username,)
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
            member_id, member_name, member_username = row
            data = {
                "id": member_id,
                "name": member_name,
                "username": member_username
                }
            item["data"] = data
    return item

class nameUpdateRequest(BaseModel):
    name: str


@app.patch("/api/member")
async def updateUsername(request: Request, body: nameUpdateRequest, content_type: str = Header(...)):
    if content_type != "application/json":
        raise HTTPException(
            status_code=400, detail="Invalid Content-Type header. Expected 'application/json'.")
    # connect to MySQL 'website' database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=DBpassword,
        database="website"
    )
    mycursor = mydb.cursor()
    sql = "UPDATE member\
            SET name = %s\
            WHERE id = %s"
    try:
        val = (body.name, request.session["MEMBER_ID"])
        mycursor.execute(sql, val)
        mydb.commit()
        if (mycursor.rowcount != 0):
            request.session.update({"MEMBER_NAME": body.name})
            return {"ok": True}
        else:
            return {"error": True}
    except:
        return {"error": True}

if __name__ == "__main__":
   uvicorn.run("main:app",host = "127.0.0.1", port= 8000, log_level="info")

# load in environment variables in .env
load_dotenv()
DBpassword = os.getenv('password')

# "CREATE TABLE member (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), username VARCHAR(255), password VARCHAR(255))"

