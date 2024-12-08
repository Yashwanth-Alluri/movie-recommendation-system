from flask import Flask, request, jsonify, render_template
import pickle
import requests

app = Flask(__name__)

# Load preprocessed data
movies = pickle.load(open('data/movies.pkl', 'rb'))  # Renamed file
similarity_matrix = pickle.load(open('data/similarity_matrix.pkl', 'rb'))  # Renamed file

# Fetch movie poster using TMDb API
def fetch_poster(movie_id):
    api_key = "37611794e9a1aaaa2aa2f65b648681d5"  # Replace with your TMDb API key
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url).json()
    poster_path = response.get('poster_path')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return None

# Recommendation logic
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
        return []  # Return an empty list when the movie is not found

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Recommendation route
@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.json
    movie_name = data.get('movie_name')
    recommendations = recommend(movie_name)
    return jsonify({'recommendations': recommendations})

# Suggestion route
@app.route('/suggest', methods=['GET'])
def suggest():
    query = request.args.get('q', '').lower()
    suggestions = movies[movies['title'].str.lower().str.contains(query)].head(10)
    return jsonify({'suggestions': suggestions['title'].tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)