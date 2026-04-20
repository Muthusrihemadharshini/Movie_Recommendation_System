import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

movies_1 = pickle.load(open("1st_movie_list.pkl", 'rb'))
movies_2 = pickle.load(open("2nd_movie_list.pkl", 'rb'))
movies_3 = pickle.load(open("3rd_movie_list.pkl", 'rb'))
movies_4 = pickle.load(open("4th_movie_list.pkl", 'rb'))
movies_5 = pickle.load(open("5th_movie_list.pkl", 'rb'))
movies_6= pickle.load(open("6th_movie_list.pkl", 'rb'))
movies_7 = pickle.load(open("7th_movie_list.pkl", 'rb'))
movies_8 = pickle.load(open("8th_movie_list.pkl", 'rb'))
movies_9 = pickle.load(open("9th_movie_list.pkl", 'rb'))
movies_10 = pickle.load(open("10th_movie_list.pkl", 'rb'))
all_movies_titles = []

# Append titles from each chunk to the list
all_movies_titles.extend(movies_1['Movie Name'].values)
all_movies_titles.extend(movies_2['Movie Name'].values)
all_movies_titles.extend(movies_3['Movie Name'].values)
all_movies_titles.extend(movies_4['Movie Name'].values)
all_movies_titles.extend(movies_5['Movie Name'].values)
all_movies_titles.extend(movies_6['Movie Name'].values)
all_movies_titles.extend(movies_7['Movie Name'].values)
all_movies_titles.extend(movies_8['Movie Name'].values)
all_movies_titles.extend(movies_9['Movie Name'].values)
all_movies_titles.extend(movies_10['Movie Name'].values)

# Accessing individual similarity matrices (similarity_1 to similarity_10)
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

# Store all similarity matrices in a list for easier processing
similarity_matrices = [
    similarity_1_matrix, similarity_2_matrix, similarity_3_matrix,
    similarity_4_matrix, similarity_5_matrix, similarity_6_matrix,
    similarity_7_matrix, similarity_8_matrix, similarity_9_matrix, similarity_10_matrix
]

similarity_1 = similarity_matrices[0]  # First similarity matrix
similarity_2 = similarity_matrices[1]  # Second similarity matrix
similarity_3 = similarity_matrices[2]  # Third similarity matrix
similarity_4 = similarity_matrices[3]  # Fourth similarity matrix
similarity_5 = similarity_matrices[4]  # Fifth similarity matrix
similarity_6 = similarity_matrices[5]  # Sixth similarity matrix
similarity_7 = similarity_matrices[6]  # Seventh similarity matrix
similarity_8 = similarity_matrices[7]  # Eighth similarity matrix
similarity_9 = similarity_matrices[8]  # Ninth similarity matrix
similarity_10 = similarity_matrices[9]  # Tenth similarity matrix






# Now all_movies_titles contains all movie titles from all chunks


st.header("Indian Movie Recommender System")

select_value = st.selectbox("Select movie from dropdown", all_movies_titles)

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(select_value)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.text(movie_name[i])
            st.image(movie_poster[i])
