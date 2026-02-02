from flask import Flask, render_template, request
import requests

API_KEY = "beafddf47a67dfbd047f0534d1f41694"
BASE_URL = "https://api.themoviedb.org/3"
IMG_BASE = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)

@app.route('/')
def home():
    url = BASE_URL + '/movie/popular'
    params = {}
    params['api_key'] = API_KEY
    params['language'] = 'es-ES'
    
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    peliculas = datos.get('results', [])
    peliculas = peliculas[:10]
    
    for pelicula in peliculas:
        poster = pelicula.get('poster_path')
        if poster:
            pelicula['poster_full'] = IMG_BASE + poster
        else:
            pelicula['poster_full'] = None
    
    return render_template('base.html', movies=peliculas)

@app.route('/search')
def search():
    palabra = request.args.get('q', '')
    
    if palabra == '':
        return render_template('search.html', movies=[], query='')
    
    url = BASE_URL + '/search/movie'
    params = {}
    params['api_key'] = API_KEY
    params['query'] = palabra
    params['language'] = 'es-ES'
    
    respuesta = requests.get(url, params=params)
    datos = respuesta.json()
    peliculas = datos.get('results', [])
    
    for pelicula in peliculas:
        poster = pelicula.get('poster_path')
        if poster:
            pelicula['poster_full'] = IMG_BASE + poster
        else:
            pelicula['poster_full'] = None
    
    return render_template('search.html', movies=peliculas, query=palabra)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    url = BASE_URL + '/movie/' + str(movie_id)
    params = {}
    params['api_key'] = API_KEY
    params['language'] = 'es-ES'
    params['append_to_response'] = 'credits,videos'
    
    respuesta = requests.get(url, params=params)
    pelicula = respuesta.json()
    
    poster = pelicula.get('poster_path')
    if poster:
        pelicula['poster_full'] = IMG_BASE + poster
    else:
        pelicula['poster_full'] = None
    
    actores = []
    if 'credits' in pelicula:
        cast = pelicula['credits'].get('cast', [])
        for actor in cast[:5]:
            actor_data = {}
            actor_data['name'] = actor.get('name', 'N/A')
            actor_data['character'] = actor.get('character', 'N/A')
            profile = actor.get('profile_path')
            if profile:
                actor_data['foto'] = IMG_BASE + profile
            else:
                actor_data['foto'] = None
            actores.append(actor_data)
    
    pelicula['actores'] = actores
    
    trailer = None
    if 'videos' in pelicula:
        videos = pelicula['videos'].get('results', [])
        for video in videos:
            if video.get('type') == 'Trailer':
                trailer = video.get('key')
                break
    
    pelicula['trailer'] = trailer
    
    return render_template('detail.html', movie=pelicula)

if __name__ == '__main__':
    app.run(debug=True)
