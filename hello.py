from flask import Flask, request, render_template, url_for, redirect, g
import os
app = Flask(__name__,template_folder='templates')
print os.environ['MAPPATH']

@app.route("/")
def hello():
    return render_template('form.html')

@app.route("/map", methods=['GET', 'POST'])
def map():
    return render_template('example.html')
