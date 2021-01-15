import json
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
import logging
import databases, sqlalchemy, uuid


## lectura archivo de configuración ##

with open('config.json') as config_file:
    config = json.load(config_file)
dbConnection = config["dbConnection"]
dbDebug = config['dbDebug']


### SQLALCHEMY

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

## creamos la conexión a la base Postgress ## 

database = databases.Database(dbConnection)
metadata = sqlalchemy.MetaData()

## Creamos la tabla ##

users = sqlalchemy.Table(
    "py_users",
    metadata,
    sqlalchemy.Column("user_id", sqlalchemy.String, primary_key=True,unique=True),
    sqlalchemy.Column("first_name", sqlalchemy.String),
    sqlalchemy.Column("lastname", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String,unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String,unique=True),
    sqlalchemy.Column("type_user", sqlalchemy.CHAR),
    sqlalchemy.Column("created_at", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.CHAR),
)

engine = sqlalchemy.create_engine(dbConnection, echo = True)
metadata.create_all(engine)


class UserList(BaseModel):

    user_id: str
    first_name: str
    lastname: str
    username: str
    #password: str
    email: str
    type_user: str
    created_at: str
    status: str


class UserEntry(BaseModel):

    first_name: str = Field(..., example="user")
    lastname: str = Field(..., example="lastname")
    username: str = Field(..., example="username")
    password: str = Field(..., example="pass123")
    email: str = Field(..., example="example@test.com")
    type_user: str = Field(..., example="A")
    status: str = Field(..., example="active")

class UserUpdate(BaseModel):

    user_id: str = Field(..., example="Enter your id")
    first_name: str = Field(..., example="user")
    lastname: str = Field(..., example="lastname")
    username: str  = Field(..., example="username")
    password: str  = Field(..., example="pass123")
    email: str = Field(..., example="example@test.com")
    type_user: str = Field(..., example="A")
    status: str = Field(..., example="active")

class UserDelete(BaseModel):

    user_id: str = Field(..., example = "Enter your ID")

class UserLogin(BaseModel):

    username: str  = Field(..., example="username")
    password: str  = Field(..., example="pass123")