import streamlit as st
import pickle
import pandas as pd
import requests
import gzip


def fetch_posters(movie_id):
    response = requests.get(
        "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
            movie_id))

    data = response.json()

    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    movie_index = movie_df[movie_df["title"] == movie].index[0]
    vector = similarity[movie_index]
    similar_movies = sorted(enumerate(vector), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in similar_movies:
        movie_id = movie_df.iloc[i[0]].id

        recommended_movies.append(movie_df.iloc[i[0]]['title'])

        # fetch posters
        recommended_movies_posters.append(fetch_posters(movie_id))

    return recommended_movies, recommended_movies_posters


movie_df = pickle.load(open('movies.pkl', 'rb'))
movie_list = movie_df['title'].values

similarity = pickle.load(gzip.open("similarity.pkl.gz", "rb"))


st.title("Ree Recommends")

selected_movie = st.selectbox(
    "Choose a movie",
    movie_list)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters[0], caption=names[0])

    with col2:
        st.image(posters[1], caption=names[1])

    with col3:
        st.image(posters[2], caption=names[2])

    with col4:
        st.image(posters[3], caption=names[3])

    with col5:
        st.image(posters[4], caption=names[4])

