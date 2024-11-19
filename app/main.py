#!/usr/bin/env python3

import os
from fastapi import FastAPI
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv("DBPASS")
DB = "xtm9px"


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],  
    allow_headers=["*"],  
)


def get_db_connection():
    try:
        db = mysql.connector.connect(
            user=DBUSER,
            host=DBHOST,
            password=DBPASS,
            database=DB
        )
        cursor = db.cursor()
        return db, cursor
    except Error as e:
        print(f"Error: {e}")
        return None, None


@app.get("/")
def read_root():
    return {"message": "Welcome to the DIY Spotify API!"}


@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    db, cursor = get_db_connection()
    if not db or not cursor:
        return {"Error": "Failed to connect to the database"}
    
    try:
        cursor.execute(query)
        headers = [x[0] for x in cursor.description]
        results = cursor.fetchall()
        json_data = [dict(zip(headers, result)) for result in results]
        return json_data
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    finally:
        cursor.close()
        db.close()


@app.get('/songs')
def get_songs():
    query = """
        SELECT songs.title, songs.album, songs.artist, songs.year,
               songs.file, songs.image, genres.genre
        FROM songs
        JOIN genres ON songs.genre = genres.genreid
    """
    db, cursor = get_db_connection()
    if not db or not cursor:
        return {"Error": "Failed to connect to the database"}
    
    try:
        cursor.execute(query)
        headers = [x[0] for x in cursor.description]
        results = cursor.fetchall()
        json_data = [dict(zip(headers, result)) for result in results]
        return json_data
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}
    finally:
        cursor.close()
        db.close()