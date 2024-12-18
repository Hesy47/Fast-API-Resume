from fastapi import FastAPI
import validations as validated


app = FastAPI()


@app.get("/welcome/{admin_name}")
def welcome(admin_name):
    Admin_Message = "Welcome Back Master"
    Message = "Welcome to my first Fast API App!"

    if admin_name == "Amir" or admin_name == "Code":
        return {"Message": Admin_Message}

    return {"Message": Message}


@app.post("/send-info")
def send_information(user: validated.Create_User):
    return {"Message": "Successfully added to database", "information": user}
