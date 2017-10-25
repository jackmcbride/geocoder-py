from flask import Flask, render_template, request, send_file
import requests
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
import pandas
from table import generate_table
from map import generate_webmap
from time import sleep
import os

app=Flask(__name__)

@app.route('/')
def index():
    try:
        os.remove("uploads/uploaded_data.csv")
        os.remove("templates/table.html")
        os.remove("templates/webmap.html")
    except OSError:
        pass
    return render_template("index.html", text="Selected file must be a .csv file.")

@app.route('/success', methods=["POST"])
def success():
    global file
    if request.method=="POST":
        file=request.files["file"]
        if len(file.filename) > 0:
            file.save("uploads/uploaded_data.csv")
            generate_table("uploads/uploaded_data.csv")
            generate_webmap("uploads/uploaded_data.csv")
            #Display table
            if generate_table("uploads/uploaded_data.csv") == "Error":
                return render_template("index.html",
                text="Make sure you have an column labelled 'Address' or 'address' in your .csv file.")
            else:
                return render_template("success.html",
                table="table_frame.html", btns="button_panel.html")
        else:
            return render_template("index.html",
            text="Please select a file.")

@app.route('/table')
def table():
    try:
        os.remove("templates/table.html")
    except OSError:
        pass
    generate_table("uploads/uploaded_data.csv")
    return render_template("success.html", table="table_frame.html", 
                            btns="button_panel.html")

@app.route('/map')
def map():
    try:
        os.remove("templates/webmap.html")
    except OSError:
        pass
    generate_webmap("uploads/uploaded_data.csv")
    return render_template("success.html", map="map_frame.html",
    btns="button_panel.html")

@app.route('/view_map')
def view_map():
    return render_template("webmap.html")

@app.route('/view_table')
def view_table():
    return render_template("table.html")

@app.route("/download")
def download():
    return send_file("uploads/uploaded_data.csv", attachment_filename="yourfile.csv", as_attachment=True)

if __name__ == '__main__':
    app.debug=True
    app.run()