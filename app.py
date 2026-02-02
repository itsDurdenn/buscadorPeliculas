from flask import Flask, render_template, request
import requests

API_KEY="beafddf47a67dfbd047f0534d1f41694"
BASE_URL="https://api.themoviedb.org/3"
IMAGEN_BASE="https://image.tmdb.org/t/p/w500"

app=Flask(__name__)


@app.route('/')
def home():
    return render_template('base.html')


@app.route('/search')
def search():
    busqueda = request.args.get('q', '')
    
    if busqueda == '':
        return render_template('search.html', movies=[], query='')
    
    url_api = BASE_URL + '/search/movie'
    parametros = {
        'api_key': API_KEY,
        'query': busqueda,
        'language': 'es-ES'
    }
    
    respuesta = requests.get(url_api, params=parametros)
    datos = respuesta.json()
    
    peliculas = datos.get('results', [])
    
    for pelicula in peliculas:
        poster_path = pelicula.get('poster_path')
        if poster_path:
            pelicula['poster_full'] = IMAGEN_BASE + poster_path
        else:
            pelicula['poster_full'] = None
    
    return render_template('search.html', movies=peliculas, query=busqueda)

if __name__ == '__main__':
    app.run(debug=True)
