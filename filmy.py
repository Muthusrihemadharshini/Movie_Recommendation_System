import requests
import pickle
import os
import pandas as pd
import streamlit as st
# CONFIG (CHANGE THIS ONLY)
# -----------------------------------
BASE = "https://huggingface.co/datasets/MSHD/movie-recommendation-data/resolve/main/"

# -----------------------------------
# DOWNLOAD + LOAD FUNCTION
# -----------------------------------
def download_and_load(file_url, file_name):
    
    # If already exists → don't download again
    if not os.path.exists(file_name):
        print(f"Downloading {file_name}...")

        r = requests.get(file_url)

        if r.status_code != 200:
            raise Exception(f"❌ Failed: {file_name} | Status: {r.status_code}")

        # If HTML instead of pickle → wrong link
        if r.content.startswith(b"<"):
            raise Exception(f"❌ {file_name} is HTML, not pickle → check URL")

        with open(file_name, "wb") as f:
            f.write(r.content)

    # Load pickle
    with open(file_name, "rb") as f:
        return pickle.load(f)


# -----------------------------------
# MOVIE FILES
# -----------------------------------

movie1  = download_and_load(BASE + "1th_movie_list.pkl?download=true",  "1.pkl")
movie2  = download_and_load(BASE + "2th_movie_list.pkl?download=true",  "2.pkl")
movie3  = download_and_load(BASE + "3th_movie_list.pkl?download=true",  "3.pkl")
movie4  = download_and_load(BASE + "4th_movie_list.pkl?download=true",  "4.pkl")
movie5  = download_and_load(BASE + "5th_movie_list.pkl?download=true",  "5.pkl")
movie6  = download_and_load(BASE + "6th_movie_list.pkl?download=true",  "6.pkl")
movie7  = download_and_load(BASE + "7th_movie_list.pkl?download=true",  "7.pkl")
movie8  = download_and_load(BASE + "8th_movie_list.pkl?download=true",  "8.pkl")
movie9  = download_and_load(BASE + "9th_movie_list.pkl?download=true",  "9.pkl")
movie10 = download_and_load(BASE + "10th_movie_list.pkl?download=true", "10.pkl")


# -----------------------------------
# SIMILARITY FILES
# -----------------------------------

sim1  = download_and_load(BASE + "1th_similarity.pkl?download=true",  "1s.pkl")
sim2  = download_and_load(BASE + "2th_similarity.pkl?download=true",  "2s.pkl")
sim3  = download_and_load(BASE + "3th_similarity.pkl?download=true",  "3s.pkl")
sim4  = download_and_load(BASE + "4th_similarity.pkl?download=true",  "4s.pkl")
sim5  = download_and_load(BASE + "5th_similarity.pkl?download=true",  "5s.pkl")
sim6  = download_and_load(BASE + "6th_similarity.pkl?download=true",  "6s.pkl")
sim7  = download_and_load(BASE + "7th_similarity.pkl?download=true",  "7s.pkl")
sim8  = download_and_load(BASE + "8th_similarity.pkl?download=true",  "8s.pkl")
sim9  = download_and_load(BASE + "9th_similarity.pkl?download=true",  "9s.pkl")
sim10 = download_and_load(BASE + "10th_similarity.pkl?download=true","10s.pkl")


# -----------------------------------
# OPTIONAL: STORE IN LISTS (EASY USE)
# -----------------------------------

all_movie_chunks = [
    movie1, movie2, movie3, movie4, movie5,
    movie6, movie7, movie8, movie9, movie10
]

similarity_matrices = [
    sim1, sim2, sim3, sim4, sim5,
    sim6, sim7, sim8, sim9, sim10
]

print("✅ All files loaded successfully!")
# -------------------------------


# Combine all movie chunks
all_movies_df = pd.concat(all_movie_chunks, ignore_index=True)
all_movies_titles = all_movies_df['Movie Name'].values

# -------------------------------
# POSTER FUNCTION
# -------------------------------
def fetch_poster(ID):
    try:
        url = f"http://www.omdbapi.com/?i={ID}&apikey=39be2013"
        data = requests.get(url).json()
        poster_url = data.get('Poster', 'https://via.placeholder.com/500x750?text=No+Poster+Available')

        if poster_url == "N/A":
            return 'https://via.placeholder.com/500x750?text=No+Poster+Available'

        return poster_url
    except:
        return 'https://via.placeholder.com/500x750?text=Error'

# -------------------------------
# UI
# -------------------------------
st.header("Indian Movie Recommender System")
select_value = st.selectbox("Select movie from dropdown", all_movies_titles)

# -------------------------------
# RECOMMEND FUNCTION
# -------------------------------
def recommend(movie):
    try:
        selected_similarity = None
        movies_chunk = None

        for idx, chunk in enumerate(all_movie_chunks):
            if movie in chunk['Movie Name'].values:
                selected_similarity = similarity_matrices[idx]
                movies_chunk = chunk
                break

        if selected_similarity is None:
            return [], []

        index = movies_chunk[movies_chunk['Movie Name'] == movie].index[0]
        distances = sorted(
            list(enumerate(selected_similarity[index])),
            reverse=True,
            key=lambda x: x[1]
        )

        recommend_movies = []
        recommend_posters = []

        for i in distances[1:6]:
            movie_id = movies_chunk.iloc[i[0]]['ID']
            recommend_movies.append(movies_chunk.iloc[i[0]]['Movie Name'])
            recommend_posters.append(fetch_poster(movie_id))

        return recommend_movies, recommend_posters

    except Exception as e:
        st.error(f"Error: {e}")
        return [], []

# -------------------------------
# BUTTON
# -------------------------------
if st.button("Show Recommendation"):
    recommended_movies, recommended_posters = recommend(select_value)

    if recommended_movies:
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movies[i])
                st.image(recommended_posters[i])