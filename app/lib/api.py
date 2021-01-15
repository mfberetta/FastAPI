from fastapi import FastAPI, HTTPException
import databases, sqlalchemy, uuid
from fastapi.middleware.cors import CORSMiddleware
import json
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime, timedelta
import logging
from .models import *
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder

## lectura archivo de configuración ##
with open('config.json') as config_file:
    config = json.load(config_file)
logPath = config["dbLogPath"]

## configuracion del archivo de log##
logger = logging.getLogger('log')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(logPath)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup():
    await database.connect()
    logger.info ('Database connected successfully')

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
    logger.info ('Database disconnected successfully')

## CONSULTA DE USUARIOS ##
@app.get("/api/users", response_model=List[UserList])
async def find_all_users():

    try:
        query = users.select()
        logger.info("Consulta de usuarios")
        return await database.fetch_all(query)  

    except Exception as e:
        logger.error("CONSULTA DE USUARIOS - " + str(e))
        return {"status": str(e)}
        

## CREACION DE USUARIO ##
@app.post("/api/users", response_model=UserList)
async def register_users(user:UserEntry):

    try: 
        gID = str(uuid.uuid1())
        gDate = str(datetime.now())

        passwordHash = generate_password_hash(user.password, method='sha256')

        query = users.insert().values(
            user_id = gID,
            first_name = user.first_name,		
            lastname = 	user.lastname,
            username = 	user.username,	
            password =	passwordHash,
            email = user.email,
            type_user = user.type_user,
            created_at = gDate,
            status= "1"
        )

        await database.execute(query)
        logger.info("Creación de usuario: " + user.username )
        return {
            "user_id": gID,
            **user.dict(),
            "created_at":gDate,
            "status": "1"
        }

    except Exception as e:
        print(e)
        logger.error("CREACION DE USUARIO - " + str(e))
        return {
            "user_id": gID,
            **user.dict(),
            "created_at":gDate,
            "status": str(e)
        }

## CONSULTA DE USUARIO ##
@app.get("/api/users/{user_id}", response_model=UserList)
async def find_user_by_id (user_id: str):
    
    try:
        query = users.select().where(users.c.user_id == user_id)
        print (query)
        logger.info("Consulta de usuario: " + user_id)
        return await database.fetch_one(query)
    
    except:
        logger.error("CONSULTA DE USUARIO - " +str(e))
        return {"status": str(e)}

## ACTUALIZACION DE USUARIO ##
@app.put("/api/users", response_model=UserList)
async def update_user (user: UserUpdate):
    
    try:
        passwordHash = generate_password_hash(user.password, method='sha256')
        gDate = str(datetime.now())
        query = users.update().\
            where(users.c.user_id == user.user_id). \
            values(
                first_name = user.first_name,		
                lastname = 	user.lastname,
                username = 	user.username,	
                password =	passwordHash,
                email = user.email,
                type_user = user.type_user,
                created_at = gDate,
                status= "1",
        )
        await database.execute(query)
        logger.info("Actualizacion de usuario: " + user.user_id )
        return await find_user_by_id(user.user_id)
            
    except Exception as e:
        logger.error("ACTUALIZACION DE USUARIO - " + str(e))
        return {"status": "Error, incorrect values"}

## BORRADO DE USUARIO ##
@app.delete("/api/users/{user_id}")
async def delete_user (user:UserDelete):
    try:
        query = users.delete().where (users.c.user_id == user.user_id)
        await database.execute(query)
        logger.info("Borrado de usuario: " + user.user_id)
        return {"status":True, "message": "User has been deleted!!"}
    except Exception as e:
        logger.error("BORRADO DE USUARIO - " + str(e))
        return {"status": str(e)}

## LOGIN DE USUARIO ##
@app.post("/api/users/")
async def login_user (user:UserLogin):
    
    try:
        query = users.select().where(users.c.username == user.username)
        salida = await database.fetch_one(query)

        if salida:
            response_dic = jsonable_encoder(salida)
            print("Password: ", response_dic['password'])
            passwordValid = response_dic['password']                            
                                                                                                            
            if passwordValid != None:
    
                if user:
                    if check_password_hash(passwordValid,user.password):
                        logger.info("Login de usuario: " + user.username )
                        user_id = response_dic['user_id'] 
                        return {"status":True, "message": "Login Succesfully!!", "user_id": user_id}
                    logger.error("Error Login, " + user.username + " user or password incorrect!!")
                    return {"status":False, "message": "Error Login, user or password incorrect!!"}
            logger.error("Error Login!!")
            return {"status":False, "message": "Error Login"}

        else:
            logger.error("Username " + user.username + " not found!!" )
            return {"status":False, "message": "Username not found!!"}

    except Exception as e:
        logger.error("LOGIN DE USUARIO - " + str(e))
        return {"status": str(e)}