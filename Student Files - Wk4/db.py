#------------------------------------------------------------------------------- 
# Assignment:    Assignment 3B 
# 
# Program Name:  am_Assignment_3B.py  
#                 
# 
# Purpose:       The purpose of this program is  
#                to display the database's data in the Python's program. 
# 
# Author:        Ausaf Mohiuddin  
# 
# Created:       09/13/2022
#  
# 
#------------------------------------------------------------------------------ 
 



import sys
import os
import sqlite3
from contextlib import closing

from objects import Category
from objects import Movie

conn = None
DB_FILE = "db/movies.db"

def connect():
    global conn
    if not conn:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row

def close():
    if conn:
        conn.close()

def make_category(row):
    return Category(row["categoryID"], row["categoryName"])

def make_movie(row):
    return Movie(row["movieID"], row["name"], row["year"], row["minutes"],
            make_category(row))

def get_categories():
    query = '''SELECT categoryID, name as categoryName
               FROM Category'''
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()

    categories = []
    for row in results:
        categories.append(make_category(row))
    return categories

def get_category(category_id):
    query = '''SELECT categoryID, name AS categoryName
               FROM Category WHERE categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        row = c.fetchone()
        if row:
            return make_category(row)
        else:
            return None

def get_movies_by_category(category_id):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID as categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE Movie.categoryID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (category_id,))
        results = c.fetchall()

    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies

#START OF GET_MOVIE FUNCTION

def get_movie_by_movieID(movieID):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID as categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE movieID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (movieID,))
        result = c.fetchone()

    return make_movie(result)



def get_movies_by_year(year):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID as categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE year = ?'''
    with closing(conn.cursor()) as c:
        c.execute(query, (year,))
        results = c.fetchall()

    movies = []
    for row in results:
        movies.append(make_movie(row))
    return movies


def add_movie(movie):
    sql = '''INSERT INTO Movie (categoryID, name, year, minutes)
             VALUES (?, ?, ?, ?)'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie.category.id, movie.name, movie.year,
                        movie.minutes))
        conn.commit()

def delete_movie(movie_id):
    sql = '''DELETE FROM Movie WHERE movieID = ?'''
    with closing(conn.cursor()) as c:
        c.execute(sql, (movie_id,))
        test = conn.commit()
        print("Test", test)


def get_movie_by_minutes(minutes):
    query = '''SELECT movieID, Movie.name, year, minutes,
                      Movie.categoryID as categoryID,
                      Category.name as categoryName
               FROM Movie JOIN Category
                      ON Movie.categoryID = Category.categoryID
               WHERE minutes < ? 
               ORDER BY minutes ASC'''
    with closing(conn.cursor()) as c:
        c.execute(query, (minutes,))
        result = c.fetchall()
    
    movies = []
    for row in result:
        movies.append(make_movie(row))
    return movies
    
    
    