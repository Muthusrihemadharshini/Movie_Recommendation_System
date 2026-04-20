import streamlit as st
import pickle
import requests
import pandas as pd

# Fetch poster for movie
def fetch_poster(ID, api_key):
    try:
        url = f"http://www.omdbapi.com/?i={ID}&apikey=39be2013"
        data = requests.get(url).json()
        # Handle cases where the poster is unavailable or invalid
        poster_url = data.get('Poster', 'https://via.placeholder.com/500x750?text=No+Poster+Available')
        
        # Check if the poster_url is 'N/A', which indicates no poster
        if poster_url == "N/A":
            return 'https://via.placeholder.com/500x750?text=No+Poster+Available'  # fallback poster
        
        return poster_url
    except Exception as e:
        st.error(f"Error fetching poster for {ID}: {e}")
        return 'https://via.placeholder.com/500x750?text=Error+Fetching+Poster'

# Set your OMDb API key
api_key = "39be2013"

# Load movie data from pickle files
all_movie_chunks = [
    pickle.load(open(f"{i}th_movie_list.pkl", 'rb')) for i in range(1, 11)
]
all_movies_df = pd.concat(all_movie_chunks, ignore_index=True)

# Extract movie titles for the dropdown
all_movies_titles = all_movies_df['Movie Name'].values

# Load similarity matrices from pickle files (optimized to avoid memory overload)
similarity_matrices = [
    pickle.load(open(f"{i}th_similarity.pkl", 'rb')) for i in range(1, 11)
]

# Define header and dropdown for movie selection
st.header("Indian Movie Recommender System")
select_value = st.selectbox("Select movie from dropdown", all_movies_titles)

def recommend(movie):
    try:
        # Identify which chunk contains the selected movie and get its similarity matrix
        selected_similarity = None
        movies_chunk = None
        for idx, chunk in enumerate(all_movie_chunks):
            if movie in chunk['Movie Name'].values:
                selected_similarity = similarity_matrices[idx]
                movies_chunk = chunk
                break
        
        if selected_similarity is None or movies_chunk is None:
            st.error("Movie not found!")
            return [], []

        # Get the index of the selected movie
        index = movies_chunk[movies_chunk['Movie Name'] == movie].index[0]
        distances = sorted(list(enumerate(selected_similarity[index])), reverse=True, key=lambda x: x[1])

        recommend_movies = []
        recommend_posters = []

        for i in distances[1:6]:
            movie_id = movies_chunk.iloc[i[0]]['ID']
            recommend_movies.append(movies_chunk.iloc[i[0]]['Movie Name'])
            recommend_posters.append(fetch_poster(movie_id, api_key))

        return recommend_movies, recommend_posters

    except Exception as e:
        st.error(f"Error in recommendation process: {e}")
        return [], []

# Show recommendations when the button is pressed
if st.button("Show Recommendation"):
    recommended_movies, recommended_posters = recommend(select_value)
    if recommended_movies and recommended_posters:
        col1, col2, col3, col4, col5 = st.columns(5)
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                st.text(recommended_movies[i])
                st.image(recommended_posters[i])

//