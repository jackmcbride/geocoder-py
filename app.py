from flask import Flask, render_template, request, send_file
import requests
import pandas
from table import generate_table
from map import generate_webmap
import datetime
import os
import glob

app=Flask(__name__)

@app.route('/')
def index():
    try:
        os.remove("templates/table.html")
        os.remove("templates/webmap.html")
        os.remove("uploads/*")
    except OSError:
        pass
    return render_template("index.html", text="Selected file must be a .csv file.")

@app.route('/success', methods=["POST"])
def success():
    global file
    if request.method=="POST":
        file=request.files["file"]
        if len(file.filename) > 0:
            filename=datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f"+".csv")
            file.save(filename)
            if generate_table(filename) == "Error":
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
                            btns="button_panel.html")

@app.route('/map')
def map():
    generate_webmap(get_latest_file())
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
    return send_file(get_latest_file(), attachment_filename="yourfile.csv", as_attachment=True)

def get_latest_file():
    list_of_files = glob.glob('uploads/*')
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

if __name__ == '__main__':
    app.debug=True
    app.run()