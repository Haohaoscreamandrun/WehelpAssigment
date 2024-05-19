from fastapi import APIRouter, Request, HTTPException, Header
import mysql.connector
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()
DBpassword = os.getenv('password')

router = APIRouter(
    prefix="/api",
    tags=["api"]
)

# Create nested baseModel for response
class Member(BaseModel):
    id: int
    name: str
    username: str


class memberItem(BaseModel):
    data: Member | None = None  # should be able to respond null


class nameUpdateRequest(BaseModel):
    name: str


@router.get("/member", response_model=memberItem)
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


@router.patch("/member")
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
