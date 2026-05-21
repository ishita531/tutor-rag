from fastapi import APIRouter,Depends,HTTPException
from fastapi.security import HTTPBasic,HTTPBasicCredentials
from .model import StudentUser,TeacherUser
from config.db import users_collection
from .hash_utils import hash_password,verify_password
router=APIRouter()
#app=FastAPI()
security=HTTPBasic()




#Authenticates the user using http basic auth
def authenticate(credentials:HTTPBasicCredentials=Depends(security)):
    user_record=users_collection.find_one({"username":credentials.username})
    if not user_record or not verify_password(credentials.password,user_record["password"]):
        raise HTTPException(status_code=401,detail="Invalid username or password")
    return {
        "user_id": str(user_record["_id"]),
        "username":user_record["username"],
        "fullname":user_record["fullname"],
        "email":user_record["email"],
        "role":user_record["role"],
        "grade": user_record.get("grade")
    }


# Handles a student sign up request
#app.post("")
@router.post("/signup/student")
def signup_student(req:StudentUser):
    #Check if username already exists
    if users_collection.find_one({"username" : req.username}):
        raise HTTPException(status_code=400,detail="Username already exists")
    
    #Hash the password before storing
    hashed_password=hash_password(req.password)
    users_collection.insert_one(
    {
        "fullname":req.fullname,
        "email":req.email,
        "username":req.username,
        "password":hashed_password,
        "grade":req.grade,
        "school":req.school,
        "role":"Student",
    })
    return{"message":"Student user created Successfully"}

@router.post("/signup/teacher")
def signup_student(req:TeacherUser):
    #Check if username already exists
    if users_collection.find_one({"username" : req.username}):
        raise HTTPException(status_code=400,detail="Username already exists")
    
    #Hash the password before storing
    hashed_password=hash_password(req.password)
    users_collection.insert_one(
    {
        "fullname":req.fullname,
        "email":req.email,
        "username":req.username,
        "password":hashed_password,
        
        "school":req.school,
        "role":"Teacher",
    })
    return{"message":"Teacher user created Successfully"}


@router.get("/login")
def login(user=Depends(authenticate)):
    return user