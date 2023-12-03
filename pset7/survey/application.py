import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    if request.method == "POST":
        with open('survey.csv', 'a', newline='') as csvfile:
            fieldnames = ['First Name', 'Last Name', 'City', "Age", "Sibling"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'First Name': request.form.get("name"), 'Last Name': request.form.get("lastName"), 'City': request.form.get("City"), 'Age': request.form.get("age"), 'Sibling': request.form.get("sibling")})
            get_sheet()
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    if request.method == "GET":
        persons=[]
        with open('survey.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            counter = 0
            for row in reader:
                person = []
                counter +=1
                person.append(str(counter))
                person.append(row['First Name'])
                person.append(row['Last Name'])
                person.append(row['City'])
                person.append(row['Age'])
                person.append(row['Sibling'])
                persons.append(person)
        
        for person in persons:
            return render_template("sheet.html",persons=persons)
