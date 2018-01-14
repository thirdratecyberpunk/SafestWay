from flask import Flask, request, render_template, url_for, redirect, g
import os
import urllib2
import json
from convert import getCrimeRateOfRoute, decode
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

    # requests a route for the given start and end
    route = urllib2.urlopen("https://api.mapbox.com/directions/v5/mapbox/walking/"
    + str(startLatLong["longitude"]) + ","
    + str(startLatLong["latitude"]) + ";"
    + str(finishLatLong["longitude"]) + ","
    + str(finishLatLong["latitude"]) + "?"
    + "alternatives=false&access_token="
    + "pk.eyJ1IjoibGV3aXNiIiwiYSI6ImNqY2RiaXc3ODBxcXUyeW1tbmdwc2xtZnQifQ.ro-l864DlvMbaZ4Dp5HJ9Q").read()
    route = json.loads(route)
    polyline = route["routes"][0]["geometry"]

    # gets a list of all streets
    points = decode(polyline)
    print "points: " + str(points)
    x = []
    for item in points:
        x.extend(item)

    # gets crime data for the waypoints in a given route
    crimevalue = getCrimeRateOfRoute(polyline)
    print "crimevalue: " + str(crimevalue)
    # takes the user to the map page
    return render_template('example.html', startLatLong=startLatLong, finishLatLong=finishLatLong, points=x)
