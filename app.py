from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "secret"   # required for flashing messages

# -------------------------
# MongoDB Connection (using MongoDB Atlas)
# -------------------------
client = MongoClient("mongodb+srv://flask_app:80UTj7Bymm2mMRDH@flaskapp.xuvpmkq.mongodb.net/?appName=flaskapp")
# client = MongoClient("mongodb+srv://flask_app:80UTj7Bymm2mMRDH@flaskapp.xuvpmkq.mongodb.net/")
db = client["mydb"]
collection = db["flask_app"]


# -------------------------
# Show Form
# -------------------------
@app.route('/')
def form():
    return render_template("form.html")


# -------------------------
# Handle Form Submission
# -------------------------
@app.route('/submit', methods=['GET', 'POST'])
def submit():

    if request.method == 'GET':
        return redirect(url_for("form"))

    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        flash("Name and Email are required!")
        return render_template("form.html")

    data = {"name": name, "email": email}

    try:
        collection.insert_one(data)
        return redirect(url_for("success"))

    except Exception as e:
        flash(str(e))
        return render_template("form.html")


# -------------------------
# Success Page
# -------------------------
@app.route('/success')
def success():
    return render_template("success.html")


if __name__ == '__main__':
    app.run(debug=True, port=5002)
