FROM python:3.6
WORKDIR /code
RUN pip3 install databases
RUN pip3 install DateTime
RUN pip3 install typing
RUN pip3 install uuid
RUN pip3 install asyncpg
RUN pip3 install psycopg2
RUN pip3 install email-validator
RUN pip3 install typing_extensions
RUN pip3 install python-dotenv
RUN pip3 install pymysql
RUN pip3 install sqlalchemy
RUN pip3 install fastapi
RUN pip3 install uvicorn
RUN pip3 install pydantic
RUN pip3 install passlib
RUN pip3 install python-multipart
RUN pip3 install werkzeug
RUN pip3 install python-jose[cryptography]

EXPOSE 8082
EXPOSE 8001 

#CMD ["uvicorn", "main:app", "--reload"] 
CMD ["python3", "__init__.py"]