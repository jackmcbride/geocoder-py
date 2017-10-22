from flask import Flask, render_template, request, send_file
import requests
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
import pandas
from table import generate_table
from map import generate_webmap

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", text="Selected file must be a .csv file.")

@app.route('/success', methods=["POST"])
def success():
    global file
    if request.method=="POST":
        file=request.files["file"]
        if len(file.filename) > 0:
            file.save("uploads/uploaded" + file.filename)
            if generate_table("uploads/uploaded" + file.filename) == "Error":
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
    return render_template("success.html", table="table_frame.html", 
    download_btn="download.html", btns="button_panel.html")

@app.route('/map')
def map():
    return render_template("success.html", map="map_frame.html",
    download_btn="download.html", btns="button_panel.html")

@app.route('/geo_map')
def geo_map():
    generate_webmap("uploads/uploaded" + file.filename)
    return render_template("webmap.html")

@app.route('/geo_table')
def geo_table():
    return render_template("table.html")

@app.route("/download")
def download():
    return send_file("uploads/uploaded" + file.filename, attachment_filename="yourfile.csv", as_attachment=True)

if __name__ == '__main__':
    app.debug=True
    app.run()