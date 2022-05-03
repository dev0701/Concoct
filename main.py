#main.py
from flask import Flask, jsonify, request, render_template, flash, session, abort
from flask import session as login_session
from flaskext.mysql import MySQL
import os

app = Flask(__name__)
app.secret_key = "totallysupersecret"
mysql = MySQL()

#MySQL config
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Zer0cool'
app.config['MYSQL_DATABASE_DB'] = 'Concoct'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

###Initial Landing page 
@app.route("/", methods=['POST','GET'])
def check():
    if not session.get('logged_in'):
        return home()
    else: 
        return home()

###Login page 
@app.route("/login", methods=['POST','GET'])
def login():
    if not session.get('logged_in'):
        return render_template("login.html")
    else: 
        return home()

###Log out Function
@app.route("/logout", methods=['POST','GET'])
def logout():
    if not session.get('logged_in'):
        return home()
    else:
        session['logged_in'] = False
        return home()

    
### User Authentication
@app.route("/authenticate", methods=['POST','GET'])
def authenticate():
    if auth_user(request.form['username'], request.form['password']) != "Authentication Failed":
        session['logged_in'] = True
        session['user'] = request.form['username']
        conn = mysql.connect()
        with conn.cursor() as cursor:
            #result = cursor.execute('SELECT position FROM Employee WHERE employee_id = %s', (session['id']))
            #position = cursor.fetchall()
            result = cursor.execute('SELECT * FROM USER WHERE username = %s', (session['user']))
            data = cursor.fetchall()
            return home()
    else:
        flash('The customer username or password is incorrect')
    return login()

###User Authentication function
def auth_user(username, password):
    conn = mysql.connect()
    with conn.cursor() as cursor: 
        result = cursor.execute('SELECT * FROM User WHERE username = %s and password = %s', (username, password))
        user = cursor.fetchall()
        if result > 0:
            got_user= "auth pass"
        else:
            got_user= "Authentication Failed"
    conn.close()
    return got_user


### Home Page
@app.route("/home", methods=['POST','GET'])
def home():
    return render_template("home.html")

### Results Page
@app.route("/results", methods=['POST','GET'])
def results():
    if request.method == "POST":
        if request.form['action'] == 'Show All Beverages':
            conn = mysql.connect()
            print(request.form['action'])
            with conn.cursor() as cursor: 
                result = cursor.execute('call ReturnAllCocktails;')
                data = cursor.fetchall()
            print(data[0][0])
            conn.close()
            return render_template("results.html", data=data)

        elif request.form['action'] == "Search" :
            ##Fetch ingredients from search form and add to a list. 
            form = request.form
            ingredients = []
            for x in range (1,5):
                curr = 'ingredient' + str(x)
                ingredients.append(form[curr])
            print(ingredients)
            
            ingredients_id = []
            ##Fetch ingredient id's from ingredient table, if any
            for a in range(0,4):
                if(ingredients[a] != ""):
                    conn = mysql.connect()
                    with conn.cursor() as cursor: 
                        result = cursor.execute('SELECT ingredient_id FROM Ingredient WHERE ingredient_name = %s', (ingredients[a]))
                    data = cursor.fetchall()
                    ingredients_id.append(data[0][0])
            print(ingredients_id)
            
            cocktails = []
            ##Fetch recipe id's that have the correlated ingredient numbers
            for a in range(0, len(ingredients_id)):
                conn = mysql.connect()
                with conn.cursor() as cursor: 
                    result = cursor.execute('SELECT cocktail_id FROM Ingredient_Cocktail WHERE ingredient_id = %s', (ingredients_id[a]))
                data = cursor.fetchall()
                for x in range (0,len(data)):
                    cocktails.append(data[x][0])
            print(cocktails)

            ##Sort cocktails in order of ingredients match:
            cocktails = sorted(cocktails, key = cocktails.count, reverse = True)
            print(cocktails)
            cocktails_sorted = []
            curr = cocktails[0]
            cocktails_sorted.append(cocktails[0])
            for x in range (1,len(cocktails)):
                if curr != cocktails[x]:
                    cocktails_sorted.append(cocktails[x])
                    curr = cocktails[x]
            print(cocktails_sorted)
            
            cocktail_results = []
            ##Fetch the cocktails in order: 
            for x in cocktails_sorted:
                conn = mysql.connect()
                with conn.cursor() as cursor: 
                    result = cursor.execute('SELECT * FROM Cocktail WHERE cocktail_id = %s', (x))
                data = cursor.fetchall()
                cocktail_results.append(data)
            print(cocktail_results)
            #print(cocktail_results[0][0][1])
            #print(cocktail_results[0][0][3])
            #print(cocktail_results[1][0][1])
            #print(cocktail_results[1][0][3])
            
            cocktail_final = []
            ##Fetch Cocktail Relevant information: 
            for x in range(0, len(cocktail_results)):
                conn = mysql.connect()
                with conn.cursor() as cursor: 
                    result = cursor.execute('SELECT c.cocktail_id, c.cocktail_name, u.name, c.description, t.taste_name, c.likes  FROM Cocktail c, User u, Taste t WHERE c.cocktail_id = %s AND u.user_id = c.user_id AND t.taste_id = c.taste_id' , (cocktail_results[x][0][0]))
                data = cursor.fetchall()
                cocktail_final.append(data)
                
            data = cocktail_final
            return render_template("results.html",data = data)

@app.route("/add_drink", methods=['POST','GET'])
def add_drink():
    return render_template("add_drink.html")

@app.route("/drink_added", methods=['POST','GET'])
def drink_added():
    if request.method == "POST":
        drink_name = request.form['drink-name']
        ingredient1 = request.form['ingredient1']
        ingredient2 = request.form['ingredient2']
        ingredient3 = request.form['ingredient3']
        ingredient4 = request.form['ingredient4']
        ingredient5 = request.form['ingredient5']
        ingredient6 = request.form['ingredient6']
        taste= request.form['taste']
        description = request.form['description']
        username = session['user']
        ingredients = []
        ingredients.append(ingredient1)
        ingredients.append(ingredient2)
        ingredients.append(ingredient3)
        ingredients.append(ingredient4)
        ingredients.append(ingredient5)
        ingredients.append(ingredient6)
        print(ingredients)
        print(username)
        ingredients_to_add = []

        ##Find the user who is submitting the drink
        conn = mysql.connect()
        user_id = ""
        with conn.cursor() as cursor: 
            result = cursor.execute('SELECT user_id FROM User WHERE username = %s ', (username))
            data = cursor.fetchall()
            print(data)
            user_id = data[0]

        ##Find ingredients that need to be added to ingredient list and add them
        for x in range(0, 6):
            if ingredients[x] != '':
                conn = mysql.connect()
                with conn.cursor() as cursor: 
                    result = cursor.execute('SELECT ingredient_id FROM Ingredient WHERE ingredient_name = %s ', (ingredients[x]))
                    data = cursor.fetchall()
                    if result > 0:
                        print("found" + ingredients[x])
                        ingredients_to_add.append(data)
                    else:
                        result = cursor.execute('SELECT max(ingredient_id) FROM Ingredient')
                        data = cursor.fetchall()
                        print(data)
                        new_id = data[0][0] + 1
                        print(new_id)
                        print(ingredients[x])
                        result = cursor.execute('INSERT INTO `Ingredient` (`ingredient_id`, `ingredient_name`) VALUES (%s,%s)',(new_id,ingredients[x]))
                        conn.commit()
                        data = cursor.fetchall()
                        ingredients_to_add.append(new_id)
        taste_id = 0
        ##Find if taste needs to be added, then add
        conn = mysql.connect()
        with conn.cursor() as cursor: 
            result = cursor.execute('SELECT taste_id FROM Taste WHERE taste_name = %s ', (taste))
            data = cursor.fetchall()
            if result > 0:
                print("found" + ingredients[x])
                taste_id = data
            else:
                result = cursor.execute('SELECT max(taste_id) FROM Taste')
                data = cursor.fetchall()
                print(data)
                new_id = data[0][0] + 1
                print(new_id)
                print(taste)
                result = cursor.execute('INSERT INTO `Taste` (`taste_id`, `taste_name`) VALUES (%s,%s)',(new_id,taste))
                conn.commit()
                data = cursor.fetchall()
                taste_id = new_id


        drink_id = 0
        ##Find if drink exists, if not, create the drink
        conn = mysql.connect()
        with conn.cursor() as cursor: 
            result = cursor.execute('SELECT cocktail_id FROM Cocktail WHERE cocktail_name = %s ', (drink_name))
            data = cursor.fetchall()
            if result > 0:
                print("found" + drink_name)
            else:
                result = cursor.execute('SELECT max(cocktail_id) FROM Cocktail')
                data = cursor.fetchall()
                print(data)
                new_id = data[0][0] + 1
                print(new_id)
                print(drink_name)
                result = cursor.execute('INSERT INTO `Cocktail` (`cocktail_id`, `cocktail_name`,`user_id`, `description`, `taste_id`,`likes`) VALUES (%s, %s, %s,%s, %s, %s)',(new_id,drink_name,user_id,description, taste_id, 0))
                conn.commit()
                data = cursor.fetchall() 
                drink_id = new_id
                
        print(taste_id)
        print(ingredients_to_add)
        ##Add Ingredient-Cocktail relationships
        for x in ingredients_to_add:
            conn = mysql.connect()
            with conn.cursor() as cursor: 
                result = cursor.execute('INSERT INTO `Ingredient_Cocktail` (`ingredient_id`,`cocktail_id`) VALUES (%s,%s)', (x, drink_id))
                data = cursor.fetchall()
                conn.commit()

        print(drink_name)
        return render_template("home.html")

@app.route("/drink", methods=['POST','GET'])
def drink():
    if request.method == "POST":
        drink_name = request.form['action']
        print(drink_name)
        conn = mysql.connect()
        information = []
        with conn.cursor() as cursor: 
            result = cursor.execute('SELECT c.cocktail_id, c.cocktail_name, u.name, c.description, t.taste_name, c.likes  FROM Cocktail c, User u, Taste t WHERE c.cocktail_name = %s AND u.user_id = c.user_id AND t.taste_id = c.taste_id', (drink_name))
            data = cursor.fetchall()
            information.append(data)
            drink_id = information[0][0][0]
            print(drink_id)
            result = cursor.execute('SELECT i.ingredient_name FROM Ingredient i, Ingredient_Cocktail ic WHERE ic.cocktail_id = %s AND ic.ingredient_id = i.ingredient_id', (drink_id))
            data = cursor.fetchall()
            information.append(data)
        print(information)
                
        return render_template("cocktail.html", data = information)

@app.route("/likes", methods=['POST','GET'])
def likes():
    return render_template("home.html")    

@app.route("/like", methods=['POST','GET'])
def like():
    if request.method == "POST":
        drink_name = request.form['action']
        drink_name = drink_name[5:]
        print(drink_name)
        ###Create Like
        conn = mysql.connect()
        with conn.cursor() as cursor: 
            result = cursor.execute('SELECT cocktail_id FROM Cocktail WHERE cocktail_name = %s', (drink_name))
            data = cursor.fetchall()
            drink_id = data[0][0]
            print(drink_id)
            username = session['user']
            result = cursor.execute('SELECT user_id FROM User WHERE username = %s', (username))
            data = cursor.fetchall()
            user_id = data[0][0]
            result = cursor.execute('SELECT user_id FROM Saved_Cocktail WHERE user_id = %s AND cocktail_id = %s', (user_id, drink_id))
            data = cursor.fetchall()
            print(data)
            if result <= 0:
                result = cursor.execute('INSERT INTO `Saved_Cocktail` (`cocktail_id`, `user_id`) VALUES (%s,%s)',(drink_id,user_id))
                conn.commit()
                result = cursor.execute('UPDATE Cocktail SET likes = (SELECT COUNT(user_id) FROM Saved_Cocktail WHERE cocktail_id = %s ) WHERE cocktail_id = %s',(drink_id, drink_id))
                conn.commit()
        return render_template("home.html")    

@app.route("/search", methods=['POST','GET'])
def search():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        if request.method == "POST":
            if request.form['action'] == 'Search':
                print('post method')
                form = request.form
                search_value = form['search_string']
                print(search_value)
                conn = mysql.connect()
                with conn.cursor() as cursor: 
                    result = cursor.execute('SELECT DISTINCT * FROM Employee WHERE employee_id = %s OR first_name = %s OR last_name = %s OR position = %s OR salary = %s OR department_id = %s OR city = %s', (search_value,search_value,search_value,search_value,search_value,search_value,search_value ))
                data = cursor.fetchall()
                print(data)       
                conn.close()
                return render_template("search.html", data=data) 
            if request.form['action'] == 'Show All':
                conn = mysql.connect()
                print(request.form['action'])
                with conn.cursor() as cursor: 
                    result = cursor.execute('call ReturnAllEmployees;')
                    data = cursor.fetchall()
                print(data)
                conn.close()
                return render_template("search.html", data=data)
            if request.form['action'] == 'Sort by Salary':
                conn = mysql.connect()
                print(request.form['action'])
                with conn.cursor() as cursor: 
                    result = cursor.execute('call sortBySalary;')
                    data = cursor.fetchall()
                print(data)
                conn.close()
                return render_template("search.html", data=data)
    return render_template("search.html")


if __name__ == '__main__':
    app.run(debug=True)