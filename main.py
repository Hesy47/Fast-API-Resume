from fastapi import FastAPI
import validation as valid

app = FastAPI()


@app.get("/")
async def welcome():
    welcome = "This is my First REST API app"
    framework = "Created by FAST API"

    return {"Welcome": welcome, "Framework": framework}


@app.get("/admin/{admin_pass}")
async def admin_panel(admin_pass: int):
    if admin_pass == 1380:
        return {"Message": "Welcome back Admin"}

    return {"Message": "The password is not valid!"}


@app.get("/business/{position}")
async def business(position: valid.ModelName):
    if position == valid.ModelName.it:
        return {"Message": "Welcome back IT Master"}
    elif position == valid.ModelName.social:
        return {"Message": "Welcome back SOCIAL Master"}
    elif position == valid.ModelName.sell:
        return {"Message": "Welcome back SOCIAL Master"}


@app.post("/register")
async def register(user: valid.User):
    message = f"welcome to our website {user.username}"

    return {"message": message, "information": user}
