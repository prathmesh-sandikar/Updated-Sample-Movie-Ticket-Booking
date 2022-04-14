import flask
from flask import Flask, render_template, redirect, request
import sqlite3

conn = sqlite3.connect("Bookings.db", check_same_thread=False)
cursor = conn.cursor()

Movies_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='PICTURE'").fetchall()
shows_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='SHOW'").fetchall()
halls_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='HALL'").fetchall()
Book_tickets_table = conn.execute(
    "SELECT name from sqlite_master WHERE type='table' AND name='BOOKED_TICKETS'").fetchall()

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
    conn.execute(''' CREATE TABLE SHOW(
                            SHOWID INTEGER PRIMARY KEY AUTOINCREMENT,
                            MOVIEID INTEGER,
                            MOVIENAME TEXT,
                            HALLID INTEGER,
                            TIME INTEGER,
                            DATE INTEGER,
                            PRICEID INTEGER,
                            CityName TEXT); ''')
    print("Table has created")

if halls_table:
    print("Table Already Exists ! ")

else:
    conn.execute(''' CREATE TABLE HALL1(
                            HALLID INTEGER PRIMARY KEY,
                            SHOWID FOREIGN KEY REFERENCES SHOW(SHOWID),
                            Class TEXT,
                            No_of_seats INTEGER); ''')
    print("Table has created")

if Book_tickets_table:
    print("Table Already Exists ! ")

else:
    conn.execute(''' CREATE TABLE BOOKED_TICKETS(
                            TICKET_NO INTEGER PRIMARY KEY AUTOINCREMENT,
                            SHOWID INTEGER,
                            SEAT_NO INTEGER); ''')
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
        getMOvieId = request.form["mid"]
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
            data = (getMOvieId, getMOvieName, getHallId, getTime, getDate, getPriceId, getCItyName)
            insert_query = '''INSERT INTO SHOW(MOVIEID, MOVIENAME, HALLID, TIME, DATE, PRICEID, CityName) 
                                    VALUES (?,?,?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            conn.commit()
            print("Show added successfully")
            return redirect("/viewallshows")

        except Exception as e:
            print(e)
    return render_template("showsDashboard.html")


@app.route("/viewallshows")
def viewAllShows():
    cur = conn.cursor()
    cur.execute("SELECT * FROM SHOW")
    res = cur.fetchall()
    return render_template("viewallshows.html", cinemass=res)


@app.route("/showsHalls", methods=["GET", "POST"])
def arrangeHalls():
    if request.method == "POST":
        getMShowId = request.form["sid"]
        getClass = request.form["class"]
        getNoOfSeats = request.form["nos"]

        print(getMShowId)
        print(getClass)
        print(getNoOfSeats)

        try:
            data = (getMShowId, getClass, getNoOfSeats)
            insert_query = '''INSERT INTO HALL(SHOWID, Class, No_of_seats) 
                                    VALUES (?,?,?)'''

            cursor.execute(insert_query, data)
            conn.commit()
            print("Hall added successfully")
            return redirect("/viewallhalls")

        except Exception as e:
            print(e)
    return render_template("showsHalls.html")


@app.route("/viewallHalls")
def viewAllHalls():
    cur = conn.cursor()
    cur.execute("SELECT * FROM HALL")
    res = cur.fetchall()
    return render_template("viewallhalls.html", cinema=res)


@app.route("/getAvailableSeats", methods=["GET"])
def seatingManagement():
    if request.method == "GET":
        hallId = request.args.get('hallId')
        showId = request.args.get('showId')
        print("showId : ", showId)
        print("hallId: ", hallId)
        cur = conn.cursor()
        cur.execute("SELECT * FROM HALL WHERE HALLID = ? AND SHOWID = ?", (hallId, showId))
        res = cur.fetchall()
        print(res)
        print("*****")
        # data = (hall_class,showId)
        # q =  "SELECT * FROM HALL"
        # cur.execute(q,data)
        # res = cur.fetchall()
        # print("*** res **: ", res )


        totalGold = 0
        totalStandard = 0

        for i in res:
            print("***** ele ****: ", i[2])
            if i[2] == 'gold':
                totalGold = i[3]
            if i[2] == 'standard':
                totalStandard = i[3]

        # cur.execute("SELECT SEAT_NO FROM BOOKED_TICKETS WHERE SHOWID = " + getshowID)

        # goldSeats = []
        # standardSeats = []
        #
        # for i in range(1, totalGold + 1):
        #     goldSeats.append([i, ''])
        #
        #     for i in range(1, totalStandard + 1):
        #         standardSeats.append([i, ''])
        #
        #     for i in res:
        #         if i[0] > 1000:
        #             goldSeats[i[0] % 1000 - 1][1] = 'disabled'
        #         else:
        #             standardSeats[i[0] - 1][1] = 'disabled'
        return render_template("seating.html", goldSeats=totalGold, standardSeats=totalStandard)

if __name__ == "__main__":
    app.run(debug=True)
