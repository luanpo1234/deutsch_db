import sys
sys.path.append("..")

from flask import Flask, redirect, url_for, render_template, request

import json_reader

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/suche/", methods=["POST", "GET"])
def suche():
    if request.method == "POST":
        level, gram_thema, thema = request.form["lvl"].upper(), [x.strip().lower() for x in request.form["grm"].split(",")], [x.strip().lower() for x in request.form["thm"].split(",")] #TODO aqui e abaixo: função pros processamentos das strings
        test_search = {"level": level, "grammar": gram_thema, "keywords":thema}
        print("thema", thema)
        df_res = json_reader.search(json_reader.df, test_search)
        str_df_res = df_res.to_html()
        return f"Ergebnis: {str_df_res}"
    else:
        return render_template("suche.html")
    
@app.route("/einfuegen/", methods=["POST", "GET"])
def einfuegen():
    if request.method == "POST":
        link, level, gram_thema, thema = request.form["lnk"], request.form["lvl"].upper(), [x.strip().lower() for x in request.form["grm"].split(",")], [x.strip().lower() for x in request.form["thm"]]
        entry = {"link": link, "level": level, "grammar": gram_thema, "keywords":thema}
        json_new, msg = json_reader.add_entry(json_reader.jtest, entry)
        str_df_res = json_reader.df.to_html()
        return f"{msg} <br /> {str_df_res}"
    else:
        return render_template("einfuegen.html")

# @app.route("/<usr>/")
# def user(usr):
    # return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
    

# @app.route("/<name>")
# def user(name):
#     return f"<h1>Hello {name}!</h1>"

# @app.route("/admin/")
# def admin():
#     return redirect(url_for("user", name="Admin"))