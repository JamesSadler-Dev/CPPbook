from flask import render_template,Flask,request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("tableofcontents.html")    


@app.route("/cppbook-pg<int:number>")
def book(number):
    return render_template(f"cppbook-pg{number}.html")    


