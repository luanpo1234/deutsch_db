import sys
sys.path.append("..")

from flask import Flask, redirect, url_for, render_template, request

import api

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/suche/", methods=["POST", "GET"])
def suche():
    if request.method == "POST":
        level, gram_thema, thema = api.check_empty(request.form.getlist('lvl_checkbox')), api.check_empty([api.preprocess_query("select_all_grammar", el) for el in request.form["grammar"].split(" ")]), api.check_empty([api.preprocess_query("select_all_tkeywords", el) for el in request.form["theme"].split(" ")]) #TODO aqui e abaixo: função pros processamentos das strings
        test_search = {"level": level, "grammar": gram_thema, "keywords":thema}
        #jtemp = api.get_json(api.JSON_PATH)
        df = api.create_df_from_sql()
        df_res = api.search(df, test_search)
        str_df_res = api.df_to_html_pretty(df_res)
        return render_template("result.html", content=str_df_res)
    else:
        return render_template("suche.html")

"""    
@app.route("/einfuegen/", methods=["POST", "GET"])
def einfuegen():
    if request.method == "POST":
        link, level, gram_thema, thema = request.form["lnk"], [x.strip().upper() for x in request.form["lvl"].split(",")], [x.strip().lower() for x in request.form["grm"].split(",")], [x.strip().lower() for x in request.form["thm"].split(",")]
        entry = {"link": link, "level": level, "grammar": gram_thema, "keywords":thema}
        jtemp = api.get_json(api.JSON_PATH)
        json_new, msg = api.add_entry(jtemp, entry)
        df, error_indexes = api.create_df(jtemp)
        str_df_res = api.df_to_html_pretty(df)
        return render_template("result.html", content=msg + "<br />" + str_df_res)
    else:
        return render_template("einfuegen.html")
"""

if __name__ == "__main__":
    app.run(host='192.168.0.70', port=5000, debug=True)