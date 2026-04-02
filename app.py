import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

st.title('Movies Recommendation System')

movies_file_id = "1q1kVzsvKJ4nJH_8JkdJvERtdU94Y_mkG"
similarity_file_id = "1Xq8Q6b62kQhh1miuMUUqLkf-k8PH13A6"

movies_url = f"https://drive.google.com/uc?id={movies_file_id}"
similarity_url = f"https://drive.google.com/uc?id={similarity_file_id}"

if not os.path.exists("movies_dict.pkl"):
    gdown.download(movies_url, "movies_dict.pkl", quiet=False)

if not os.path.exists("similarity.pkl"):
    gdown.download(similarity_url, "similarity.pkl", quiet=False)

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarities = pickle.load(open('similarity.pkl', 'rb'))

selected_movie = st.selectbox('Select a movie', movies['title'])


def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=aa60fd3cecf966eba363e707215770e3'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarities[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


if st.button('Recommend'):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(names[0])
        st.image(posters[0])

    with col2:
        st.write(names[1])
        st.image(posters[1])

    with col3:
        st.write(names[2])
        st.image(posters[2])

    with col4:
        st.write(names[3])
        st.image(posters[3])

    with col5:
        st.write(names[4])
        st.image(posters[4])