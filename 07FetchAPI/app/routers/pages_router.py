from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
DBpassword = os.getenv('password')

router = APIRouter()

templates = Jinja2Templates(directory='templates')

@router.get("/error", response_class=HTMLResponse)
async def error(request: Request, message: str):  # message for query parameter
    return templates.TemplateResponse(
        request=request,
        name='error.html',
        # show different message in different situation
        context={"message": message},
        status_code=200
    )

@router.get("/member", response_class=HTMLResponse)
async def success(request: Request):
    # block any access without green flag
    if len(request.session.keys()) == 0 or not request.session["SIGNED-IN"] == True:
        return RedirectResponse(url="/?message=請重新登入", status_code=303)
    else:
        # access database and message table
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
                "message": message},
            status_code=200
        )
