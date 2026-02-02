from flask import Flask, render_template, request 
import requests

API_KEY="beafddf47a67dfbd047f0534d1f41694"
BASE_URL = "https://api.themoviedb.org/3"


app = Flask(__name__)
@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
