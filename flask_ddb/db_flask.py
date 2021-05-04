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
        level, gram_thema, thema = json_reader.check_empty(request.form["selectedItemsValue"].split(",")), json_reader.check_empty([json_reader.preprocess_query("select_all_grammar", el) for el in request.form["grammar"].split(" ")]), json_reader.check_empty([json_reader.preprocess_query("select_all_tkeywords", el) for el in request.form["theme"].split(" ")]) #TODO aqui e abaixo: função pros processamentos das strings
        print("selectedItems", request.form["selectedItemsValue"])
        test_search = {"level": level, "grammar": gram_thema, "keywords":thema}
        #jtemp = json_reader.get_json(json_reader.JSON_PATH)
        df = json_reader.create_df_from_sql()
        df_res = json_reader.search(df, test_search)
        str_df_res = json_reader.df_to_html_pretty(df_res)
        return render_template("result.html", content=str_df_res)
    else:
        return render_template("suche.html")
    
@app.route("/einfuegen/", methods=["POST", "GET"])
def einfuegen():
    if request.method == "POST":
        link, level, gram_thema, thema = request.form["lnk"], [x.strip().upper() for x in request.form["lvl"].split(",")], [x.strip().lower() for x in request.form["grm"].split(",")], [x.strip().lower() for x in request.form["thm"].split(",")]
        entry = {"link": link, "level": level, "grammar": gram_thema, "keywords":thema}
        jtemp = json_reader.get_json(json_reader.JSON_PATH)
        json_new, msg = json_reader.add_entry(jtemp, entry)
        df, error_indexes = json_reader.create_df(jtemp)
        str_df_res = json_reader.df_to_html_pretty(df)
        return render_template("result.html", content=msg + "<br />" + str_df_res)
    else:
        return render_template("einfuegen.html")

if __name__ == "__main__":
    app.run(host='192.168.0.70', port=5000, debug=True)