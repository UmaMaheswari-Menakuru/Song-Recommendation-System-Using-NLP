#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load your DataFrame and cosine similarity matrix
df = pd.read_csv(r"C:\Users\user\ SONG RECOMMENDATIONS PROJECT(P426)\english_spotify_tracks_clusters.csv")  # Update with your actual CSV path
cosine_sim = np.load(r"C:\Users\user\ SONG RECOMMENDATIONS PROJECT(P426)\cosine_similarity_matrix.npy")  # Update with your actual cosine similarity file path

# Function to get song recommendations
def recommend_songs(song_name, df, cosine_sim, top_n=10):
    if song_name not in df['name'].values:
        return {"error": f"Song '{song_name}' not found in the DataFrame."}
    
    idx = df.index[df['name'] == song_name][0]
    song_cluster = df.loc[idx, 'cluster']
    cluster_indices = df[df['cluster'] == song_cluster].index
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = [score for score in sim_scores if score[0] in cluster_indices]
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    
    if len(sim_scores) == 0:
        return []

    song_indices = [i[0] for i in sim_scores]
    recommendations = df.iloc[song_indices][['name', 'artist', 'genre']].to_dict(orient='records')
    
    return recommendations

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the unique list of song names
    song_names = df['name'].unique().tolist()
    songs = None

    if request.method == 'POST':
        selected_song = request.form.get('names')
        print(f"Selected Song: {selected_song}")  # Debugging print
        songs = recommend_songs(selected_song, df, cosine_sim)
        print(f"Recommendations: {songs}")  # Debugging print

    return render_template('index.html', name=song_names, songs=songs)

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




