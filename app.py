from flask import Flask, render_template
import requests

url="https://api.themoviedb.org/3/movie"

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)
