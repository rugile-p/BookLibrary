from multiprocessing import connection
import uuid
from flask import Flask, redirect, request
from flask import render_template
import psycopg2

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/users")
def show_users():
    connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM users;')
    users_from_db = cursor.fetchall()
    cursor.close()
    connection.close()

    nou = len(users_from_db)
    return render_template("users.html", users = users_from_db, numberOfUsers = nou)

@app.route("/user/delete/<user_id>")
def delete_user(user_id):
    connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")

    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))

    cursor.close()
    connection.close()
 
    return redirect("/users")

@app.route("/user/add", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("user_new.html")
    if request.method == "POST":
        id = str(uuid.uuid4())
        name = request.form.get("name")

    connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (user_id, user_name) VALUES (%s, %s)", (id, name))
    cursor.close()
    connection.close()

    return redirect("/users")

@app.route("/user/modify/<user_id>", methods=["GET", "POST"])
def modify_user(user_id):
    if request.method == "GET":
        connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        single_user = cursor.fetchone()
        print(single_user)
        cursor.close()
        connection.close()

        return render_template("user_modify.html", user = single_user)

    if request.method == "POST":
        name = request.form.get("name")
        connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")

        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET user_name = %s WHERE user_id = %s", (name, user_id))
        cursor.close()
        connection.close()

        return redirect("/users")

################################################################################################################################### BOOKS

@app.route("/books")
def show_books():
    connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM books;')
    books_from_db = cursor.fetchall()
    cursor.close()
    connection.close()

    nob = len(books_from_db)
    return render_template("books.html", books = books_from_db, numberOfBooks = nob)

@app.route("/book/delete/<book_id>")
def delete_book(book_id):
    connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))

    cursor.close()
    connection.close()
 
    return redirect("/books")

@app.route("/book/add", methods=["GET", "POST"])
def add_book():
    if request.method == "GET":
        return render_template("book_new.html")
    if request.method == "POST":
        id = str(uuid.uuid4())
        title = request.form.get("title")

    connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("INSERT INTO books (book_id, book_name) VALUES (%s, %s)", (id, title))
    cursor.close()
    connection.close()

    return redirect("/books")
    

@app.route("/book/modify/<book_id>", methods=["GET", "POST"])
def modify_book(book_id):
    if request.method == "GET":
        connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
        single_book = cursor.fetchone()
        print(single_book)
        cursor.close()
        connection.close()

        return render_template("book_modify.html", book = single_book)

    if request.method == "POST":
        title = request.form.get("title")
        connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("UPDATE books SET book_name = %s WHERE book_id = %s", (title, book_id))
        cursor.close()
        connection.close()

        return redirect("/books")


@app.route("/lendings")
def show_lendings():
    connection = psycopg2.connect(host="localhost", database="library", 
        user="postgres", password="12344")
    cursor = connection.cursor()
    cursor.execute("""SELECT books_users.id, books.book_name, users.user_name, until FROM books_users 
        INNER JOIN books ON books_users.book_id = books.book_id 
        INNER JOIN users ON books_users.user_id = users.user_id    
        ORDER BY users.user_name, books.book_name
    """)
    lendings_from_db = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("lendings.html", entries = lendings_from_db,
        number_of_lendings = len(lendings_from_db))

@app.route("/lending/add", methods=["GET", "POST"])
def add_lending():
    if request.method == "GET":
        connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users;")
        users_from_db = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books;")
        books_from_db = cursor.fetchall()
        cursor.close()

        connection.close()
       
        return render_template("lending_new.html", 
            users = users_from_db, 
            books = books_from_db)
    if request.method == "POST":
        id = str(uuid.uuid4())
        user_id = request.form.get("user")
        book_id = request.form.get("book")
        until = request.form.get("until")

        # take until as text - convert it to date and send to SQL

        connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("""INSERT INTO books_users (id, user_id, book_id, until) 
            VALUES (%s, %s, %s, %s)""", (id, user_id, book_id, until))
        cursor.close()
        connection.close()

        return redirect("/lendings")

@app.route("/lending/delete/<lending_id>")
def delete_lending(lending_id):
    connection = psycopg2.connect(host="localhost", 
        database="library", user="postgres", password="12344")
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("DELETE FROM books_users WHERE id = %s", (lending_id,))

    cursor.close()
    connection.close()

    return redirect("/lendings")


@app.route("/lending/modify/<lending_id>", methods=["GET", "POST"])
def modify_lending(lending_id):
    if request.method == "GET":
        connection = psycopg2.connect(host="localhost", 
            database="library", user="postgres", 
            password="12344")
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users;")
        users_from_db = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books;")
        books_from_db = cursor.fetchall()
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute("""SELECT id, book_id, user_id, until 
            FROM books_users WHERE id = %s""", (lending_id,))
        single_lending = cursor.fetchone()

        # make sure lending contains valid date

        cursor.close()
        connection.close()

        return render_template("lending_modify.html", 
            lending = single_lending, 
            users = users_from_db, 
            books = books_from_db)

    if request.method == "POST":
        until = request.form.get("until")
        book = request.form.get("book")
        user = request.form.get("user")
        
        connection = psycopg2.connect(host="localhost", 
            database="library", user="postgres", 
            password="12344")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("""UPDATE books_users SET book_id = %s,
            user_id = %s, until = %s WHERE id = %s""", 
            (book, user, until, lending_id))
        cursor.close()
        connection.close()

        return redirect("/lendings")  

##########################################################################################################################################

@app.route("/games")
def show_games():
    connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")

    cursor = connection.cursor()
    cursor.execute('SELECT * FROM games;')
    games_from_db = cursor.fetchall()

    cursor.close()
    connection.close()

    nog = len(games_from_db)
    return render_template("games.html", games = games_from_db, numberOfGames = nog)

@app.route("/game/delete/<game_id>")
def delete_game(game_id):
    connection = psycopg2.connect(host="localhost", 
        database="library", user="postgres", password="12344")
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("DELETE FROM games WHERE id = %s", (game_id,))


    cursor.close()
    connection.close()

    return redirect("/games")

@app.route("/part/delete/<part_id>")
def delete_part(part_id):
    connection = psycopg2.connect(host="localhost", 
        database="library", user="postgres", password="12344")
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("DELETE FROM game_parts WHERE id = %s", (part_id,))


    cursor.close()
    connection.close()

    return redirect("/games")

@app.route("/game/add", methods=["GET", "POST"])
def add_game():
    if request.method == "GET":
        return render_template("game_new.html")
    if request.method == "POST":
        game_id = str(uuid.uuid4())
        name = request.form.get("name")

    connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
    connection.autocommit = True

    cursor = connection.cursor()
    cursor.execute("INSERT INTO games (id, name) VALUES (%s, %s)", (game_id, name))
    cursor.close()

    # id = str(uuid.uuid4())

    # cursor = connection.cursor()
    # cursor.execute("INSERT INTO game_parts (id, game_id) VALUES (%s, %s)", (id, game_id))
    # cursor.close()

    connection.close()

    return redirect("/games")

@app.route("/part/add/<game_id>", methods=["GET", "POST"])
def add_part(game_id):
    if request.method == "GET":
        return render_template("part_new.html", gameid = game_id )
    if request.method == "POST":
        id = str(uuid.uuid4())
        name = request.form.get("name")
        quantity = int(request.form.get("quantity"))

    connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
    connection.autocommit = True

    cursor = connection.cursor()
    cursor.execute("INSERT INTO game_parts (id, name, quantity, game_id) VALUES (%s, %s, %s, %s)", (id, name, quantity, game_id))
    cursor.close()

    # id = str(uuid.uuid4())

    # cursor = connection.cursor()
    # cursor.execute("INSERT INTO game_parts (id, game_id) VALUES (%s, %s)", (id, game_id))
    # cursor.close()

    connection.close()

    return redirect("/games")

@app.route("/game/modify/<game_id>", methods=["GET", "POST"])
def modify_game(game_id):
    if request.method == "GET":
        connection = psycopg2.connect(host="localhost", 
            database="library", user="postgres", password="12344")
        
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM games WHERE id = %s;", (game_id,))
        single_game = cursor.fetchone()
        cursor.close()

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM game_parts WHERE game_id = %s;", (game_id,))
        parts_from_db = cursor.fetchall()
        cursor.close()

        connection.close()

        return render_template("game_modify.html", game = single_game, game_parts = parts_from_db)

    if request.method == "POST":
        game_name = request.form.get("name")
        # game_part_name = request.form.get("game_part_name")
        # quantity = request.form.get("quantity")
        
        connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
        connection.autocommit = True

        cursor = connection.cursor()
        cursor.execute("UPDATE games SET name = %s WHERE id = %s", (game_name, game_id))
        cursor.close()

        # cursor = connection.cursor()
        # cursor.execute("UPDATE game_parts SET name = %s, quantity = %s WHERE game_id = %s", (game_part_name, quantity, game_id))
        # cursor.close()

        connection.close()

        return redirect("/games")  
 

@app.route("/part/modify/<part_id>", methods=["GET", "POST"])
def modify_part(part_id):
    if request.method == "GET":
        connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM game_parts WHERE id = %s", (part_id,))
        single_part = cursor.fetchone()
       
        cursor.close()
        connection.close()

        return render_template("part_modify.html", part = single_part)

    if request.method == "POST":
        name = request.form.get("name")
        quantity = request.form.get("quantity")
        connection = psycopg2.connect(host="localhost", database="library", user="postgres", password="12344")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("UPDATE game_parts SET name = %s, quantity = %s WHERE id = %s", (name, quantity, part_id))
        cursor.close()
        connection.close()

        return redirect("/games")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
