from fastapi import FastAPI

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

