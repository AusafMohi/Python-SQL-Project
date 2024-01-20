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
# Course:        231CIS109.950 
# 
# Created:       09/13/2022
#  
# 
#------------------------------------------------------------------------------ 


#!/usr/bin/env/python3

# Import db.py and class Movie from object.py
import db
from objects import Movie

# Define the global variables
CAT  = 1 
YEAR = 2 
MIN  = 3 
ADD  = 4 
DEL  = 5 
EXIT = 6 

COM_MENU  = "COMMAND MENU\n"
COM_MENU += f"{CAT} - View movies by category\n"
COM_MENU += f"{YEAR} - View movies by year\n"
COM_MENU += f"{MIN} - View movies with a maximum value of minutes\n" 
COM_MENU += f"{ADD} - Add a movie\n"
COM_MENU += f"{DEL} - Delete a movie\n"
COM_MENU += f"{EXIT} - Exit the program\n\n"
COM_MENU += "Please select your COMMAND choice: (1-5): "

def main():

    db.connect()
    display_title()
    cat_menu = build_categories()
    while True:

        command = int(input(COM_MENU))
        if command == CAT:
            display_movies_by_category(cat_menu)

        elif command == YEAR:
            display_movies_by_year()
        
        elif command == MIN: 
            display_movies_by_minutes() 

        elif command == ADD:
            add_movie()

        elif command == DEL:
            delete_movie()

        elif command == EXIT:
            break

        else:
            print("Not a valid command. Please try again.\n")
            display_menu()
    db.close()
    print("Bye!")

def display_title():
    print("The Movie List program\n")

    return


def build_categories():

    cat_menu = "CATEGORIES\n"

    categories = db.get_categories()
    for category in categories:
        cat_menu += str(category.id) + ". " + category.name + "\n"

    cat_menu += f"\nPlease select your CATEGORY choice: (1-{category.id}): "

    return cat_menu

def display_movies(movies, title_term):
    print("MOVIES - " + title_term)
    line_format = "{:>4s} {:37s} {:6s} {:5s} {:10s}"
    print(line_format.format("ID", "Name", "Year", "Mins", "Category"))
    print("-" * 65)
    for movie in movies:
        print(line_format.format(str(movie.id), movie.name,
                                 str(movie.year), str(movie.minutes),
                                 movie.category.name))
    print()

def display_movies_by_category(cat_menu):

    category_id = int(input(cat_menu))
    category = db.get_category(category_id)
    if category == None:
        print("There is no category with that ID.\n")
    else:
        print()
        movies = db.get_movies_by_category(category_id)
        display_movies(movies, category.name.upper())

def display_movies_by_year():
    year = int(input("Year: "))
    print()
    movies = db.get_movies_by_year(year)
    display_movies(movies, str(year))

#ADDING NEW OFPTION OF VIEWING MOVIES WITH MINUTES



def add_movie():
    name        = input("Name: ")
    year        = int(input("Year: "))
    minutes     = int(input("Minutes: "))
    category_id = int(input("Category ID: "))

    category = db.get_category(category_id)
    if category == None:
        print("There is no category with that ID. Movie NOT added.\n")
    else:
        movie = Movie(name=name, year=year, minutes=minutes,
                      category=category)
        db.add_movie(movie)
        print(name + " was added to database.\n")

#ADDING A DELETE FUNCTION HERE

def delete_movie():
    movie_id = int(input("Movie ID: "))
    Movie = db.get_movie_by_movieID(movie_id) 
 
    prompt = f"Are you sure you want to delete '{Movie.name}' (y/n):" 
    response = input(prompt) 
 
    if response.lower() =="y": 
        db.delete_movie(movie_id) 
        print(f"'{Movie.name} was deleted from the database.\n") 
    else: 
        print(f"'{Movie.name} was NOT deleted from the database.\n") 



def display_movies_by_minutes(): 
    max_min = int(input("Maximum number of minutes: ")) 
    print() 
    movies = db.get_movie_by_minutes(max_min) 
    display_movies(movies, f"LESS THAN {max_min}") 
 
 
if __name__ == "__main__":
    main()