from flask import Flask, request, jsonify, render_template
import pickle
import requests

app = Flask(__name__)

import os
import requests

def download_similarity_matrix():
    url = "https://www.dropbox.com/scl/fi/7dne70f91kwtatyj8ql8q/similarity_matrix.pkl?rlkey=pnpdj7ne1pucrin405c0b11d8&st=chpzbstc&dl=1"
    destination = "data/similarity_matrix.pkl"
    
    if not os.path.exists(destination):
        print("Downloading similarity_matrix.pkl from Dropbox...")
        response = requests.get(url)
        response.raise_for_status()  
        
        os.makedirs("data", exist_ok=True)
        with open(destination, "wb") as file:
            file.write(response.content)
        print("Download completed!")


download_similarity_matrix()


import pickle
similarity_matrix = pickle.load(open("data/similarity_matrix.pkl", "rb"))


movies = pickle.load(open('data/movies.pkl', 'rb'))  
similarity_matrix = pickle.load(open('data/similarity_matrix.pkl', 'rb'))  


def fetch_poster(movie_id):
    api_key = "37611794e9a1aaaa2aa2f65b648681d5"  
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url).json()
    poster_path = response.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None


def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity_matrix[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append({
                "title": movies.iloc[i[0]].title,
                "poster": fetch_poster(movie_id)
            })
        return recommended_movies
    except IndexError:
        return []  


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.json
    movie_name = data.get('movie_name')
    recommendations = recommend(movie_name)
    return jsonify({'recommendations': recommendations})


@app.route('/suggest', methods=['GET'])
def suggest():
    query = request.args.get('q', '').lower()
    print(f"Received Query: {query}")  

    try:
        
        if movies.empty:
            print("Error: Movies DataFrame is empty!")
            return jsonify({'suggestions': []}), 500
        
        if 'title' not in movies.columns:
            print("Error: 'title' column missing in Movies DataFrame!")
            return jsonify({'suggestions': []}), 500

      
        suggestions = movies[movies['title'].str.lower().str.contains(query)].head(10)
        print(f"Suggestions Found: {suggestions['title'].tolist()}") 

        return jsonify({'suggestions': suggestions['title'].tolist()})
    except Exception as e:
        print(f"Error in /suggest: {e}") 
        return jsonify({'suggestions': []}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
