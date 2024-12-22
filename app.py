import numpy as np
import pandas as pd
import streamlit as st 


# Loading the necessary data
movies_df = pd.read_csv('Required_df.csv')
# cos = pd.read_csv('cosine_df.csv', header=None)
cosine_similarity = np.loadtxt("cosine_sim.csv", delimiter=",")
movies_list = list(movies_df["title"].values)

# Function to get the recommendations
def get_recommendations(title, cosine_sim = cosine_similarity, new_df = movies_df, top_n=5):
    
    idx = new_df[new_df['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort by similarity and apply weighted score
    sim_scores = sorted(
        sim_scores, key=lambda x: (x[1] * new_df.iloc[x[0]]['weighted_score']), reverse=True
    )
    
    top_indices = [i[0] for i in sim_scores[1:top_n + 1]]  # Exclude itself
    return top_indices

# Application
st.set_page_config(page_title="Movie Recommendation System", layout="wide", page_icon="🎥")
st.title("Popcorn Picks🍿: What Movie Should I watch?🎬🎭")
st.write("Pick a Film and Let's find a Match !")
st.markdown("<hr style='border: 2px solid #ccc;'>", unsafe_allow_html=True)

selected_movie = st.selectbox("Select a Movie:", movies_list)

if st.button("Show Recommendations"):
    recommendations_list = get_recommendations(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for i, col in enumerate([col1, col2, col3, col4, col5]):
        recommended_movie = movies_df.iloc[recommendations_list[i]]
        
        with col:
            
            st.markdown(f"### **{recommended_movie['title']}**")
            st.write(f"**Overview:** {recommended_movie['overview']}")
            st.write(f"**Popularity Score (1-10):** {round(recommended_movie['popularity_log']*10,1)}")
            st.write(f"**Viewer Rating (1-10):** {round(recommended_movie['vote_average_log']*10,1)}")   