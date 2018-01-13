from flask import Flask, request, render_template, url_for, redirect, g
import os
import urllib2
import json
app = Flask(__name__,template_folder='templates')
api_key = os.environ['MAPPATH']

@app.route("/")
def hello():
    return render_template('form.html')

@app.route("/map", methods=['GET', 'POST'])
def map():
    # calculates the lat/long given a postcode
    start = request.form["start"]
    startPostcode = urllib2.urlopen("https://api.postcodes.io/postcodes/" + start).read()
    spj = json.loads(startPostcode)
    startLatLong = {"latitude": spj["result"]["latitude"], "longitude": spj["result"]["longitude"]}
    finish = request.form["finish"]
    finishPostcode = urllib2.urlopen("https://api.postcodes.io/postcodes/" + finish).read()
    fpj = json.loads(finishPostcode)
    finishLatLong = {"latitude": fpj["result"]["latitude"], "longitude": fpj["result"]["longitude"]}
    return render_template('example.html', startLatLong=startLatLong, finishLatLong=finishLatLong)
