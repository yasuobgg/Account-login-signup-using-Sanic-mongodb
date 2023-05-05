# local lib
from mongo_module import MongoDB as mongo
from auth import protected, login

# from login import login

# simple lib
import os
from dotenv import load_dotenv

# app lib
from sanic import Sanic, text
from sanic import json as sanic_json
# from sanic.response import text
from sanic_cors import CORS

# lay thong tin tu file .env, khai bao mongodb
load_dotenv()
url = os.getenv("CONNECTION_STRING")
db_name = os.getenv("DATABASE_NAME")
col_name = os.getenv("COLLECTION_NAME")

mymongo = mongo(url, db_name, col_name)


app = Sanic(__name__)
CORS(app)
app.config.SECRET = "KEEP_IT_SECRET_KEEP_IT_SAFE"
app.blueprint(login)

# first, go to route `/jwt` to get bearer token
# then, each request you must send with bearer token to use


@app.route("/signup", methods=["post"])  # only need 2 fields: username and password
@protected
async def signup(request):
    data = request.json  # get data from request
    # print(data)
    username = data["username"]
    # print (username)
    if len(data) < 2:  # if 1 or 2 fields is missing
        return sanic_json(
            {"message": "please enter all fields"},
            headers={"X-Served-By": "CMC"},
            status=200,
        )
    if len(data) == 2:
        bool_qr = mymongo.findone({"info.username": username})  # find username
        if not bool_qr:  # can not find username in db
            mymongo.insert_one({"info": data})
            return sanic_json(
                {"message": "created"}, headers={"X-Served-By": "CMC"}, status=201
            )
        else:
            return sanic_json(
                {"message": "username already exis"},
                headers={"X-Served-By": "CMC"},
                status=200,
            )
    else:  # too many fields
        return sanic_json(
            {"message": "too many fields"}, headers={"X-Served-By": "CMC"}, status=200
        )


@app.route("/login", methods=["post"])
@protected
async def login(request):
    data = request.json
    username = data["username"]
    password = data["password"]

    bool_qr_username = mymongo.findone({"info.username": username})  # find username
    # print(bool_qr_username)
    if bool_qr_username:
        bool_qr_password = mymongo.find_one(
            {"info.username": username}
        )  # find data by username
        pass_qr = bool_qr_password["info"][
            "password"
        ]  # get the password by the data found
        # print(pass_qr)
        if pass_qr == password:  # neu dung, tra ve thong bao thanh cong
            return text("welcome")
        else:
            return text("incorrect password")  # neu sai, tra ve thong bao sai mat khau

    return text(
        "incorrect username"
    )  # neu ko tim thay username trong db, tra ve thong bao sai ten username


@app.route("/change_password", methods=["put"])
@protected
async def change_password(request):
    data = request.json
    r = mymongo.findone({"info.username": data["username"]})
    if r:
        myquery = {"info.username": data["username"]}
        newvalue = {"$set": {"info.password": data["password"]}}
        mymongo.update_one(myquery, newvalue)
        return text("done")
    else:
        return text("account not exis")


@app.route("/delete/<username:str>", methods=["delete"])
@protected
async def delete(request, username: str):
    r = mymongo.findone({"info.username": username})
    # print(r)
    if r:
        mymongo.delete_one({"info.username": username})
        return sanic_json(
            {"message": "successful"}, status=204
        )  # when set status=204, all json data will disappear
    else:
        return text("account not exis")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5555, debug=True, auto_reload=True)
