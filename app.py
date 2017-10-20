from flask import Flask, render_template, request, send_file
import requests
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from werkzeug import secure_filename
import datetime
import pandas
from table import generate_table
from map import generate_webmap

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success', methods=["POST"])
def success():
    global file
    if request.method=="POST":
        file=request.files["file"]
        if len(file.filename) > 0:
            file.save(secure_filename("uploaded" + file.filename))
            if generate_table("uploaded" + file.filename) == "Error":
                return render_template("index.html",
                text="Please make sure you have an address column in your csv file!")
            else:
                generate_webmap()
                return render_template("index.html",
                table="table_frame.html", download_btn="download.html", btns="button_panel.html")
        else:
            return render_template("index.html",
            text="Please select a file to upload.")

@app.route('/table')
def table():
    return render_template("index.html", table="table_frame.html", 
    download_btn="download.html", btns="button_panel.html")

@app.route('/map')
def map():
    return render_template("index.html", map="map_frame.html", 
    download_btn="download.html", btns="button_panel.html")

@app.route('/geo_map')
def geo_map():
    return render_template("webmap.html")

@app.route('/geo_table')
def geo_table():
    return render_template("table.html")

@app.route("/download")
def download():
    return send_file("geocoding_data.csv", attachment_filename="yourfile.csv", as_attachment=True)

if __name__ == '__main__':
    app.debug=True
    app.run()