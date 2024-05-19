from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import mysql.connector
from dotenv import load_dotenv
import os

router = APIRouter()

load_dotenv()
DBpassword = os.getenv('password')


@router.post("/signup", response_class=HTMLResponse, tags=["sign"])
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
    mycursor.execute(sql, val)
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
        # redirect to homepage with query message
        return RedirectResponse(url="/?message=註冊成功，請由下方登入", status_code=303)


@router.post("/signin", response_class=HTMLResponse, tags=["sign"])
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
    sql = 'SELECT id, name\
        FROM member WHERE username = %s AND password = %s'
    query = (username, password,)
    mycursor.execute(sql, query)
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


@router.get("/signout", response_class=HTMLResponse, tags=["sign"])
async def logout(request: Request):
    # switch the flag back to red
    request.session.update({"SIGNED-IN": False})
    return RedirectResponse(url="/?message=已成功登出", status_code=302)
