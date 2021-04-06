# -*- coding: utf-8 -*-
"""
Created on Mon Apr  5 14:40:33 2021

@author: luanp
"""

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>/")
def user(usr):
    return f"<h1>{usr}</h1>"

if __name__ == "__main__":
    app.run(debug=True)
    
    
    

# @app.route("/<name>")
# def user(name):
#     return f"<h1>Hello {name}!</h1>"

# @app.route("/admin/")
# def admin():
#     return redirect(url_for("user", name="Admin"))