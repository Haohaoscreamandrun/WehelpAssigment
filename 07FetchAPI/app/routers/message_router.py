from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
DBpassword = os.getenv('password')

router = APIRouter()

@router.post("/createMessage", response_class=HTMLResponse)
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


@router.post("/deleteMessage", response_class=HTMLResponse)
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
