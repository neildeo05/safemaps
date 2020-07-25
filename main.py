from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("home.html")

@app.route("/about", methods=["GET"])
def abt():
    return render_template("AboutPage.html")



@app.route("/map", methods=["GET"])
def home():
    if request.method == "GET":
        conn = sqlite3.connect("test.db")
        sql = "SELECT * FROM STREETS;"
        curr = conn.cursor()
        curr.execute(sql)
        x = curr.fetchall()
        conn.commit()
        conn.close()

        fs = ret_dup_rem_all(x)
        tmp = []
        for i in fs:
            tmp.append({"address": i[0], "cases": i[1]})

        fs = tmp
        # response = jsonify(fs)
        # response.headers.add('Access-Control-Allow-Origin', '*') 
        return render_template("iconmaps.html", test=fs)

@app.route("/has-covid", methods=["POST", "GET"])
def infected():
    if request.method == "GET":
        return render_template("hascovid.html")
    else:
        conn = sqlite3.connect("test.db")
        street = request.form["streetname"]
        statement = "INSERT INTO STREETS (NAME, COVID) VALUES ('{}', 'yes');".format(street)
        conn.execute(statement)
        conn.commit()
        conn.close()
        return redirect(url_for("home"))

@app.route("/recovered", methods=["POST", "GET"])
def recover():
    if request.method == "GET":
        return render_template("recovered.html")
    else:
        conn = sqlite3.connect("test.db")
        street = request.form["streetname"]
        
        statement = "SELECT rowid from streets where NAME = '{}'".format(street)
        # statement = "select rowid from streets where name='OOF Avenue';"
        curr = conn.cursor()
        curr.execute(statement)
        rows = curr.fetchall()
        ids = rows[0][0]
        statement = "DELETE from STREETS where rowid = '{}';".format(ids)
        curr.execute(statement)
        conn.commit()
        conn.close()
        return redirect(url_for("home"))






def ret_dup_rem_all(x):
    ret_arr = []
    for i in x:
        ret_arr.append([i[0], x.count(i)])


    res = []
    [res.append(x) for x in ret_arr if x not in res]

    return res

@app.route("/all", methods=["GET"])
def getall():
    conn = sqlite3.connect("test.db")
    sql = "SELECT * FROM STREETS;"
    curr = conn.cursor()
    curr.execute(sql)
    x = curr.fetchall()
    conn.commit()
    conn.close()
    fs = ret_dup_rem_all(x)
    fs = (dict(fs))
    response = jsonify(fs)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
# @app.route("/api/all", methods=["GET"])
# def apigetall():
    # conn = sqlite3.connect("test.db")
    # sql = "SELECT * FROM STREETS;"
    # curr = conn.cursor()
    # curr.execute(sql)
    # x = curr.fetchall()
    # conn.commit()
    # conn.close()
    # fs = ret_dup_rem_all(x)
    # fs = (dict(fs))
    # return render_template("api.html", title=fs)
if __name__ == '__main__':
    app.run(debug=True)


    
