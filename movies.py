import streamlit as st
import pickle
import requests
import pandas as pd

# Fetch poster for movie\import requests

def fetch_poster(ID, api_key):
    # Make an API request to OMDb API with the IMDB ID and the API key
    url = f"http://www.omdbapi.com/?i=tt3896198&apikey=39be2013"
    data = requests.get(url).json()

    # Get the poster URL
    poster_url = data.get('Poster', 'No poster available')  # Returns 'No poster available' if not found
    return poster_url

# Set your own OMDb API key here (replace 'your_api_key' with the actual key)
api_key = "39be2013"

# Example of how you call the function
imdb_id = "tt0848228"  # Replace with a valid IMDb ID
poster_url = fetch_poster(imdb_id, api_key)
print(poster_url)





"""def fetch_poster(ID, api_key):
    url = f"http://www.omdbapi.com/?i=tt3896198&apikey=39be2013"
    data = requests.get(url).json()
    poster_url = data.get('Poster', 'No poster available')
    return poster_url"""




# Load movie data from pickle files
movies_1 = pickle.load(open("1st_movie_list.pkl", 'rb'))
movies_2 = pickle.load(open("2nd_movie_list.pkl", 'rb'))
movies_3 = pickle.load(open("3rd_movie_list.pkl", 'rb'))
movies_4 = pickle.load(open("4th_movie_list.pkl", 'rb'))
movies_5 = pickle.load(open("5th_movie_list.pkl", 'rb'))
movies_6 = pickle.load(open("6th_movie_list.pkl", 'rb'))
movies_7 = pickle.load(open("7th_movie_list.pkl", 'rb'))
movies_8 = pickle.load(open("8th_movie_list.pkl", 'rb'))
movies_9 = pickle.load(open("9th_movie_list.pkl", 'rb'))
movies_10 = pickle.load(open("10th_movie_list.pkl", 'rb'))

# Combine all movie chunks into one DataFrame
all_movies_df = pd.concat([movies_1, movies_2, movies_3, movies_4, movies_5,
                           movies_6, movies_7, movies_8, movies_9, movies_10], ignore_index=True)

# Extract movie titles for the dropdown
all_movies_titles = all_movies_df['Movie Name'].values

# Load similarity matrices from pickle files
similarity_1_matrix = pickle.load(open("1st_movie_similarity.pkl", 'rb'))
similarity_2_matrix = pickle.load(open("2nd_films_similarity.pkl", 'rb'))
similarity_3_matrix = pickle.load(open("3rd_similarity.pkl", 'rb'))
similarity_4_matrix = pickle.load(open("4th_similarity.pkl", 'rb'))
similarity_5_matrix = pickle.load(open("5th_similarity.pkl", 'rb'))
similarity_6_matrix = pickle.load(open("6th_similarity.pkl", 'rb'))
similarity_7_matrix = pickle.load(open("7th_similarity.pkl", 'rb'))
similarity_8_matrix = pickle.load(open("8th_similarity.pkl", 'rb'))
similarity_9_matrix = pickle.load(open("9th_similarity.pkl", 'rb'))
similarity_10_matrix = pickle.load(open("10th_similarity.pkl", 'rb'))

# Store all similarity matrices in a list
similarity_matrices = [
    similarity_1_matrix, similarity_2_matrix, similarity_3_matrix,
    similarity_4_matrix, similarity_5_matrix, similarity_6_matrix,
    similarity_7_matrix, similarity_8_matrix, similarity_9_matrix, similarity_10_matrix
]

# Define the header and dropdown for movie selection
st.header("Indian Movie Recommender System")
select_value = st.selectbox("Select movie from dropdown", all_movies_titles)
def recommend(movie):
    # Identify which chunk contains the selected movie
    for idx, chunk in enumerate([movies_1, movies_2, movies_3, movies_4, movies_5, 
                                  movies_6, movies_7, movies_8, movies_9, movies_10]):
        if movie in chunk['Movie Name'].values:
            # Get the corresponding similarity matrix for the chunk
            selected_similarity = similarity_matrices[idx]
            movies_chunk = chunk
            break
    else:
        st.error("Movie not found in any chunk!")
        return [], []

    # Get the index of the selected movie within the correct chunk
    index = movies_chunk[movies_chunk['Movie Name'] == movie].index[0]
    distances = sorted(list(enumerate(selected_similarity[index])), 
                       reverse=True, key=lambda vector: vector[1])

    recommend_movies = []
    recommend_posters = []

    # Recommend top 5 similar movies from the same chunk
    for i in distances[1:6]:
        movie_id = movies_chunk.iloc[i[0]]['ID']
        recommend_movies.append(movies_chunk.iloc[i[0]]['Movie Name'])
        recommend_posters.append(fetch_poster(movie_id, api_key))

    return recommend_movies#, recommend_posters

if st.button("Show Recommend"):
    recommended_movies , recommended_posters = recommend(select_value) 
    if recommended_movies and recommended_posters:
        col1, col2, col3, col4, col5 = st.columns(5)
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            with col:
                st.text(recommended_movies[i])
                st.image(recommended_posters[i])

