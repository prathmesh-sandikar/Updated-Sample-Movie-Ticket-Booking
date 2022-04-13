import flask
from flask import Flask, render_template, redirect, request
import sqlite3



conn = sqlite3.connect("Bookings.db", check_same_thread=False)
cursor = conn.cursor()

Movies_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='PICTURE'").fetchall()
shows_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='SHOWS'").fetchall()


if Movies_table:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE PICTURE(
                            MOVIEID INTEGER PRIMARY KEY AUTOINCREMENT,
                            MOVIENAME TEXT,
                            LANGUAGE TEXT,
                            MOVIEANIMATION TEXT,
                            SHOWSTART TEXT,
                             SHOWEND TEXT,
                             CITYNAME TEXT); ''')
    print("Table has created...!")


if shows_table:
    print("Table Already Exists ! ")

else:
    conn.execute(''' CREATE TABLE SHOWS(
                            SHOWID INTEGER PRIMARY KEY AUTOINCREMENT,
                            MOVIENAME TEXT,
                            HALLID INTEGER,
                            TIME INTEGER,
                            DATE INTEGER,
                            PRICEID INTEGER,
                            CityName TEXT); ''')
    print("Table has created")



app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/login-owner", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        getUname = request.form["uname"]
        getpass = request.form["pswd"]
    try:
        if getUname == 'owner' and getpass == "12345":
            return redirect("/dashboard")
        else:
            print("Invalid username and password")
    except Exception as e:
        print(e)

    return render_template("/owner_login.html")



@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        getMovieName = request.form["moviename"]
        getLanguage = request.form["mlanguage"]
        getAnimation = request.form["manimation"]
        getShow_Start = request.form["showstart"]
        getShow_End = request.form["showend"]
        getCityName = request.form["cityname"]

        print(getMovieName)
        print(getLanguage)
        print(getAnimation)
        print(getShow_Start)
        print(getShow_End)
        print(getCityName)
        try:
            data = (getMovieName, getLanguage, getAnimation, getShow_Start, getShow_End, getCityName)
            insert_query = '''INSERT INTO PICTURE(MOVIENAME, LANGUAGE, MOVIEANIMATION, SHOWSTART, SHOWEND, CITYNAME) 
                                    VALUES (?,?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            conn.commit()
            print("Movie added successfully")
            return redirect("/viewall")

        except Exception as e:
            print(e)
    return render_template("dashboard.html")



@app.route("/viewall")
def viewall():
    cur = conn.cursor()
    cur.execute("SELECT * FROM PICTURE")
    res = cur.fetchall()
    return render_template("viewall.html", cinemas=res)

@app.route("/showsDashboard", methods=["GET", "POST"])
def arrangeShows():
    if request.method == "POST":
        getMOvieName = request.form["mname"]
        getHallId = request.form["hid"]
        getTime = request.form["shtime"]
        getDate = request.form["shdate"]
        getPriceId = request.form["prid"]
        getCItyName = request.form["ciname"]

        print(getMOvieName)
        print(getHallId)
        print(getTime)
        print(getDate)
        print(getPriceId)
        print(getCItyName)

        try:
            data = (getMOvieName, getHallId, getTime, getDate, getPriceId, getCItyName)
            insert_query = '''INSERT INTO SHOWS(MOVIENAME, HALLID, TIME, DATE, PRICEID, CityName) 
                                    VALUES (?,?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            conn.commit()
            print("Show added successfully")
            return redirect("/viewallshows")

        except Exception as e:
            print(e)
    return render_template("showsDashboard.html")


@app.route("/viewallshows")
def viewallshows():
    cur = conn.cursor()
    cur.execute("SELECT * FROM SHOWS")
    res = cur.fetchall()
    return render_template("viewallshows.html", cinemass=res)



if __name__ == "__main__":
    app.run(debug=True)

